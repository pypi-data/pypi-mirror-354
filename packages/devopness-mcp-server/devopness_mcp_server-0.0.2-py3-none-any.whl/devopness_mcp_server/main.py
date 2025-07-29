from .server import server


def run() -> None:
    """
    Start the Devopness MCP Server.

    This is the main entry-point for the MCP server.

    It sets up the server, registers the tools and then starts the server.
    """
    # TODO: Use a logger instead of default print
    print("🚀 Starting Devopness MCP Server...")

    server.run()

    # TODO: Use a logger instead of default print
    print("🚀 Devopness MCP Server stopped.")


if __name__ == "__main__":
    run()
