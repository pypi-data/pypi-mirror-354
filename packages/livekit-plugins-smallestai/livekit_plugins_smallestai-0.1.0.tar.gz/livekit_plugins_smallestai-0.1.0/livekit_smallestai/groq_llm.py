# livekit_smallestai/llm_groq.py

import os, asyncio, logging
from livekit.plugins.base import LLMBase
from groq_client import GroqClient, CompletionRequest

log = logging.getLogger(__name__)

class GroqLLM(LLMBase):
    """
    LiveKit LLM plugin backed by Groq Cloud.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        timeout: float = 60.0
    ):
        token = api_key or os.getenv("GROQ_API_KEY")
        if not token:
            raise ValueError("GROQ_API_KEY not set")
        self.client = GroqClient(api_key=token, timeout=timeout)
        self.model = model or os.getenv("GROQ_MODEL") or "llama-3.3-70b-versatile"

    async def chat(self, messages: list[dict], **kwargs) -> str:
        """
        messages: list of {"role": "user"|"assistant", "content": str}
        """
        # assemble prompt
        prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            # simple role tags; adjust per your conventions
            prompt += f"<|{role}|> {content}\n"
        req = CompletionRequest(
            model=self.model,
            prompt=prompt,
            max_tokens=kwargs.get("max_tokens", 512),
            temperature=kwargs.get("temperature", 0.7)
        )
        # wrap sync call
        resp = await asyncio.to_thread(self.client.complete, req)
        text = resp.choices[0].text.strip()
        log.debug("GroqLLM: response `%s`", text)
        return text