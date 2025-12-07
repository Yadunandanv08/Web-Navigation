import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from contextlib import AsyncExitStack
from dotenv import load_dotenv
import os

load_dotenv()
MCP_SSE_URL = os.getenv("MCP_SSE_URL")

class PlaywrightConnection:

    def __init__(self, url=MCP_SSE_URL):
        self.url = url
        self.session = None
        self.exit_stack = None

    async def connect(self):

        self.exit_stack = AsyncExitStack()

        # Open SSE streams
        streams = await self.exit_stack.enter_async_context(sse_client(self.url))
        read_stream, write_stream = streams

        # Initialize MCP session
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        await self.session.initialize()
        return self

    async def close(self):
        """Close session"""
        if self.exit_stack:
            await self.exit_stack.aclose()

    def get_session(self):
        """
        Returns the MCP session for calling tools.
        """
        if not self.session:
            raise ConnectionError("MCP session not initialized. Call connect() first.")
        return self.session

def start_connection(url=MCP_SSE_URL):
    
    return asyncio.run(PlaywrightConnection(url).connect())

