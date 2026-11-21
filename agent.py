import ast
import operator as op
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

# Let the Gemini route keep working with the key name you already use.
if os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

# ---------- Tools ----------
_OPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression, e.g. '100 * 83.5'."""
    try:
        return str(_eval(ast.parse(expression, mode="eval").body))
    except Exception as e:
        return f"Error calculating: {e}"


@tool
def web_search(query: str) -> str:
    """Search for current exchange rates, facts, or news."""
    if "usd" in query.lower() or "inr" in query.lower():
        return "MOCK DATA: 1 USD is approximately 83.50 INR."
    return "Mock search result: The requested information is available."


# ---------- Model (swap provider by editing LLM in .env) ----------
# Examples:
#   LLM=groq:qwen/qwen3-32b            (needs GROQ_API_KEY, pip install langchain-groq)
#   LLM=ollama:qwen3:8b                (local, pip install langchain-ollama)
#   LLM=google_genai:gemini-2.5-flash  (needs GEMINI_API_KEY, pip install langchain-google-genai)
MODEL_NAME = os.getenv("LLM", "groq:qwen/qwen3-32b")

llm = init_chat_model(
    MODEL_NAME,
    temperature=0,
    max_retries=1,   # fail fast instead of looking like a hang
    timeout=30,
)

agent = create_agent(
    model=llm,
    tools=[calculator, web_search],
    system_prompt="You are a helpful financial assistant. Always use the calculator for math.",
    checkpointer=InMemorySaver(),
)


def text_of(content):
    """Some providers return a list of content blocks instead of a string."""
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") for b in content if isinstance(b, dict))


# ---------- Chat loop ----------
config = {"configurable": {"thread_id": "chat-1"}}
print(f"Using model: {MODEL_NAME}  (type 'quit' to exit)")

while True:
    user_input = input("\nYou: ")
    if user_input.strip().lower() == "quit":
        break
    print("\nAgent: ", end="", flush=True)
    try:
        for chunk in agent.stream(
            {"messages": [("user", user_input)]}, config, stream_mode="updates"
        ):
            for node, values in chunk.items():
                for msg in values.get("messages", []):
                    if getattr(msg, "tool_calls", None):
                        for tc in msg.tool_calls:
                            print(f"\n   [Using Tool: {tc['name']} {tc['args']}]")
                    elif msg.type == "tool":
                        print(f"   [Tool Result: {str(msg.content)[:100]}]")
                    elif msg.type == "ai":
                        print(text_of(msg.content), end="", flush=True)
        print()
    except Exception as e:
        print(f"\nError: {type(e).__name__}: {e}")