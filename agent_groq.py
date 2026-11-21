import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient

load_dotenv()

# --- 1. SETUP CLIENTS ---
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

MODEL_NAME = "openai/gpt-oss-120b" # From your check_models.py output

# --- 2. DEFINE YOUR LOCAL TOOLS ---
def calculator(expression: str) -> str:
    """Calculates mathematical expressions."""
    try:
        print(f"   [Tool Call] Calculator: {expression}")
        result = eval(expression)
        print(f"   [Tool Result] {result}")
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def web_search(query: str) -> str:
    """Searches the internet for current information using Tavily."""
    try:
        print(f"   [Tool Call] Tavily Search: {query}")
        response = tavily_client.search(query, max_results=3)
        
        results = response.get("results", [])
        if not results:
            print("   [Tool Result] No results found.")
            return "No results found."
            
        formatted_results = "\n".join([f"- {r['content']}" for r in results])
        print(f"   [Tool Result] Found {len(results)} snippets.")
        return formatted_results
    except Exception as e:
        print(f"   [Tool Error] {e}")
        return f"Search failed: {e}"

# --- 3. DESCRIBE TOOLS FOR THE MODEL ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculates mathematical expressions. Use for any math.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "A Python math string, e.g., '100 * 83.50'"}
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Searches the internet for current exchange rates, news, or facts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query string."}
                },
                "required": ["query"],
            },
        },
    },
]

# --- 4. THE AGENT LOOP ---
print(f"🤖 Groq ({MODEL_NAME}) + Tavily Agent is ready! (Type 'quit' to exit)")
print("Try: 'What is the USD to INR rate? Convert $250 to INR.'")

messages = []

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'quit':
        break

    messages.append({"role": "user", "content": user_input})
    print("\nAgent: ", end="", flush=True)

    try:
        # THE FIX: A loop that allows the agent to use multiple tools in a row
        while True:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )
            
            response_message = response.choices[0].message
            messages.append(response_message) 

            # If the model wants to use a tool, execute it and loop again
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    if function_name == "calculator":
                        tool_result = calculator(function_args["expression"])
                    elif function_name == "web_search":
                        tool_result = web_search(function_args["query"])
                    else:
                        tool_result = f"Unknown tool: {function_name}"
                    
                    # Append the tool's result to the conversation
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result,
                    })
                # The 'while True' loop will now call the API again with the tool results
                
            else:
                # If there are no tool calls, it's the final answer!
                print(response_message.content)
                messages.append({"role": "assistant", "content": response_message.content})
                break # Exit the inner loop, wait for next user input
                
    except Exception as e:
        print(f"\nError: {e}")
        messages.pop() 