import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL"),
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )