# livekit_smallestai/llm_groq.py
import os, asyncio, logging
from livekit.plugins.base import LLMBase
from groq import Groq            # ← official SDK

log = logging.getLogger(__name__)

class GroqLLM(LLMBase):
    def __init__(self, *, api_key: str | None = None,
                 model: str | None = None, timeout: float = 60.0):
        token = api_key or os.getenv("GROQ_API_KEY")
        if not token:
            raise ValueError("GROQ_API_KEY not set")
        self.client = Groq(api_key=token, timeout=timeout)
        self.model = model or os.getenv("GROQ_MODEL") or "llama-3.3-70b-versatile"

    async def chat(self, messages: list[dict], **kw) -> str:
        # delegate to Groq’s OpenAI-compatible endpoint
        resp = await asyncio.to_thread(
            self.client.chat.completions.create,
            model=self.model,
            messages=messages,
            max_tokens=kw.get("max_tokens", 512),
            temperature=kw.get("temperature", 0.7),
        )
        return resp.choices[0].message.content.strip()
