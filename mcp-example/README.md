# 🧠 1 Week 1 Agent: MCP Tools - Code Runner & Web Search

This project demonstrates how to build **MCP (Model Context Protocol) servers** using [FastMCP](https://github.com/affaalfiandy/fastmcp), featuring two core tools:
- 🧪 `code_runner_server.py`: Executes Python code from prompts and saves the output.
- 🔍 `search_server.py`: Performs real-time web search using Tavily.
- 🧠 `main.py`: LangGraph agent that calls an MCP tool.

## 🚀 Setup

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/username/mcp-code-runner-agent.git
cd mcp-code-runner-agent
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

> Make sure you have Python >= 3.10 and `git` installed.

---

### 2. Run MCP Servers

#### 🔧 Code Runner MCP Server

```bash
python code_runner_server.py
```

The server will run on port `3001` using SSE transport.

#### 🌍 Web Search MCP Server (Tavily)

Create a `.env` file with your Tavily API key:

```env
TAVILY_API_KEY=your-tavily-key
```

Then run the search server:

```bash
python search_server.py
```

---

### 3. Run the LangGraph Agent

To test the agent that uses the `code_runner` tool:

```bash
python main.py
```

It will print the output of the executed Python code.

---

## 📁 Project Structure

```
.
├── code_runner_server.py   # MCP tool for executing Python code
├── search_server.py        # MCP tool for web search using Tavily
├── main.py                 # LangGraph Agent using MCP tool
├── requirements.txt        # Dependency list
└── .env                    # (Optional) for Tavily API key
```

---

## 🧠 Example Agent Interaction

Prompt inside `main.py`:
```python
{"role": "user", "content": "Create a file with the result of 100*80*71*7+87"}
```

The agent will:
- Call the `run_python_code` MCP tool
- Execute the given Python code
- Save the output to `output.txt`
- Print confirmation in the terminal

---

## ✨ Notes

- Can be extended with multi-step agents (e.g., search → run).
- You can easily add more MCP tools as needed.

