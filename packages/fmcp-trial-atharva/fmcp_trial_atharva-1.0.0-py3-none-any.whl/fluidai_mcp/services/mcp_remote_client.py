#!/usr/bin/env python3
"""
FluidMCP Remote Client - Unified MCP STDIO to HTTP Bridge
Supports both single package and multi-package modes
"""
import sys
import json
import asyncio
import aiohttp
import os
import re
from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass

@dataclass
class PackageInfo:
    name: str
    session_id: Optional[str] = None
    tools: List[Dict[str, Any]] = None

class FluidMCPRemoteClient:
    def __init__(self):
        self.server_url = os.environ.get("FMCP_SERVER_URL", "http://localhost:8099")
        self.bearer_token = os.environ.get("FMCP_BEARER_TOKEN")
        self.single_package_mode = os.environ.get("FMCP_PACKAGE_NAME")
        self.packages: Dict[str, PackageInfo] = {}
        self.headers = {"Content-Type": "application/json"}
        
        if self.bearer_token:
            self.headers["Authorization"] = f"Bearer {self.bearer_token}"

    # === PACKAGE DISCOVERY ===
    async def discover_packages(self) -> bool:
        """Discover available packages from the server"""
        if self.single_package_mode:
            # Single package mode
            if await self._test_package(self.single_package_mode):
                self.packages[self.single_package_mode] = PackageInfo(self.single_package_mode)
                return True
            return False
        else:
            # Multi-package mode
            return await self._discover_all_packages()

    async def _discover_all_packages(self) -> bool:
        """Discover all available packages"""
        discovered_packages = []
        
        # Try common package names
        common_packages = [
            "tavily-mcp", "postgres", "google-maps", "dart", "sequential-thinking",
            "neo4j-aura", "brave-search", "perplexity-ask", "airbnb", "jupyter"
        ]
        
        for package_name in common_packages:
            if await self._test_package(package_name):
                self.packages[package_name] = PackageInfo(package_name)
                discovered_packages.append(package_name)
        
        print(f"Discovered {len(discovered_packages)} packages: {discovered_packages}", file=sys.stderr)
        return len(discovered_packages) > 0

    async def _test_package(self, package_name: str) -> bool:
        """Test if a package endpoint is available"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.server_url}/{package_name}/mcp/tools/list",
                    headers=self.headers,
                    timeout=3
                ) as resp:
                    return resp.status == 200
        except:
            return False

    # === SESSION MANAGEMENT ===
    async def initialize_package_session(self, package_name: str) -> Optional[str]:
        """Initialize SSE session for a package"""
        if package_name not in self.packages:
            return None
            
        package_info = self.packages[package_name]
        if package_info.session_id:
            return package_info.session_id

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.server_url}/{package_name}/sse/start",
                    headers=self.headers,
                    timeout=10
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        session_id = result["session_id"]
                        package_info.session_id = session_id
                        print(f"Session initialized for {package_name}: {session_id}", file=sys.stderr)
                        return session_id
                    else:
                        print(f"Failed to start session for {package_name}: {resp.status}", file=sys.stderr)
                        return None
        except Exception as e:
            print(f"Session init error for {package_name}: {e}", file=sys.stderr)
            return None

    # === TOOL MANAGEMENT ===
    async def get_all_tools(self) -> List[Dict[str, Any]]:
        """Get tools from all packages"""
        all_tools = []
        
        for package_name, package_info in self.packages.items():
            tools = await self._get_package_tools(package_name)
            if tools:
                # Process tools for multi-package mode
                if not self.single_package_mode:
                    tools = self._add_package_prefix_to_tools(tools, package_name)
                all_tools.extend(tools)
        
        return all_tools

    async def _get_package_tools(self, package_name: str) -> List[Dict[str, Any]]:
        """Get tools from a specific package"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.server_url}/{package_name}/mcp/tools/list",
                    headers=self.headers,
                    timeout=10
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        if "result" in result and "tools" in result["result"]:
                            tools = result["result"]["tools"]
                            # Validate and clean tools
                            validated_tools = []
                            for tool in tools:
                                validated_tool = self._validate_tool_schema(tool)
                                if validated_tool:
                                    validated_tools.append(validated_tool)
                            return validated_tools
        except Exception as e:
            print(f"Failed to get tools from {package_name}: {e}", file=sys.stderr)
        return []

    def _add_package_prefix_to_tools(self, tools: List[Dict], package_name: str) -> List[Dict]:
        """Add package prefix to tool names for multi-package mode"""
        prefixed_tools = []
        for tool in tools:
            tool_copy = tool.copy()
            original_name = tool["name"]
            clean_package = self._clean_name(package_name)
            clean_tool = self._clean_name(original_name)
            
            # Add package metadata for routing
            tool_copy["_package"] = package_name
            tool_copy["_original_name"] = original_name
            tool_copy["name"] = f"{clean_package}_{clean_tool}"
            
            prefixed_tools.append(tool_copy)
        return prefixed_tools

    def _clean_name(self, name: str) -> str:
        """Clean name to match Claude's pattern ^[a-zA-Z0-9_-]{1,64}$"""
        # Replace invalid characters with underscores
        cleaned = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
        # Limit to 64 characters
        cleaned = cleaned[:64]
        # Ensure it doesn't start or end with underscore/hyphen
        cleaned = cleaned.strip('_-')
        return cleaned or "tool"

    def _validate_tool_schema(self, tool: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Validate and clean tool schema"""
        if not tool.get("name") or not tool.get("description"):
            return None

        clean_tool = {
            "name": str(tool["name"]),
            "description": str(tool["description"])
        }

        # Copy package metadata if present
        for meta_field in ["_package", "_original_name"]:
            if meta_field in tool:
                clean_tool[meta_field] = tool[meta_field]

        # Handle inputSchema
        if "inputSchema" in tool and isinstance(tool["inputSchema"], dict):
            clean_tool["inputSchema"] = self._clean_input_schema(tool["inputSchema"])

        return clean_tool

    def _clean_input_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Clean input schema for Claude compatibility"""
        clean_schema = {
            "type": schema.get("type", "object"),
            "properties": {},
            "required": []
        }

        if "properties" in schema and isinstance(schema["properties"], dict):
            for prop_name, prop_def in schema["properties"].items():
                if isinstance(prop_def, dict):
                    clean_prop = {}
                    # Copy allowed fields
                    for field in ["type", "description", "enum", "items", "minimum", "maximum"]:
                        if field in prop_def:
                            clean_prop[field] = prop_def[field]
                    
                    # Handle default values
                    if "default" in prop_def and prop_def["default"] is not None:
                        clean_prop["default"] = prop_def["default"]
                    
                    clean_schema["properties"][str(prop_name)] = clean_prop

        if "required" in schema and isinstance(schema["required"], list):
            clean_schema["required"] = [str(req) for req in schema["required"]]

        return clean_schema

    # === TOOL CALLING ===
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any], request_id: int) -> Dict[str, Any]:
        """Call a tool, routing to correct package"""
        package_name, actual_tool_name = self._parse_tool_name(tool_name)
        
        if not package_name:
            return self._error_response(request_id, -32601, f"Tool not found: {tool_name}")

        # Ensure session exists
        session_id = await self.initialize_package_session(package_name)
        if not session_id:
            return self._error_response(request_id, -32603, f"Failed to initialize session for {package_name}")

        # Prepare tool call request
        tool_request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/call",
            "params": {
                "name": actual_tool_name,
                "arguments": arguments
            }
        }

        # Make the call
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.server_url}/{package_name}/sse/tools/call",
                    headers=self.headers,
                    json=tool_request,
                    timeout=30
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return self._extract_tool_response(result, request_id)
                    else:
                        text = await resp.text()
                        return self._error_response(request_id, -32603, f"Tool call failed: {resp.status} - {text}")
        except Exception as e:
            return self._error_response(request_id, -32603, f"Tool call error: {e}")

    def _parse_tool_name(self, tool_name: str) -> tuple[Optional[str], str]:
        """Parse tool name to extract package and actual tool name"""
        if self.single_package_mode:
            return self.single_package_mode, tool_name
        
        # Multi-package mode: extract package from prefixed name
        if "_" in tool_name:
            parts = tool_name.split("_", 1)
            if len(parts) == 2:
                package_name = parts[0]
                actual_tool_name = parts[1]
                
                # Verify package exists
                if package_name in self.packages:
                    return package_name, actual_tool_name
        
        # Fallback: search for tool in all packages
        for package_name in self.packages:
            if self._package_has_tool_sync(package_name, tool_name):
                return package_name, tool_name
        
        return None, tool_name

    def _package_has_tool_sync(self, package_name: str, tool_name: str) -> bool:
        """Synchronous check if package has tool (for fallback)"""
        # This is a simplified check - in practice you might want to cache tool lists
        return package_name in self.packages

    def _extract_tool_response(self, sse_result: Dict[str, Any], request_id: int) -> Dict[str, Any]:
        """Extract MCP response from SSE result"""
        if "messages" in sse_result and sse_result["messages"]:
            last_message = sse_result["messages"][-1]
            if "response" in last_message and last_message["status"] == "completed":
                try:
                    return json.loads(last_message["response"])
                except json.JSONDecodeError:
                    return self._error_response(request_id, -32603, "Invalid response from MCP server")
        
        return self._error_response(request_id, -32603, "No response from tool call")

    # === MCP REQUEST HANDLING ===
    async def handle_mcp_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle MCP request"""
        method = request.get("method")
        request_id = request.get("id")

        if method == "initialize":
            return await self._handle_initialize(request_id)
        elif method == "notifications/initialized":
            return None
        elif method == "tools/list":
            return await self._handle_tools_list(request_id)
        elif method == "tools/call":
            return await self._handle_tools_call(request)
        else:
            return self._error_response(request_id, -32601, f"Method not found: {method}")

    async def _handle_initialize(self, request_id: int) -> Dict[str, Any]:
        """Handle initialize request"""
        success = await self.discover_packages()
        if success:
            mode = "single-package" if self.single_package_mode else "multi-package"
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": f"FluidMCP-{mode} ({len(self.packages)} packages)",
                        "version": "1.0.0"
                    }
                }
            }
        else:
            return self._error_response(request_id, -32603, "No FluidMCP packages available")

    async def _handle_tools_list(self, request_id: int) -> Dict[str, Any]:
        """Handle tools/list request"""
        try:
            if not self.packages:
                await self.discover_packages()
            
            all_tools = await self.get_all_tools()
            print(f"Returning {len(all_tools)} tools from {len(self.packages)} packages", file=sys.stderr)
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"tools": all_tools}
            }
        except Exception as e:
            return self._error_response(request_id, -32603, f"Failed to get tools: {e}")

    async def _handle_tools_call(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        params = request.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        request_id = request.get("id")

        if not tool_name:
            return self._error_response(request_id, -32602, "Tool name is required")

        return await self.call_tool(tool_name, arguments, request_id)

    def _error_response(self, request_id: int, code: int, message: str) -> Dict[str, Any]:
        """Create error response"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message}
        }

    # === MAIN LOOP ===
    async def run(self):
        """Main STDIO loop"""
        mode = "single-package" if self.single_package_mode else "multi-package"
        print(f"FluidMCP Remote Client starting in {mode} mode...", file=sys.stderr)
        print(f"Server: {self.server_url}", file=sys.stderr)
        
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                    response = await self.handle_mcp_request(request)
                    
                    if response:
                        print(json.dumps(response), flush=True)
                        
                except json.JSONDecodeError:
                    error = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
                    print(json.dumps(error), flush=True)
                except Exception as e:
                    error = {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}
                    print(json.dumps(error), flush=True)
                    
        except KeyboardInterrupt:
            print("Remote client interrupted", file=sys.stderr)
        except Exception as e:
            print(f"Remote client error: {e}", file=sys.stderr)

def main():
    """Entry point"""
    try:
        client = FluidMCPRemoteClient()
        asyncio.run(client.run())
    except Exception as e:
        print(f"Failed to start client: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()