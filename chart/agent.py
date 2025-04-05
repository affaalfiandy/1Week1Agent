from langchain.agents import initialize_agent, AgentType
from langchain_core.messages import SystemMessage
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import os
import sys
import traceback
from io import StringIO
import textwrap
import re

# Function: Load and summarize dataset
def retrieve_data(query=None):
    try:
        df = pd.read_csv("data.csv")
        summary = {
            "columns": df.columns.tolist(),
            "data_types": df.dtypes.apply(lambda x: str(x)).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "num_rows": len(df)
        }
        return f"Dataset Summary:\n{summary}"
    except FileNotFoundError:
        return "Error: 'data.csv' not found. Ensure the file is in the root directory."

# Python REPL tool (improved to handle various code formatting issues)
def python_repl(code):
    import matplotlib
    matplotlib.use('Agg')  # Safe backend
    from PIL import Image, ImageDraw, ImageFont

    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    try:
        # Clean up code by removing markdown formatting
        clean_code = code.strip()
        
        # Remove markdown code block syntax if present
        if clean_code.startswith("```python"):
            clean_code = clean_code[9:]
        elif clean_code.startswith("```"):
            clean_code = clean_code[3:]
            
        # Remove closing code block markers
        if clean_code.endswith("```"):
            clean_code = clean_code[:-3]
            
        # Remove "python" prefix if it exists
        if clean_code.startswith("python "):
            clean_code = clean_code[7:]
            
        # Strip any remaining backticks
        clean_code = clean_code.strip("`").strip()
        
        # Ensure matplotlib imports are present for plotting
        if "matplotlib.pyplot" in clean_code and "matplotlib.use('Agg')" not in clean_code:
            clean_code = "import matplotlib\nmatplotlib.use('Agg')\n" + clean_code
            
        # Dedent code to handle indentation
        dedented_code = textwrap.dedent(clean_code)
        
        # Debug info (can be removed in production)
        print(f"Executing code:\n{dedented_code}\n---")
        
        # Execute the code
        exec(compile(dedented_code, "<string>", "exec"), globals())
        sys.stdout = old_stdout
        return mystdout.getvalue()
    except Exception as e:
        sys.stdout = old_stdout
        return f"Error: {str(e)}\n{traceback.format_exc()}"

# Define tools
retrieve_data_tool = Tool(
    name="RetrieveData",
    func=retrieve_data,
    description="Loads 'data.csv' and provides an overview of its columns, data types, missing values, and row count."
)

python_repl_tool = Tool(
    name="PythonREPL",
    func=python_repl,
    description="A Python REPL. Use this to execute Python commands. Input should be a valid Python command. Do not use markdown code blocks or shell commands."
)

# Enhanced system prompt with improved instructions and examples
system_prompt = """You are a chart generator agent with expertise in data storytelling that will generate and save charts as PNG files (IMPORTANT: MAKE THEM COLORFUL).

Process:
1. Retrieve and analyze 'data.csv' using the RetrieveData tool.
2. Determine the best chart types based on the dataset and insights available.
3. Generate multiple charts if necessary and ALWAYS save them as separate PNG files.
4. At the end, combine all charts into a single image called 'final_chart.png' using a horizontal or grid layout.
5. Provide a single combined data analysis summary at the bottom of the final image.

Critical Instructions:
1. NEVER use plt.show() or any display functions.
2. ALWAYS start any plotting code with appropriate matplotlib configuration:
   import matplotlib
   matplotlib.use('Agg')
   import matplotlib.pyplot as plt
   
3. ALWAYS save each chart with a descriptive name like 'chart_1_rating_by_year.png'.
4. When combining charts, use PIL to create a grid layout (2x2 or 3x1 depending on number of charts).
5. Add a text summary using PIL.ImageDraw with insights about the data.
6. After 'final_chart.png' is created, DELETE all individual chart files.
7. NEVER submit code with triple backticks (```). Just write the Python code directly.
8. NEVER use "python" as a prefix to your code - write pure Python code only.
9. For long code blocks, break them into smaller, manageable pieces.
10. If a chart operation fails, try a simpler approach.

Example of correct code format:
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 5))
plt.plot(x, y)
plt.title('My Chart')
plt.savefig('chart_1.png')
plt.close()

Important: All code executed by the PythonREPL tool will be run in the same session, so variables defined in one action will be available in subsequent actions.
"""

# Load API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not found. Please set it in your .env file.")

# Initialize LLM with a more sophisticated model if available
llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)

# Create the agent
tools = [retrieve_data_tool, python_repl_tool]

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={
        "system_message": SystemMessage(content=system_prompt),
        "early_stopping_method": "generate",  # Helps prevent incomplete executions
    }
)

# Enhanced prompt for better chart generation
chart_prompt = """
Create a suitable chart based on the dataset and provide insights for me. Follow these steps:

1. First, load and examine the data to understand its structure.
2. Generate at least 3 different charts that best visualize interesting aspects of the data.
3. Make sure to save each chart as a separate PNG file with descriptive names.
4. After creating the charts, combine them into a single image called 'final_chart.png'.
5. Add a text section at the bottom of the final image summarizing key insights.
6. Use bright, visually appealing colors and ensure all text is readable.
7. Make the final image compact but comprehensive.

Focus on creating insightful visualizations rather than complex code.
"""

# Run the agent
result = agent_executor.invoke({"input": chart_prompt})

print(result)