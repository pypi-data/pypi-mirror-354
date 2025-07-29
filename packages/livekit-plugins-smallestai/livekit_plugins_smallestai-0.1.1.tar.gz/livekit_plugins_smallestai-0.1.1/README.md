# livekit-plugins-smallestai

A LiveKit Agents plugin integrating Smallest AI’s Atoms SDK for high-fidelity text-to-speech (TTS), streaming speech-to-text (STT), and Groq LLM support.

## Features

- **TTS with Smallest AI Waves**  
  Real-time audio generation via Atoms' Waves engine.

- **Streaming STT**  
  Two-way audio transcription using Atoms' ASR models.

- **Groq LLM Integration**  
  Chat powered by Groq Cloud’s llama-3.3-70b-versatile model.

## Installation

```bash
pip install livekit-plugins-smallestai
```

## Environment Variables

```dotenv
# Smallest AI Atoms API key
SMALLEST_API_KEY=sk-...

# TTS/STT model overrides (optional)
SMALLEST_TTS_MODEL=waves-v2
SMALLEST_TTS_VOICE=en-IN-female-neutral
SMALLEST_STT_MODEL=whisper-small

# Groq Cloud credentials
GROQ_API_KEY=groq-...
GROQ_MODEL=llama-3.3-70b-versatile
```

## Usage

```python
import os, asyncio
from livekit import AgentSession
from livekit_smallestai.tts import SmallestTTS
from livekit_smallestai.stt import SmallestSTT
from livekit_smallestai.llm_groq import GroqLLM

async def main():
    session = AgentSession(
        llm=GroqLLM(),
        tts=SmallestTTS(),
        stt=SmallestSTT(),
    )
    await session.say("Hello from Smallest AI & Groq!")
    message = await session.chat([{"role":"user","content":"Welcome!"}])
    print(message)

if __name__ == "__main__":
    asyncio.run(main())
```

## Development

```bash
# Build
python3 -m build

# Test
pip install pytest
pytest -q

# Publish
twine upload dist/*
```

## License

MIT License. See [LICENSE](LICENSE) for details.