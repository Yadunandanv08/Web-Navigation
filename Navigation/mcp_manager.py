import threading
import asyncio
import os
import sys
from mcp import ClientSession
from mcp.client.sse import sse_client
from contextlib import AsyncExitStack
from dotenv import load_dotenv

load_dotenv()

class MCPSessionKeeper:
    _instance = None
    
    def __init__(self):
        self.loop = None
        self.thread = None
        self.session = None
        self.exit_stack = None
        # Use the URL from env, default to localhost:8931
        self.mcp_url = os.getenv("MCP_SSE_URL")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = MCPSessionKeeper()
        return cls._instance

    def start(self):
        """
        Starts the background thread and connects to the EXISTING server.
        """
        if self.thread and self.thread.is_alive():
            return # Already running

        print(f"--- 🔌 Connecting to MCP Server at {self.mcp_url} ---")

        # 1. Start the Background Loop in a separate thread
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_loop, args=(self.loop,), daemon=True)
        self.thread.start()

        # 2. Connect to the server (running on the background loop)
        try:
            future = asyncio.run_coroutine_threadsafe(self._connect(), self.loop)
            future.result(timeout=10) # Wait up to 10s for connection
        except Exception as e:
            print(f"Could not connect to MCP Server. Is 'run_server.py' running?")
            raise e

    def _run_loop(self, loop):
        """The infinite loop that keeps the connection alive."""
        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def _connect(self):
        """Internal async method to establish connection."""
        self.exit_stack = AsyncExitStack()
        # Connect via SSE
        streams = await self.exit_stack.enter_async_context(sse_client(self.mcp_url))
        self.session = await self.exit_stack.enter_async_context(ClientSession(streams[0], streams[1]))
        await self.session.initialize()
        print("--- Connected to Browser Session (Persistent) ---")

    def call_tool(self, tool_name, arguments):
        """
        Thread-safe method for the Agent to call.
        """
        if not self.loop or not self.session:
            # Auto-start if they forgot to call start()
            self.start()

        # Define the work to be done on the background loop
        async def _work():
            return await self.session.call_tool(tool_name, arguments)

        # Submit work and wait for the result
        future = asyncio.run_coroutine_threadsafe(_work(), self.loop)
        return future.result()

    def stop(self):
        """Clean shutdown of the connection."""
        print("--- Closing Connection ---")
        if self.loop and self.exit_stack:
            asyncio.run_coroutine_threadsafe(self.exit_stack.aclose(), self.loop).result()
        
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)