#!/usr/bin/env python3
"""
Test ElevenLabs TTS for YouTube Shorts
"""
import os
from elevenlabs.client import ElevenLabs

# Read script
with open('script.txt', 'r') as f:
    content = f.read()

# Extract just the spoken parts
lines = content.split('\n')
spoken_text = []

for line in lines:
    if line.strip() and not line.startswith('TITLE:') and not line.startswith('HOOK') and not line.startswith('CONTENT') and not line.startswith('CTA') and not line.startswith('---') and not line.startswith('WORD COUNT') and not line.startswith('ESTIMATED'):
        spoken_text.append(line.strip())

text = ' '.join(spoken_text)

print("Script text:")
print(text)
print(f"\nCharacters: {len(text)}")

# Initialize ElevenLabs
api_key = os.getenv('ELEVEN_API_KEY')

if not api_key:
    print("\n❌ ERROR: ELEVEN_API_KEY not set")
    exit(1)

client = ElevenLabs(api_key=api_key)

print("\n🎤 Generating voiceover with ElevenLabs...")
print("Voice: Adam")

# Generate audio using text_to_speech
audio_generator = client.text_to_speech.convert(
    voice_id="pNInz6obpgDQGcFmaJgB",  # Adam voice ID
    text=text,
    model_id="eleven_multilingual_v2"
)

# Save to file
with open("voiceover_eleven.mp3", "wb") as f:
    for chunk in audio_generator:
        f.write(chunk)

print("✅ Generated: voiceover_eleven.mp3")
print("\nTo compare:")
print("  Old TTS: voiceover.mp3")
print("  ElevenLabs: voiceover_eleven.mp3")
