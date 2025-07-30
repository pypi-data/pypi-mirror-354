from typing import Optional
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm(response_model: Optional[type] = None):

    api_key = os.getenv("GOOGLE_API_KEY", None)
    if not api_key:
        raise ValueError("Missing GOOGLE_API_KEY")

    google_model = "gemini-2.0-flash"
    client = genai.Client(api_key=api_key)

    def generate(prompt: str, file_path: Optional[str] = None):
        """
        wrapper for generate_content

        Args:
            prompt: str           -> normal prompt
            file_path: str | None -> file path

        Examples:

            **Text**
            ```python
            response = generate("Who is oggy?")
            ```

            **Vision**
            ```python
            response = generate("what is oggy doing in this?", "image.png")
            ```
        """

        if file_path:
            f = client.files.upload(file=file_path)
            content = [f, prompt]
        else:
            content = prompt

        if response_model:
            config = {
                "response_mime_type": "application/json",
                "response_schema": response_model,
            }
        else:
            config = None

        response = client.models.generate_content(
            model=google_model, contents=content, config=config
        )
        return response

    return generate
