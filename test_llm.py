import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    max_retries=0,   # raise immediately instead of retrying silently
    timeout=30,
)
print(llm.invoke("Say hi in one word").content)