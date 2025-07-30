import logging

from mcp_server_hatena_weekly.server import mcp


def main():
    """
    Hatena Bookmark Weekly/Monthly Ranking Server - Model Context Protocol server
    for fetching Hatena bookmark ranking data

    This server provides access to Hatena bookmark ranking data for 2025 (January-May).

    Available features:
    1. weekly: Get weekly Hatena bookmark ranking data (30 entries)
    2. monthly: Get monthly Hatena bookmark ranking data (50 entries)
    """
    import argparse

    # Command line argument configuration
    parser = argparse.ArgumentParser(
        description="Start the Hatena Bookmark Weekly/Monthly Ranking server. "
        "Fetch ranking data from pre-scraped Hatena bookmark rankings."
    )
    parser.add_argument(
        "--sse",
        choices=["on", "off"],
        default="off",
        help='Enable SSE transport when set to "on"',
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host to bind the server to (default: localhost)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the server to (default: 8000)",
    )
    parser.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error"],
        default="info",
        help="Set logging level:\n"
        "  debug: Detailed debug information\n"
        "  info: General execution information (default)\n"
        "  warning: Potential issues that do not affect execution\n"
        "  error: Errors that occur during execution",
    )
    args = parser.parse_args()

    # Map string log levels to logging constants
    log_level_map = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
    }

    log_level = log_level_map.get(args.log_level, logging.INFO)
    if args.log_level not in log_level_map:
        raise ValueError(
            f"Invalid log level: {args.log_level}. Choose from {list(log_level_map.keys())}."
        )

    # Configure logging based on command line argument
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Run server with configured arguments
    if args.sse == "on":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
