import os
import asyncio
import logging
from livekit.plugins.base import STTBase
from smallestai import Configuration, AtomsClient

log = logging.getLogger(__name__)

class SmallestSTT(STTBase):
    """
    LiveKit STT plugin backed by Smallest AI Atoms speech-to-text.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
    ):
        token = api_key or os.getenv("SMALLEST_API_KEY")
        self.model = model or os.getenv("SMALLEST_STT_MODEL") or "whisper-small"

        if not token:
            raise ValueError("SMALLEST_API_KEY not set")
        cfg = Configuration(access_token=token)
        self.client = AtomsClient(cfg)

    async def transcribe(self, audio_chunk: bytes, *, session_id: str | None = None, **kwargs) -> str:
        resp = await asyncio.to_thread(
            self.client.stt.transcribe,
            audio=audio_chunk,
            model=self.model,
        )
        text = resp.text
        log.debug("SmallestSTT: got transcript '%s'", text)
        return text
