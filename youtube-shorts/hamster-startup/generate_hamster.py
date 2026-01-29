#!/usr/bin/env python3
import os, sys
sys.path.insert(0, '../test-short/venv/lib/python3.13/site-packages')
from elevenlabs.client import ElevenLabs

text = """Okay, listen up. I've been running on this wheel for three years.

That's longer than most startups survive.

You want to know the secret? It's not about the destination. It's about consistent daily effort that looks completely pointless to outside observers.

Everyone's obsessed with "disruption" and "unicorn valuations."

Meanwhile, I'm here optimizing my seed storage strategy. That's customer retention, baby.

You know what kills startups? Overthinking. Analysis paralysis.

Me? I see a sunflower seed, I take action. No three-hour strategy meeting.

Your "minimum viable product"? I built mine in 30 seconds. It's a pile of bedding in the corner. Customers love it.

And pivoting? I pivot 47 times per minute on this wheel. That's agility.

So here's my advice: Stop reading startup blogs. Start running in circles until something works.

Your hamster has spoken."""

print(f"Characters: {len(text)}")
client = ElevenLabs(api_key=os.getenv('ELEVEN_API_KEY'))

print("🐹 Generating hamster voiceover...")
print("Voice: Josh (wise, slightly deep)")

audio_gen = client.text_to_speech.convert(
    voice_id="TxGEqnHWrfWFTfGW9XjX",  # Josh - good for wise/serious tone
    text=text,
    model_id="eleven_multilingual_v2"
)

with open("hamster_voice.mp3", "wb") as f:
    for chunk in audio_gen:
        f.write(chunk)

print("✅ Generated: hamster_voice.mp3")
