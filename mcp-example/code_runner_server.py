from fastmcp import FastMCP
from langchain_experimental.utilities import PythonREPL
import os

# Initialize FastMCP Server with the name "PythonCodeRunner"
mcp = FastMCP("PythonCodeRunner")

# Initialize Python REPL once to maintain execution state across multiple calls
repl = PythonREPL()

@mcp.tool()
async def run_python_code(code_input: str, filename: str = None) -> str:
    """
    Executes Python code using LangChain's PythonREPL.
    If `filename` is provided, the output will be saved to that file.

    Args:
        code_input (str): The Python code to be executed.
        filename (str, optional): Name of the file to save output (if any).

    Returns:
        str: The execution result or success message with file path.
    """
    try:
        # Execute code using Python REPL
        result = repl.run(code_input)

        # Save to file if filename is specified
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result)
            return f"Code executed successfully. Output saved to {filename}"
        else:
            return result

    except Exception as e:
        # Return any execution error
        return f"Error while executing code: {str(e)}"

# === Start the MCP Server using SSE transport on port 3001 ===
if __name__ == "__main__":
    mcp.run(transport="sse", port=3001)
