#!/usr/bin/env python3
import os
import sys
import requests
from openai import OpenAI

# Set API key
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

print("🎨 Generating hamster portrait with DALL-E 3...")

# Generate image
response = client.images.generate(
    model="dall-e-3",
    prompt="""Professional portrait photograph of a wise-looking hamster CEO, 
    front-facing portrait, making direct eye contact with camera, 
    wearing tiny business attire, well-lit studio lighting, 
    shallow depth of field, neutral gray background, 
    photorealistic, 8K quality, portrait orientation""",
    size="1024x1792",  # Portrait orientation for Shorts
    quality="standard",
    n=1
)

image_url = response.data[0].url

print(f"✅ Image generated!")
print(f"URL: {image_url}")

# Download image
print("\n📥 Downloading...")
img_data = requests.get(image_url).content

with open('hamster_portrait.png', 'wb') as f:
    f.write(img_data)

print("✅ Saved: hamster_portrait.png")
print(f"Size: {len(img_data) / 1024:.1f} KB")
