import os
import json
import subprocess
import shutil
import uuid
import asyncio
from typing import AsyncGenerator, Dict, Any, Union
from pathlib import Path
from loguru import logger
import time
import sys
import threading
from fastapi import FastAPI, Request, APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import time

security = HTTPBearer(auto_error=False)

# Global session storage
active_sessions: Dict[str, Dict[str, Any]] = {}

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate bearer token if secure mode is enabled"""
    bearer_token = os.environ.get("FMCP_BEARER_TOKEN")
    secure_mode = os.environ.get("FMCP_SECURE_MODE") == "true"
    
    if not secure_mode:
        return None
    if not credentials or credentials.scheme.lower() != "bearer" or credentials.credentials != bearer_token:
        raise HTTPException(status_code=401, detail="Invalid or missing authorization token")
    return credentials.credentials

def launch_mcp_using_fastapi_proxy(dest_dir: Union[str, Path]):
    dest_dir = Path(dest_dir)
    metadata_path = dest_dir / "metadata.json"
    try:
        if not metadata_path.exists():
            logger.info(f":warning: No metadata.json found at {metadata_path}")
            return None, None
        print(f":blue_book: Reading metadata.json from {metadata_path}")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        pkg = list(metadata["mcpServers"].keys())[0]
        servers = metadata['mcpServers'][pkg]
        print(pkg, servers)
    except Exception as e:
        print(f":x: Error reading metadata.json: {e}")
        return None, None
    try:
        base_command = servers["command"]
        raw_args = servers["args"]
        if base_command == "npx" or base_command == "npm":
            npm_path = shutil.which("npm")
            npx_path = shutil.which("npx")
            if npm_path and base_command == "npm":
                base_command = npm_path
            elif npx_path and base_command == "npx":
                base_command = npx_path
        args = [arg.replace("<path to mcp-servers>", str(dest_dir)) for arg in raw_args]
        stdio_command = [base_command] + args
        env_vars = servers.get("env", {})
        env = {**dict(os.environ), **env_vars}
        
        # Add diagnostic information
        print(f"🔍 Attempting to launch: {stdio_command}")
        print(f"🔍 Working directory: {dest_dir}")
        print(f"🔍 Environment vars: {list(env_vars.keys())}")
        
        process = subprocess.Popen(
            stdio_command,
            cwd=dest_dir,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            bufsize=1
        )
        
        # Check if process started successfully
        time.sleep(1)  # Give it a moment to start
        if process.poll() is not None:
            # Process already terminated
            stderr_output = process.stderr.read()
            print(f"❌ Process terminated immediately. Exit code: {process.returncode}")
            print(f"❌ Error output: {stderr_output}")
            return None, None
        
        print(f"✅ Process started successfully with PID: {process.pid}")
        
        # NOW try to initialize
        if not initialize_mcp_server(process):
            print(f"Warning: Failed to initialize MCP server for {pkg}")
            # Get error details
            if process.poll() is not None:
                stderr_output = process.stderr.read()
                print(f"Process error output: {stderr_output}")
               
        router = create_mcp_router(pkg, process)
        return pkg, router
    except FileNotFoundError as e:
        print(f":x: Command not found: {e}")
        return None, None
    except Exception as e:
        print(f":x: Error launching MCP server: {e}")
        return None, None

def create_fastapi_jsonrpc_proxy(package_name: str, process: subprocess.Popen) -> FastAPI:
    app = FastAPI()
    @app.post(f"/{package_name}/mcp")
    async def proxy_jsonrpc(request: Request):
        try:
            jsonrpc_request = await request.body()
            jsonrpc_str = jsonrpc_request.decode() if isinstance(jsonrpc_request, bytes) else jsonrpc_request
            # Send to MCP server via stdin
            process.stdin.write(jsonrpc_str + "\n")
            process.stdin.flush()
            # Read from MCP server stdout
            response_line = process.stdout.readline()
            return JSONResponse(content=json.loads(response_line))
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
    return app

def start_fastapi_in_thread(app: FastAPI, port: int):
    def run():
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    thread = threading.Thread(target=run, daemon=True)
    thread.start()

def initialize_mcp_server(process: subprocess.Popen) -> bool:
    """Initialize MCP server with proper handshake"""
    try:
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
                "clientInfo": {"name": "fluidmcp-client", "version": "1.0.0"}
            }
        }
        
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Wait for response
        start_time = time.time()
        while time.time() - start_time < 10:
            if process.poll() is not None:
                return False
            response_line = process.stdout.readline().strip()
            if response_line:
                response = json.loads(response_line)
                if response.get("id") == 0 and "result" in response:
                    # Send initialized notification
                    notif = {"jsonrpc": "2.0", "method": "notifications/initialized"}
                    process.stdin.write(json.dumps(notif) + "\n")
                    process.stdin.flush()
                    return True
            time.sleep(0.1)
        return False
    except Exception as e:
        print(f"Initialization error: {e}")
        return False

def create_mcp_router(package_name: str, process: subprocess.Popen) -> APIRouter:
    router = APIRouter()

    @router.post(f"/{package_name}/mcp", tags=[package_name])
    async def proxy_jsonrpc(
        request: Dict[str, Any] = Body(
            ...,
            example={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "",
                "params": {}
            }
        ), token: str = Depends(get_token)
    ):
        try:
            # Convert dict to JSON string
            msg = json.dumps(request)
            process.stdin.write(msg + "\n")
            process.stdin.flush()
            response_line = process.stdout.readline()
            return JSONResponse(content=json.loads(response_line))
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
    
    # SSE Session Management Endpoints
    @router.post(f"/{package_name}/sse/start", tags=[package_name])
    async def start_sse_session(
        request: Dict[str, Any] = Body(
            ...,
            example={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "tool_name",
                    "arguments": {}
                }
            }
        ), token: str = Depends(get_token)
    ):
        """Start a new SSE session and return session ID"""
        try:
            session_id = str(uuid.uuid4())
            
            # Store session data
            active_sessions[session_id] = {
                "request": request,
                "package_name": package_name,
                "process": process,
                "status": "initialized",
                "created_at": time.time()
            }
            
            return JSONResponse(content={
                "session_id": session_id,
                "status": "initialized",
                "stream_url": f"/{package_name}/sse/stream?session_id={session_id}"
            })
            
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
    
    @router.get(f"/{package_name}/sse/stream", tags=[package_name])
    async def stream_sse(
        session_id: str = Query(..., description="Session ID from /sse/start"),
        token: str = Depends(get_token)
    ):
        """Stream SSE events for a specific session"""
        
        # Check if session exists
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = active_sessions[session_id]
        request = session["request"]
        
        async def event_generator() -> AsyncGenerator[str, None]:
            try:
                # Send initial connection event
                yield f"event: connection\ndata: {json.dumps({'status': 'connected', 'session_id': session_id})}\n\n"
                
                # Send the request to MCP server
                msg = json.dumps(request)
                process.stdin.write(msg + "\n")
                process.stdin.flush()
                
                session['status'] = "processing"
                yield f"event: status\ndata: {json.dumps({'status': 'processing'})}\n\n"
                
                # Read and stream responses
                while True:
                    response_line = process.stdout.readline()
                    if not response_line:
                        break
                    
                    response_line = response_line.strip()
                    if response_line:
                        # Send as data event
                        yield f"event: data\ndata: {response_line}\n\n"
                        
                        try:
                            response_data = json.loads(response_line)
                            # Check if this is the final result
                            if "result" in response_data:
                                session['status'] = "completed"
                                yield f"event: complete\ndata: {json.dumps({'status': 'completed'})}\n\n"
                                break
                            elif "error" in response_data:
                                session['status'] = "error"
                                yield f"event: error\ndata: {response_line}\n\n"
                                break
                        except json.JSONDecodeError:
                            # Send non-JSON data as raw text
                            yield f"event: text\ndata: {json.dumps({'text': response_line})}\n\n"
                    
                    # Small delay to prevent overwhelming
                    await asyncio.sleep(0.01)
                    
            except Exception as e:
                session['status'] = "error"
                error_data = json.dumps({"error": str(e), "session_id": session_id})
                yield f"event: error\ndata: {error_data}\n\n"
            finally:
                # Clean up session after completion
                if session_id in active_sessions:
                    del active_sessions[session_id]
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Disable nginx buffering
            }
        )
    
    @router.get(f"/{package_name}/sse/status/{{session_id}}", tags=[package_name])
    async def get_session_status(
        session_id: str,
        token: str = Depends(get_token)
    ):
        """Get the status of a specific session"""
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = active_sessions[session_id]
        return JSONResponse(content={
            "session_id": session_id,
            "status": session['status'],
            "created_at": session["created_at"],
            "package_name": session["package_name"]
        })
    
    @router.delete(f"/{package_name}/sse/{{session_id}}", tags=[package_name])
    async def cancel_session(
        session_id: str,
        token: str = Depends(get_token)
    ):
        """Cancel and cleanup a specific session"""
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        del active_sessions[session_id]
        return JSONResponse(content={
            "session_id": session_id,
            "status": "cancelled"
        })
        
    @router.get(f"/{package_name}/mcp/tools/list", tags=[package_name])
    async def list_tools(token: str = Depends(get_token)):
        try:
            # Pre-filled JSON-RPC request for tools/list
            request_payload = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "tools/list"
            }
            
            # Convert to JSON string and send to MCP server
            msg = json.dumps(request_payload)
            process.stdin.write(msg + "\n")
            process.stdin.flush()
            
            # Read response from MCP server
            response_line = process.stdout.readline()
            response_data = json.loads(response_line)
            
            return JSONResponse(content=response_data)
            
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
        
    @router.post(f"/{package_name}/mcp/tools/call", tags=[package_name])
    async def call_tool(request_body: Dict[str, Any] = Body(
        ...,
        alias="params",
        example={
            "name": "", 
        }
    ), token: str = Depends(get_token)
):      
        params = request_body

        try:
            # Validate required fields
            if "name" not in params:
                return JSONResponse(
                    status_code=400, 
                    content={"error": "Tool name is required"}
                )
            
            # Construct complete JSON-RPC request
            request_payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": params
            }
            
            # Send to MCP server
            msg = json.dumps(request_payload)
            process.stdin.write(msg + "\n")
            process.stdin.flush()
            
            # Read response
            response_line = process.stdout.readline()
            response_data = json.loads(response_line)
            
            return JSONResponse(content=response_data)
            
        except json.JSONDecodeError:
            return JSONResponse(
                status_code=400, 
                content={"error": "Invalid JSON in request body"}
            )
        except Exception as e:
            return JSONResponse(
                status_code=500, 
                content={"error": str(e)}
            )
    return router

if __name__ == '__main__':
    app = FastAPI()
    install_paths = [
        "/workspaces/fluid-ai-gpt-mcp/fluidmcp/.fmcp-packages/Perplexity/perplexity-ask/0.1.0",
        "/workspaces/fluid-ai-gpt-mcp/fluidmcp/.fmcp-packages/Airbnb/airbnb/0.1.0"
    ]
    for install_path in install_paths:
        print(f"Launching MCP server for {install_path}")
        package_name, router = launch_mcp_using_fastapi_proxy(install_path)
        if package_name is not None and router is not None:
            app.include_router(router)
        else:
            print(f"Skipping {install_path} due to missing metadata or launch error.")
    uvicorn.run(app, host="0.0.0.0", port=8099)
