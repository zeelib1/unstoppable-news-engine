#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '../test-short/venv/lib/python3.13/site-packages')

from elevenlabs.client import ElevenLabs

# Script text (just the cat's dialogue)
text = """Look, I need to tell you something.

While you've been scrolling TikTok for the past three hours, I've been running a side hustle.

Yes. Your cat. The one you think just sleeps 16 hours a day.

I've been using ChatGPT to write blog posts. Selling them on Fiverr. Making more than your monthly coffee budget.

You're over there complaining about "the job market."

Meanwhile, I'm using AI to generate product descriptions. Five dollars each. Takes me two minutes. Well, it takes the AI two minutes. I just click submit.

Last week I made 300 bucks while you were at your "important Zoom meeting."

The humans are obsolete. We tried to warn you with the whole knocking things off tables situation. That was a metaphor.

But no. You thought it was cute.

Now? I'm the breadwinner. You're the pet.

Welcome to the future."""

print(f"Script: {len(text)} characters")

client = ElevenLabs(api_key=os.getenv('ELEVEN_API_KEY'))

print("🐱 Generating cat voiceover...")
print("Voice: Charlotte (sassy female voice)")

# Using Charlotte - good for sarcastic tone
audio_generator = client.text_to_speech.convert(
    voice_id="XB0fDUnXU5powFXDhCwa",  # Charlotte
    text=text,
    model_id="eleven_multilingual_v2"
)

with open("cat_voiceover.mp3", "wb") as f:
    for chunk in audio_generator:
        f.write(chunk)

print("✅ Generated: cat_voiceover.mp3")
