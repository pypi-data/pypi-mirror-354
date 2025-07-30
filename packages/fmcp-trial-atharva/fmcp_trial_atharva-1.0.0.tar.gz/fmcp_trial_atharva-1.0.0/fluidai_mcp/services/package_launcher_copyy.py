import os
import json
import subprocess
import shutil
from typing import AsyncGenerator, Dict, Any, Union
from pathlib import Path
from loguru import logger
import time
import sys
import threading
from fastapi import FastAPI, Request, APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import time

security = HTTPBearer(auto_error=False)

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
        import time
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
    
    # New SSE endpoint
    @router.post(f"/{package_name}/sse", tags=[package_name])
    async def sse_stream(
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
        async def event_generator() -> AsyncGenerator[str, None]:
            try:
                msg = json.dumps(request)
                process.stdin.write(msg + "\n")
                process.stdin.flush()
                
                # Read from stdout and stream as SSE events
                while True:
                    response_line = process.stdout.readline()
                    if not response_line:
                        break
                    
                    logger.debug(f"Received from MCP: {response_line.strip()}")
                    
                    # Format as SSE event
                    yield f"data: {response_line.strip()}\n\n"
                    
                    try:
                        response_data = json.loads(response_line)
                        if "result" in response_data:
                            break
                    except json.JSONDecodeError:
                        pass
                    
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream"
        )
        
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
