import google.generativeai as genai

from app.config import GEMINI_API_KEY


genai.configure(
    api_key=GEMINI_API_KEY
)


class LLMService:

    def __init__(self):

        self.models = [

            # Best quality
            "gemini-2.5-flash",

            # Slightly smaller version
            "gemini-2.5-flash-lite",

            # Gemini 2.0 family
            "gemini-2.0-flash",
            "gemini-2.0-flash-lite",

            # Gemini 1.5 family
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b",
            "gemini-1.5-pro"
        ]

    def generate(
        self,
        prompt
    ):

        last_exception = None

        for model_name in self.models:

            try:

                print(
                    f"\nTrying model: {model_name}"
                )

                model = genai.GenerativeModel(
                    model_name
                )

                response = model.generate_content(
                    prompt
                )

                if (
                    response
                    and hasattr(
                        response,
                        "text"
                    )
                    and response.text
                    and response.text.strip()
                ):

                    print(
                        f"Using model: {model_name}"
                    )

                    return response.text

            except Exception as e:

                error_message = str(
                    e
                ).lower()

                print(
                    f"Model {model_name} failed:"
                )
                print(e)

                last_exception = e

                if (
                    "429" in error_message
                    or "quota" in error_message
                    or "rate limit" in error_message
                    or "resource exhausted" in error_message
                ):

                    print(
                        "Quota exceeded."
                    )
                    print(
                        "Trying next model..."
                    )

                    continue

                if (
                    "not found" in error_message
                    or "unsupported" in error_message
                    or "not available" in error_message
                ):

                    print(
                        "Model unavailable."
                    )
                    print(
                        "Trying next model..."
                    )

                    continue

                continue

        raise Exception(
            f"All Gemini models failed.\n"
            f"Last error:\n{last_exception}"
        )