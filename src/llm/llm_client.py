# src/llm/llm_client.py

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class LLMClient:
    """
    Groq-powered LLM client.

    Used ONLY for reasoning & explanation.
    Never for deterministic decisions.
    """

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)

        # Fast + high-quality reasoning model
        self.model = "llama-3.3-70b-versatile"

    def run(self, prompt: str, task: str = "reasoning") -> str:
        """
        Execute a prompt against Groq LLM.
        """

        system_prompt = (
            "You are a senior marketing intelligence analyst. "
            "You explain customer behavior and business risk clearly, "
            "without inferring sensitive personal attributes."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,   # stable, non-random
            max_tokens=300,
        )

        return response.choices[0].message.content.strip()
