# VoiceClient

`VoiceClient` provides a minimal interface to Discord's voice gateway. It handles the WebSocket handshake and lets you stream audio over UDP.

## Basic Usage

```python
import asyncio
import os
import disagreement

vc = disagreement.VoiceClient(
    os.environ["DISCORD_VOICE_ENDPOINT"],
    os.environ["DISCORD_SESSION_ID"],
    os.environ["DISCORD_VOICE_TOKEN"],
    int(os.environ["DISCORD_GUILD_ID"]),
    int(os.environ["DISCORD_USER_ID"]),
)

asyncio.run(vc.connect())
```

After connecting you can send raw Opus frames:

```python
await vc.send_audio_frame(opus_bytes)
```

Call `await vc.close()` when finished.
