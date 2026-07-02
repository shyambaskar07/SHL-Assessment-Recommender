from dotenv import load_dotenv
import os

load_dotenv()

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)

TOP_K = int(
    os.getenv(
        "TOP_K",
        10
    )
)

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

GROQ_MODELS = [

    "llama-3.3-70b-versatile",

    "llama-3.1-8b-instant",

    "gemma2-9b-it",

    "llama3-8b-8192",

    "gemma-7b-it"
]