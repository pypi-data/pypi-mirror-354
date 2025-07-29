import os
import asyncio
import logging
from livekit.plugins.base import TTSBase
from smallestai import Configuration, AtomsClient

log = logging.getLogger(__name__)

class SmallestTTS(TTSBase):
    """
    LiveKit TTS plugin backed by Smallest AI Atoms Waves.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        voice: str | None = None,
    ):
        # Priority: constructor args → .env overrides → hard-coded defaults
        token = api_key or os.getenv("SMALLEST_API_KEY")
        self.model = model or os.getenv("SMALLEST_TTS_MODEL") or "waves-v2"
        self.voice = voice or os.getenv("SMALLEST_TTS_VOICE") or "en-IN-female-neutral"

        if not token:
            raise ValueError("SMALLEST_API_KEY not set")
        cfg = Configuration(access_token=token)
        self.client = AtomsClient(cfg)

    async def synthesize(self, text: str, *, session_id: str | None = None, **kwargs) -> bytes:
        resp = await asyncio.to_thread(
            self.client.tts.synthesize,
            text=text,
            voice=self.voice,
            model=self.model,
            output="bytes"
        )
        audio = resp.content
        log.debug("SmallestTTS: generated %d bytes", len(audio))
        return audio