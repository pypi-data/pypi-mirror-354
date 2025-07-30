from mcp_adapter.core.server_base import McpServerAdapterBase


class MockMcpServerSse(McpServerAdapterBase):

    name = 'MockMcpServerSse'

    description = 'MockMcpServerSse Service'

    transport = 'sse'

    @staticmethod
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        return a + b

    @staticmethod
    def sub(a: int, b: int) -> int:
        """Sub two numbers"""
        return a - b

    @staticmethod
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers"""
        return a * b


class MockMcpServerHttpStreamable(McpServerAdapterBase):

    name = 'MockMcpServerHttpStreamable'

    description = 'MockMcpServerHttpStreamable Service'

    transport = 'streamable_http'

    @staticmethod
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        return a + b

    @staticmethod
    def sub(a: int, b: int) -> int:
        """Sub two numbers"""
        return a - b

    @staticmethod
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers"""
        return a * b
