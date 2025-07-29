# NAINT

A Python client for the NAINT TTS API.

## Installation

```bash
pip install naint
```

## Example Usage

### TTS
```python
from naint import NAINT

client = NAINT(api_key="your_api_key")

# Convert text to audio (base64 WAV)
audio = client.text_to_speech.convert(
    text="Hello world!",
    voice_id="voice123"
)

# Save audio to file
client.text_to_speech.convert_to_file(
    text="Saving this to file.",
    voice_id="voice123",
    file_path="output.wav"
)
```

### STT
```python
from naint import NAINT

client = NAINT(api_key="your_api_key")а

# Convert audio to text
transcription = client.speech_to_text.transcribe(
    file_path="path_to_audio.wav",
    model="english"
)

print("Transcription:", transcription)
```

### Voice Cloning
```python
import os

from naint import NAINT

client = NAINT(api_key="your_api_key")

client.voice_cloning.clone_to_file(
    origin_audio = "origin.wav",
    reference_audio = "reference.wav",
    save_file = "cloned.wav"
)

assert os.path.isfile("cloned.wav")
```

### Working with Voices

```python
voices = client.voices.get_all()
for voice in voices.get("voices", []):
    print(voice["voice_id"], voice["name"])
```


## Async Usage

```python
import asyncio
from naint import AsyncNAINT

async def main():
    client = AsyncNAINT(api_key="your_api_key")
    
    # Get all voices
    voices = await client.voices.get_all()
    print("Voices:", voices)
    
    # Convert text to audio (base64 WAV)
    audio = await client.text_to_speech.convert(
        text="Hello world!",
        voice_id="voice123"
    )
    print("Audio:", audio)
    
    # Convert audio to text
    transcription = await client.speech_to_text.transcribe(
        file_path="path_to_audio.wav",
        model="english"
    )
    print("Transcription:", transcription)

asyncio.run(main())
```
