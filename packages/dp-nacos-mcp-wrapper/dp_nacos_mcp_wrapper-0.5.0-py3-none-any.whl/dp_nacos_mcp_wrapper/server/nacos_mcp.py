import logging
from typing import Any

import uvicorn
from mcp import stdio_server
from mcp.server import FastMCP
from mcp.server.fastmcp.server import lifespan_wrapper
from mcp.server.lowlevel.server import lifespan as default_lifespan

from deepbank_nacos_mcp_wrapper.server.nacos_server import NacosServer
from deepbank_nacos_mcp_wrapper.server.nacos_settings import NacosSettings

logger = logging.getLogger(__name__)

class NacosMCP(FastMCP):

	def __init__(self,
			name: str | None = None,
			nacos_settings: NacosSettings | None = None,
			instructions: str | None = None,
			**settings: Any):
		super().__init__(name, instructions, **settings)

		self._mcp_server = NacosServer(
				nacos_settings=nacos_settings,
				name=name or "FastMCP",
				instructions=instructions,
				lifespan=lifespan_wrapper(self, self.settings.lifespan)
				if self.settings.lifespan
				else default_lifespan,
		)
		self.dependencies = self.settings.dependencies

		# Set up MCP protocol handlers
		self._setup_handlers()

	async def run_stdio_async(self) -> None:
		"""Run the server using stdio transport."""
		async with stdio_server() as (read_stream, write_stream):
			await self._mcp_server.register_to_nacos("stdio")
			await self._mcp_server.run(
					read_stream,
					write_stream,
					self._mcp_server.create_initialization_options(),
			)

	async def run_sse_async(self) -> None:
		"""Run the server using SSE transport."""
		starlette_app = self.sse_app()
		await self._mcp_server.register_to_nacos("sse", self.settings.port, self.settings.sse_path)
		config = uvicorn.Config(
				starlette_app,
				host=self.settings.host,
				port=self.settings.port,
				log_level=self.settings.log_level.lower(),
		)
		server = uvicorn.Server(config)
		await server.serve()

	async def run_streamable_http_async(self) -> None:
		"""Run the server using SSE transport."""
		starlette_app = self.streamable_http_app()
		await self._mcp_server.register_to_nacos("streamable_http", self.settings.port, self.settings.streamable_http_path)
		config = uvicorn.Config(
				starlette_app,
				host=self.settings.host,
				port=self.settings.port,
				log_level=self.settings.log_level.lower(),
		)
		server = uvicorn.Server(config)
		await server.serve()