import os


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b"
]


MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "openai/gpt-oss-120b"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)

TOP_K = int(
    os.getenv(
        "TOP_K",
        "10"
    )
)
