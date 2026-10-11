"""Stdio MCP server exposing tools for the local math text files."""

from pathlib import Path

from mcp.server.fastmcp import FastMCP

MCP_DIR = Path(__file__).resolve().parent

mcp = FastMCP("agentic-math-files")


@mcp.tool()
def list_math_files() -> str:
    """List available .txt files in the MCP folder."""
    names = sorted(p.name for p in MCP_DIR.glob("*.txt"))
    return "\n".join(names) if names else "No .txt files found."


@mcp.tool()
def read_math_file(filename: str) -> str:
    """Read a math text file by name (e.g. hello.txt, hi.txt)."""
    path = (MCP_DIR / filename).resolve()
    if MCP_DIR not in path.parents and path != MCP_DIR:
        return f"Invalid path: {filename}"
    if not path.is_file() or path.suffix != ".txt":
        return f"File not found: {filename}"
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run(transport="stdio")
