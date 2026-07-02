from groq import Groq

from app.config import (
    GROQ_API_KEY,
    GROQ_MODELS
)


class LLMService:

    def __init__(self):

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    def generate(
        self,
        prompt
    ):

        last_error = None

        for model in GROQ_MODELS:

            try:

                print(
                    f"Trying model: {model}"
                )

                response = (
                    self.client.chat.completions.create(
                        model=model,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0
                    )
                )

                print(
                    f"Using model: {model}"
                )

                return (
                    response
                    .choices[0]
                    .message
                    .content
                )

            except Exception as e:

                print(
                    f"{model} failed"
                )

                print(e)

                last_error = e

                continue

        raise Exception(
            f"All Groq models failed.\n{last_error}"
        )