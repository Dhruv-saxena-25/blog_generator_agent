from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq


def get_llm(provider: str, model: str, api_key: str):
    if provider == "OpenAI":
        return ChatOpenAI(model=model, temperature=0.7, openai_api_key=api_key)
    
    elif provider == "Groq":
        return ChatGroq(model=model, temperature=0.7, groq_api_key=api_key)
    
    elif provider == "Gemini":
        return ChatGoogleGenerativeAI(model=model, temperature=0.7, google_api_key=api_key)
    
    else:
        raise ValueError(f"Unsupported provider: {provider}")