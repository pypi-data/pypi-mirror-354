import os
from os import path, makedirs
from time import time 

import modal 
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from contextlib import asynccontextmanager

from typing import List, Dict, Optional, Type 
from typing import Self
from enum import Enum

from mcp4modal_sandbox.log import logger
from mcp4modal_sandbox.settings import MCPServerSettings
from mcp4modal_sandbox.backend.mcp_metadata import MCP_NAME, MCP_INSTRUCTIONS
from mcp4modal_sandbox.backend.tool_descriptions import ToolDescriptions
from mcp4modal_sandbox.backend.response_schema import (
    SandboxStatus,
    SandboxListItem,
    SandboxLaunchResponse,
    SandboxTerminateResponse,
    SandboxExecuteResponse,
    PushFileToSandboxResponse,
    PullFileFromSandboxResponse,
    SandboxListDirectoryContentsResponse,
    SandboxMakeDirectoryResponse,
    SandboxRemovePathResponse,
    SandboxReadFileContentResponse,
    SandboxWriteFileResponse,
)


class GPUType(str, Enum):
    T4 = "T4"
    L4 = "L4"
    A10G = "A10G"
    A100_40GB = "A100-40GB"
    A100_80GB = "A100-80GB"
    L40S = "L40S"
    H100 = "H100"
    H200 = "H200"
    B200 = "B200"

    @classmethod
    def get_max_gpu_count(cls, gpu_type: 'GPUType') -> int:
        if gpu_type == cls.A10G:
            return 4
        return 8

    
