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

# Global session storage with enhanced structure
active_sessions: Dict[str, Dict[str, Any]] = {}
persistent_tool_sessions: Dict[str, str] = {}  # Maps package_name to session_id

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate bearer token if secure mode is enabled"""
    bearer_token = os.environ.get("FMCP_BEARER_TOKEN")
    secure_mode = os.environ.get("FMCP_SECURE_MODE") == "true"
    
    if not secure_mode:
        return None
    if not credentials or credentials.scheme.lower() != "bearer" or credentials.credentials != bearer_token:
        raise HTTPException(status_code=401, detail="Invalid or missing authorization token")
    return credentials.credentials

def fix_npm_permissions():
    """Fix npm permissions automatically without requiring sudo"""
    try:
        npm_cache_dir = Path.home() / ".npm"
        npm_global_dir = Path.home() / ".npm-global"
        
        # Check if we have permission issues
        if npm_cache_dir.exists():
            try:
                # Try to create a test file in npm cache
                test_file = npm_cache_dir / "test_permissions"
                test_file.touch()
                test_file.unlink()
            except PermissionError:
                print("🔧 Fixing npm cache permissions...")
                # Clear the problematic cache instead of using sudo
                import shutil
                if npm_cache_dir.exists():
                    try:
                        shutil.rmtree(npm_cache_dir)
                        npm_cache_dir.mkdir(exist_ok=True)
                        print("✅ Cleared npm cache")
                    except Exception as e:
                        print(f"⚠️  Could not clear npm cache: {e}")
        
        # Set up npm global directory
        if not npm_global_dir.exists():
            npm_global_dir.mkdir(exist_ok=True)
            
        # Configure npm to use the new directory
        try:
            subprocess.run(
                ["npm", "config", "set", "prefix", str(npm_global_dir)], 
                check=False, 
                capture_output=True
            )
            subprocess.run(
                ["npm", "config", "set", "cache", str(npm_cache_dir)], 
                check=False, 
                capture_output=True
            )
            print("✅ Configured npm global directory")
        except Exception as e:
            print(f"⚠️  Could not configure npm: {e}")
            
        return True
    except Exception as e:
        print(f"⚠️  Error fixing npm permissions: {e}")
        return False

def create_clean_npm_environment():
    """Create a clean npm environment for the current session"""
    try:
        # Create temporary directories
        temp_cache = Path.cwd() / ".temp_npm_cache"
        temp_global = Path.cwd() / ".temp_npm_global"
        
        temp_cache.mkdir(exist_ok=True)
        temp_global.mkdir(exist_ok=True)
        
        # Return environment variables for clean npm
        return {
            "NPM_CONFIG_CACHE": str(temp_cache),
            "NPM_CONFIG_PREFIX": str(temp_global),
            "NPM_CONFIG_USER_CONFIG": "/dev/null",  # Ignore user config
            "NPM_CONFIG_GLOBAL_CONFIG": "/dev/null"  # Ignore global config
        }
    except Exception:
        return {}

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
        
        # Handle npm/npx commands with permission fixes
        if base_command in ["npx", "npm"]:
            # First, try to fix npm permissions
            fix_npm_permissions()
            
            # Find the command
            command_path = shutil.which(base_command)
            if command_path:
                base_command = command_path
            
            # Create clean npm environment
            clean_npm_env = create_clean_npm_environment()
        else:
            clean_npm_env = {}
        
        args = [arg.replace("<path to mcp-servers>", str(dest_dir)) for arg in raw_args]
        stdio_command = [base_command] + args
        
        # Combine environments
        env_vars = servers.get("env", {})
        env = {**dict(os.environ), **env_vars, **clean_npm_env}
        
        print(f"🔍 Attempting to launch: {stdio_command}")
        print(f"🔍 Working directory: {dest_dir}")
        print(f"🔍 Environment vars: {list(env_vars.keys())}")
        
        # Try with clean environment first
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
        time.sleep(2)  # Give it more time to start
        
        if process.poll() is not None:
            # Process already terminated - try fallback
            stderr_output = process.stderr.read()
            print(f"❌ Process terminated. Exit code: {process.returncode}")
            print(f"❌ Error output: {stderr_output}")
            
            # Try fallback: use npx with --no-install
            if base_command.endswith("npx") and "-y" in args:
                print("🔄 Trying fallback with --no-install...")
                fallback_args = [arg.replace("-y", "--no-install") for arg in args]
                fallback_command = [base_command] + fallback_args
                
                process = subprocess.Popen(
                    fallback_command,
                    cwd=dest_dir,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=env,
                    text=True,
                    bufsize=1
                )
                
                time.sleep(1)
                if process.poll() is not None:
                    print("❌ Fallback also failed")
                    return None, None
        
        print(f"✅ Process started successfully with PID: {process.pid}")
        
        # Initialize MCP server
        if not initialize_mcp_server(process):
            print(f"Warning: Failed to initialize MCP server for {pkg}")
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
    
    # ===== STANDARD SSE PATTERN IMPLEMENTATION =====
    
    @router.post(f"/{package_name}/sse/start", tags=[package_name])
    async def start_sse_session(token: str = Depends(get_token)):
        """Start a new empty SSE session - NO query here (Standard Pattern)"""
        try:
            session_id = str(uuid.uuid4())
            
            # Create empty session with message queue
            active_sessions[session_id] = {
                "messages": [],           # Message queue
                "processed_count": 0,     # Track processed messages
                "status": "ready",        # Session status
                "created_at": time.time(),
                "package_name": package_name,
                "process": process,
                "context": {}            # Conversation context
            }
            
            return JSONResponse(content={
                "session_id": session_id,
                "status": "ready",
                "message_url": f"/{package_name}/sse/message?session_id={session_id}",
                "stream_url": f"/{package_name}/sse/stream?session_id={session_id}"
            })
            
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})

    @router.post(f"/{package_name}/sse/message", tags=[package_name])
    async def add_message(
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
        ),
        session_id: str = Query(..., description="Session ID from /sse/start"),
        token: str = Depends(get_token)
    ):
        """Add message to session queue - triggers real-time processing"""
        
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = active_sessions[session_id]
        
        # Add message to queue
        message_id = str(uuid.uuid4())
        message = {
            "id": message_id,
            "content": request,
            "timestamp": time.time(),
            "status": "queued"
        }
        
        session["messages"].append(message)
        session["status"] = "has_new_messages"
        
        return JSONResponse(content={
            "message_id": message_id,
            "status": "queued",
            "queue_position": len(session["messages"]),
            "session_status": session["status"]
        })
    
    @router.get(f"/{package_name}/sse/stream", tags=[package_name])
    async def stream_sse(
        session_id: str = Query(..., description="Session ID from /sse/start"),
        token: str = Depends(get_token)
    ):
        """Stream real-time responses as server processes message queue"""
        
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = active_sessions[session_id]
        
        async def event_generator() -> AsyncGenerator[str, None]:
            try:
                # Initial connection
                yield f"event: connected\ndata: {json.dumps({'session_id': session_id, 'status': 'connected'})}\n\n"
                
                # Process messages as they arrive
                while session_id in active_sessions:
                    session = active_sessions[session_id]
                    total_messages = len(session["messages"])
                    processed_count = session["processed_count"]
                    
                    # Process new messages
                    if total_messages > processed_count:
                        for i in range(processed_count, total_messages):
                            message = session["messages"][i]
                            
                            # Start processing message
                            yield f"event: processing\ndata: {json.dumps({'message_id': message['id'], 'status': 'processing'})}\n\n"
                            
                            try:
                                # Send to MCP server
                                mcp_request = message["content"]
                                msg = json.dumps(mcp_request)
                                process.stdin.write(msg + "\n")
                                process.stdin.flush()
                                
                                # Read and stream MCP response
                                response_line = process.stdout.readline()
                                if response_line:
                                    response_line = response_line.strip()
                                    
                                    # Send response as it comes
                                    yield f"event: response\ndata: {response_line}\n\n"
                                    
                                    # Update message status
                                    message["status"] = "completed"
                                    message["response"] = response_line
                                    
                                    # Check if this is an error or final response
                                    try:
                                        response_data = json.loads(response_line)
                                        if "error" in response_data:
                                            yield f"event: error\ndata: {response_line}\n\n"
                                        elif "result" in response_data:
                                            yield f"event: result\ndata: {session["messages"]}\n\n"
                                    except json.JSONDecodeError:
                                        # Handle non-JSON responses
                                        yield f"event: text\ndata: {json.dumps({'text': response_line})}\n\n"
                                
                            except Exception as e:
                                error_data = json.dumps({
                                    "message_id": message["id"], 
                                    "error": str(e)
                                })
                                yield f"event: error\ndata: {error_data}\n\n"
                                message["status"] = "error"
                            
                            session["processed_count"] += 1
                    
                    # Check for session completion
                    if processed_count >= total_messages and session.get("status") != "has_new_messages":
                        yield f"event: idle\ndata: {json.dumps({'status': 'waiting_for_messages'})}\n\n"
                    
                    session["status"] = "ready"  # Reset status
                    await asyncio.sleep(0.1)  # Poll interval for new messages
                    
            except Exception as e:
                error_data = json.dumps({"error": str(e), "session_id": session_id})
                yield f"event: error\ndata: {error_data}\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
    
    # ===== SESSION MANAGEMENT ENDPOINTS =====
    
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
            "status": session["status"],
            "created_at": session["created_at"],
            "package_name": session["package_name"],
            "message_count": len(session.get("messages", [])),
            "processed_count": session.get("processed_count", 0)
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
    
    # ===== SSE PERSISTENT SESSION ENDPOINTS =====
    
    @router.post(f"/{package_name}/sse/tools/call", tags=[package_name])
    async def sse_tools_call(
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
        ),
        timeout: int = Query(30, description="Timeout in seconds"),
        reset_session: bool = Query(False, description="Force create new session"),
        token: str = Depends(get_token)
    ):
        """
        Convenient endpoint that maintains a persistent session for the package:
        1. Reuses existing session for this package (if available)
        2. Creates new session only if none exists or reset_session=true
        3. Sends message to session
        4. Waits for completion
        5. Returns message_id and session messages
        6. Keeps session alive for future calls
        
        Returns the same format as the SSE result event.
        """
        
        session_id = None
        is_new_session = False
        
        try:
            # Step 1: Get or create persistent session for this package
            if reset_session and package_name in persistent_tool_sessions:
                # Clean up old session if reset requested
                old_session_id = persistent_tool_sessions[package_name]
                if old_session_id in active_sessions:
                    del active_sessions[old_session_id]
                del persistent_tool_sessions[package_name]
            
            # Check if we have an existing session for this package
            if package_name in persistent_tool_sessions:
                session_id = persistent_tool_sessions[package_name]
                
                # Verify session still exists and is valid
                if session_id not in active_sessions:
                    # Session was cleaned up elsewhere, create new one
                    del persistent_tool_sessions[package_name]
                    session_id = None
            
            # Create new session if needed
            if session_id is None:
                session_id = str(uuid.uuid4())
                is_new_session = True
                
                active_sessions[session_id] = {
                    "messages": [],
                    "processed_count": 0,
                    "status": "ready",
                    "created_at": time.time(),
                    "package_name": package_name,
                    "process": process,
                    "context": {},
                    "persistent": True  # Mark as persistent
                }
                
                # Store persistent mapping
                persistent_tool_sessions[package_name] = session_id
            
            session = active_sessions[session_id]
            
            # Step 2: Add message to queue
            message_id = str(uuid.uuid4())
            message = {
                "id": message_id,
                "content": request,
                "timestamp": time.time(),
                "status": "queued"
            }
            
            session["messages"].append(message)
            session["status"] = "has_new_messages"
            session["last_used"] = time.time()  # Track usage for cleanup
            
            # Step 3: Process the new message and wait for result
            start_time = time.time()
            current_message_index = len(session["messages"]) - 1  # Index of our message
            
            while time.time() - start_time < timeout:
                session = active_sessions[session_id]
                
                # Check if our specific message has been processed
                if current_message_index < session["processed_count"]:
                    # Our message has been processed
                    processed_message = session["messages"][current_message_index]
                    
                    if processed_message["status"] == "completed":
                        # Return successful result
                        return JSONResponse(content={
                            "message_id": message_id,
                            "session_id": session_id,
                            "is_new_session": is_new_session,
                            "total_messages": len(session["messages"]),
                            "messages": session["messages"]
                        })
                    elif processed_message["status"] == "error":
                        # Return error result
                        error_detail = processed_message.get("error", "Unknown MCP error")
                        raise HTTPException(
                            status_code=500,
                            detail=f"MCP processing error: {error_detail}"
                        )
                
                # Process messages if we're behind
                total_messages = len(session["messages"])
                processed_count = session["processed_count"]
                
                if total_messages > processed_count:
                    message_to_process = session["messages"][processed_count]
                    
                    try:
                        # Send to MCP server
                        mcp_request = message_to_process["content"]
                        msg = json.dumps(mcp_request)
                        process.stdin.write(msg + "\n")
                        process.stdin.flush()
                        
                        # Read response
                        response_line = process.stdout.readline()
                        if response_line:
                            response_line = response_line.strip()
                            
                            # Update message status
                            message_to_process["status"] = "completed"
                            message_to_process["response"] = response_line
                            session["processed_count"] += 1
                            
                            # Continue loop to check if our message is done
                            continue
                            
                    except Exception as e:
                        message_to_process["status"] = "error"
                        message_to_process["error"] = str(e)
                        session["processed_count"] += 1
                        
                        # Continue loop to check if our message is done
                        continue
                
                # Small delay to prevent busy waiting
                await asyncio.sleep(0.1)
            
            # Timeout occurred
            raise HTTPException(
                status_code=408,
                detail=f"Request timeout after {timeout} seconds"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        # Note: We DON'T clean up the session here - it's persistent!
    
    # Add session cleanup endpoint for persistent sessions
    @router.delete(f"/{package_name}/sse/tools/session", tags=[package_name])
    async def cleanup_persistent_session(token: str = Depends(get_token)):
        """Clean up the persistent session for this package"""
        
        if package_name in persistent_tool_sessions:
            session_id = persistent_tool_sessions[package_name]
            
            # Clean up session
            if session_id in active_sessions:
                del active_sessions[session_id]
            
            del persistent_tool_sessions[package_name]
            
            return JSONResponse(content={
                "package_name": package_name,
                "session_id": session_id,
                "status": "cleaned_up"
            })
        else:
            return JSONResponse(content={
                "package_name": package_name,
                "status": "no_persistent_session"
            })

    # Add session info endpoint
    @router.get(f"/{package_name}/sse/tools/session/info", tags=[package_name])
    async def get_persistent_session_info(token: str = Depends(get_token)):
        """Get info about the persistent session for this package"""
        
        if package_name in persistent_tool_sessions:
            session_id = persistent_tool_sessions[package_name]
            
            if session_id in active_sessions:
                session = active_sessions[session_id]
                return JSONResponse(content={
                    "package_name": package_name,
                    "session_id": session_id,
                    "status": "active",
                    "created_at": session["created_at"],
                    "last_used": session.get("last_used", session["created_at"]),
                    "total_messages": len(session["messages"]),
                    "processed_count": session["processed_count"]
                })
            else:
                # Session ID exists but session was cleaned up
                del persistent_tool_sessions[package_name]
                return JSONResponse(content={
                    "package_name": package_name,
                    "status": "orphaned_cleaned_up"
                })
        else:
            return JSONResponse(content={
                "package_name": package_name,
                "status": "no_persistent_session"
            })
    
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
