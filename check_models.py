import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

print("Available models on your Groq account:\n")
try:
    models = client.models.list()
    for m in models.data:
        # We filter for models that are generally good at tool calling
        print(m.id)
except Exception as e:
    print(f"Error fetching models: {e}")