class MCPServer:
    def __init__(self, settings: MCPServerSettings):
        self.settings = settings

    async def run_mcp(self, transport: str = 'stdio'):
        match transport:
            case 'stdio':
                await self.mcp_app.run_async(transport=transport)
            case 'streamable-http' | 'sse':
                await self.mcp_app.run_async(transport=transport, host=self.settings.mcp_host, port=self.settings.mcp_port)
            case _:
                raise ValueError(f"Invalid transport: {transport}. Must be one of: stdio, streamable-http, sse")
        
    async def __aenter__(self) -> Self:
        self.mcp_app = FastMCP(
            name=MCP_NAME,
            instructions=MCP_INSTRUCTIONS,
            lifespan=self.lifespan
        )
        logger.info('MCPServer initialized')
        
        return self
    
    @asynccontextmanager
    async def lifespan(self, mcp_app: FastMCP):
        logger.info("MCP server is starting...")
        await self.register_tools(mcp_app)
        logger.info("MCP server is ready to accept requests, tools registered")
        yield
        logger.info("MCP server is shutting down...")
        
    async def __aexit__(self, exc_type: Optional[Type[Exception]], exc_value: Optional[Exception], traceback: Optional[str]) -> None:
        if exc_type is not None:
            logger.error(f"SandboxManager exited with exception: {exc_type} {exc_value}")
            logger.exception(traceback)
        
        logger.info('SandboxManager exited') 

    async def register_tools(self, mcp_app:FastMCP):
        mcp_app.add_tool(
            name="launch_sandbox",
            description=ToolDescriptions.LAUNCH_SANDBOX,
            fn=self.launch_sandbox
        )
        mcp_app.add_tool(
            name="terminate_sandbox",
            description=ToolDescriptions.TERMINATE_SANDBOX,
            fn=self.terminate_sandbox
        )
        mcp_app.add_tool(
            name="list_sandboxes",
            description=ToolDescriptions.LIST_SANDBOXES,
            fn=self.list_sandboxes
        )

        mcp_app.add_tool(
            name="execute_command",
            description=ToolDescriptions.EXECUTE_COMMAND,
            fn=self.execute_command
        )

        mcp_app.add_tool(
            name="push_file_to_sandbox",
            description=ToolDescriptions.PUSH_FILE_TO_SANDBOX,
            fn=self.push_file_to_sandbox
        )

        mcp_app.add_tool(
            name="pull_file_from_sandbox", 
            description=ToolDescriptions.PULL_FILE_FROM_SANDBOX,
            fn=self.pull_file_from_sandbox
        )

        mcp_app.add_tool(
            name="list_directory_contents",
            description=ToolDescriptions.LIST_DIRECTORY_CONTENTS,
            fn=self.list_directory_contents
        )

        mcp_app.add_tool(
            name="make_directory",
            description=ToolDescriptions.MAKE_DIRECTORY,
            fn=self.make_directory
        )

        mcp_app.add_tool(
            name="remove_path",
            description=ToolDescriptions.REMOVE_PATH,
            fn=self.remove_path
        )

        mcp_app.add_tool(
            name="read_file_content_from_sandbox",
            description=ToolDescriptions.READ_FILE_CONTENT_FROM_SANDBOX,
            fn=self.read_file_content_from_sandbox
        )

        mcp_app.add_tool(
            name="write_file_content_to_sandbox",
            description=ToolDescriptions.WRITE_FILE_CONTENT_TO_SANDBOX,
            fn=self.write_file_content_to_sandbox
        )


    async def list_sandboxes(self, app_name: str, ctx:Context) -> List[SandboxListItem]:
        await ctx.info(f"Listing sandboxes for app '{app_name}'...")
        app = modal.App.lookup(app_name, create_if_missing=True)
        sandbox_list: List[SandboxListItem] = []
        async for sandbox in modal.Sandbox.list.aio(app_id=app.app_id):
            sandbox_status = await sandbox.poll.aio()
            sandbox_list.append(SandboxListItem(
                sandbox_id=sandbox.object_id,
                sandbox_status=SandboxStatus.RUNNING if sandbox_status is None else SandboxStatus.STOPPED,
            ))
        await ctx.info(f"Found {len(sandbox_list)} sandboxes")
        return sandbox_list
    
    async def launch_sandbox(
        self, 
        app_name: str,
        python_version: str = "3.12",
        pip_packages: List[str] = None,
        apt_packages: List[str] = None,
        timeout_seconds: int = 600,
        cpu: float = 2.0,
        memory: int = 4096,
        secrets: Dict[str, str] = None,
        volumes: Dict[str, str] = None,
        inject_predefined_secrets:List[str] = None,
        workdir: str = "/home/solver",
        gpu_type: Optional[GPUType] = None,
        gpu_count: Optional[int] = None,
    ) -> SandboxLaunchResponse:
        pip_packages = pip_packages or []
        apt_packages = apt_packages or []
        secrets = secrets or {}
        inject_predefined_secrets = inject_predefined_secrets or []
        # Build the image with Python version and dependencies
        image = modal.Image.debian_slim(python_version=python_version)
        
        # Install system dependencies
        if apt_packages:
            image = image.apt_install(*apt_packages)
        
        # Install Python packages
        if pip_packages:
            image = image.pip_install(*pip_packages)
        
        # Create secrets for environment variables (the proper Modal way)
        modal_secrets = []
        if secrets:
            secret = modal.Secret.from_dict(secrets)
            modal_secrets.append(secret)
        
        if inject_predefined_secrets:
            for secret_name in inject_predefined_secrets:
                secret = modal.Secret.from_name(secret_name)
                modal_secrets.append(secret)
        
        modal_volumes = {}
        if volumes:
            for volume_path, volume_name in volumes.items():
                modal_volumes[volume_path] = modal.Volume.from_name(volume_name, create_if_missing=True)
        
        # Configure GPU if specified
        gpu = None
        if gpu_type:
            if gpu_count:
                max_gpus = GPUType.get_max_gpu_count(gpu_type)
                if gpu_count > max_gpus:
                    raise ToolError(f"{gpu_type.value} supports up to {max_gpus} GPUs")
                gpu = f"{gpu_type.value}:{gpu_count}"
            else:
                gpu = gpu_type.value
        
        # Get or create Modal app for the specified namespace
        app = modal.App.lookup(app_name, create_if_missing=True)
        
        # Create sandbox with Modal
        with modal.enable_output():
            logger.info(f"Creating sandbox with Python {python_version} in app '{app_name}'" + (f" and GPU {gpu}" if gpu else ""))
            sandbox = await modal.Sandbox.create.aio(
                "/bin/bash",
                image=image,
                app=app,
                timeout=timeout_seconds,
                cpu=cpu,
                memory=memory,
                secrets=modal_secrets,
                volumes=modal_volumes,
                workdir=workdir,
                gpu=gpu
            )
            
        # Get the Modal-assigned ID
        sandbox_id = sandbox.object_id
        
        logger.info(f"Launched sandbox {sandbox_id} with Python {python_version}")
        
        return SandboxLaunchResponse(
            sandbox_id=sandbox_id,
            status="running",
            python_version=python_version,
            pip_packages=pip_packages,
            apt_packages=apt_packages,
        )
    

    async def terminate_sandbox(self, sandbox_id: str, ctx:Context) -> SandboxTerminateResponse:
        # Get sandbox from Modal using from_id
        modal_sandbox = await modal.Sandbox.from_id.aio(sandbox_id)

        # Check if sandbox is running before terminating
        sandbox_status = await modal_sandbox.poll.aio()
        
        # Terminate the Modal sandbox
        if sandbox_status is not None:
            return SandboxTerminateResponse(
                success=False,
                message=f"Sandbox {sandbox_id} is not running"
            )
        
        await modal_sandbox.terminate.aio()
        
        # Wait for termination
        await modal_sandbox.wait.aio(raise_on_termination=False)
        
        logger.info(f"Terminated sandbox {sandbox_id}")
        
        return SandboxTerminateResponse(
            success=True,
            message=f"Sandbox {sandbox_id} terminated successfully"
        )
    

    async def execute_command(
        self,
        sandbox_id: str, 
        command: List[str],
        timeout_seconds: int = 30
    ) -> SandboxExecuteResponse:
        # Get sandbox from Modal using from_id
        modal_sandbox = await modal.Sandbox.from_id.aio(sandbox_id)
        
        # Check if sandbox is running before executing command
        sandbox_status = await modal_sandbox.poll.aio()
        if sandbox_status is not None:
            raise ToolError(f"Sandbox {sandbox_id} is not running")
        
        start_time = time()
        
        result = await modal_sandbox.exec.aio(*command, timeout=timeout_seconds)
        await result.wait.aio()
        
        execution_time = time() - start_time
        # Get output from the sandbox
        stdout = result.stdout.read() if result.stdout else ""
        stderr = result.stderr.read() if result.stderr else ""
        returncode = result.returncode
        
        logger.info(f"Executed command in sandbox {sandbox_id}: {' '.join(command)}")
        
        return SandboxExecuteResponse(
            stdout=stdout,
            stderr=stderr,
            returncode=returncode,
            execution_time=execution_time
        )

    async def push_file_to_sandbox(
        self, 
        sandbox_id: str, 
        local_path: str, 
        sandbox_path: str,
        read_file_mode: str = "rb",
        writefile_mode: str = "wb"
    ) -> PushFileToSandboxResponse:
        # Get sandbox from Modal using from_id
        modal_sandbox = await modal.Sandbox.from_id.aio(sandbox_id)
        
        # Check if sandbox is running before copying file
        sandbox_status = await modal_sandbox.poll.aio()
        if sandbox_status is not None:
            raise ToolError(f"Sandbox {sandbox_id} is not running")
        
        if not path.exists(local_path):
            raise ToolError(f"Local file {local_path} does not exist")
        
        # Get file size
        file_size = os.path.getsize(local_path)
        
        # Read local file
        with open(local_path, read_file_mode) as file_pointer:
            content = file_pointer.read()
        
        # Write to sandbox
        file_ctm = await modal_sandbox.open.aio(sandbox_path, writefile_mode)
        with file_ctm as file_pointer:
            file_pointer.write(content)
        
        logger.info(f"Copied file from {local_path} to {sandbox_path} in sandbox {sandbox_id}")
        
        return PushFileToSandboxResponse(
            success=True,
            message=f"File copied successfully to {sandbox_path}",
            local_path=local_path,
            sandbox_path=sandbox_path,
            file_size=file_size,
        )

    async def list_directory_contents(self, sandbox_id: str, path: str) -> SandboxListDirectoryContentsResponse:
        # Get sandbox from Modal using from_id
        modal_sandbox = await modal.Sandbox.from_id.aio(sandbox_id)
        
        # Check if sandbox is running before listing directory
        sandbox_status = await modal_sandbox.poll.aio()
        if sandbox_status is not None:
            raise ToolError(f"Sandbox {sandbox_id} is not running")
        
        contents = await modal_sandbox.ls.aio(path)
        logger.info(f"Listed directory {path} in sandbox {sandbox_id}")
        
        return SandboxListDirectoryContentsResponse(
            contents=contents
        )

    async def make_directory(self, sandbox_id: str, path: str, parents: bool = False) -> SandboxMakeDirectoryResponse:
        # Get sandbox from Modal using from_id
        modal_sandbox = await modal.Sandbox.from_id.aio(sandbox_id)
    
        # Check if sandbox is running before creating directory
        sandbox_status = await modal_sandbox.poll.aio()
        if sandbox_status is not None:
            raise ToolError(f"Sandbox {sandbox_id} is not running")
        
        await modal_sandbox.mkdir.aio(path, parents=parents)
        logger.info(f"Created directory {path} in sandbox {sandbox_id}")
        
        return SandboxMakeDirectoryResponse(
            success=True,
            message=f"Directory {path} created successfully",
            path_created=path,
        )

    async def remove_path(self, sandbox_id: str, path: str, recursive: bool = False) -> SandboxRemovePathResponse:
        # Get sandbox from Modal using from_id
        modal_sandbox = await modal.Sandbox.from_id.aio(sandbox_id)    
        await modal_sandbox.rm.aio(path, recursive=recursive)
        
        logger.info(f"Removed path {path} in sandbox {sandbox_id}")
        
        return SandboxRemovePathResponse(
            success=True,
            message=f"Path {path} removed successfully",
            path_removed=path,
        )

    async def pull_file_from_sandbox(
        self, 
        sandbox_id: str, 
        sandbox_path: str, 
        local_path: str
    ) -> PullFileFromSandboxResponse:
        # Get sandbox from Modal using from_id
        modal_sandbox = await modal.Sandbox.from_id.aio(sandbox_id)
    
        # Check if sandbox is running before copying file from sandbox
        sandbox_status = await modal_sandbox.poll.aio()
        if sandbox_status is not None:
            raise ToolError(f"Sandbox {sandbox_id} is not running")
        
        # Read from sandbox
        file_ctm = await modal_sandbox.open.aio(sandbox_path, 'rb')
        with file_ctm as file_pointer:
            content = file_pointer.read()
        
        file_size = len(content)
        
        # Write to local file
        makedirs(path.dirname(local_path), exist_ok=True)
        with open(local_path, 'wb') as file_pointer:
            file_pointer.write(content)
        
        logger.info(f"Copied file from {sandbox_path} to {local_path} from sandbox {sandbox_id}")
        
        return PullFileFromSandboxResponse(
            success=True,
            message=f"File copied successfully to {local_path}",
            file_size=file_size,
            sandbox_path=sandbox_path,
            local_path=local_path,
        )

    async def read_file_content_from_sandbox(self, sandbox_id: str, path: str) -> SandboxReadFileContentResponse:
        # Get sandbox from Modal using from_id
        modal_sandbox = await modal.Sandbox.from_id.aio(sandbox_id)
        
        # Check if sandbox is running before reading file
        sandbox_status = await modal_sandbox.poll.aio()
        if sandbox_status is not None:
            raise ToolError(f"Sandbox {sandbox_id} is not running")
        
        # Read from sandbox
        file_ctm = await modal_sandbox.open.aio(path, 'rb')
        with file_ctm as file_pointer:
            content = file_pointer.read()
        
        logger.info(f"Read file content from {path} in sandbox {sandbox_id}")
        
        return SandboxReadFileContentResponse(
            content=content
        )
    
    async def write_file_content_to_sandbox(
            self, 
            sandbox_id:str, 
            sandbox_path:str,
            content:str,
            ) -> SandboxWriteFileResponse:
        sandbox = await modal.Sandbox.from_id.aio(sandbox_id)
        sandbox_status = await sandbox.poll.aio()
        if sandbox_status is not None:
            raise ToolError(f"Sandbox {sandbox_id} is not running")
        
        file_ctm = await sandbox.open.aio(sandbox_path, "w")
        with file_ctm as file_pointer:
            file_pointer.write(content)

        logger.info(f"Content written successfully to {sandbox_path}")

        return SandboxWriteFileResponse(
            success=True,
            message=f"Content written successfully to {sandbox_path}",
            file_path=sandbox_path,
        )
        