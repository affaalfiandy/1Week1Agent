# code_runner_mcp_server.py

import os
from fastmcp import FastMCP

# Init FastMCP Server
mcp = FastMCP("PythonCodeRunner")

@mcp.tool()
async def run_python_code(code: str, filename: str = "output.txt") -> str:
    """
    Menjalankan kode Python dan menyimpan output ke file .txt.
    """
    try:
        # Gunakan context dictionary untuk output exec
        context = {}

        # Tangkap hasil print
        import io
        import contextlib

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(code, context)

        # Tulis ke file
        result = output.getvalue()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result)

        return f"Kode berhasil dijalankan dan output disimpan di {filename}"
    except Exception as e:
        return f"Terjadi error saat menjalankan kode: {str(e)}"

# === Run MCP Server ===
if __name__ == "__main__":
    mcp.run(transport="sse", port=3001)

