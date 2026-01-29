#!/usr/bin/env python3
"""
Generate hamster portrait with DALL-E (via OpenAI API)
"""
import os
import requests

# Note: You can also use Midjourney, but DALL-E is easier via API
# For now, let's document what to request

prompt = """
Professional portrait photograph of a wise-looking hamster, 
front-facing, making direct eye contact with camera, 
well-lit studio lighting, shallow depth of field, 
neutral background, 4K quality, photorealistic,
portrait orientation suitable for video
"""

print("=" * 60)
print("DALL-E PROMPT FOR HAMSTER PORTRAIT:")
print("=" * 60)
print(prompt)
print("\n" + "=" * 60)
print("\nOPTIONS:")
print("=" * 60)
print("\n1. OpenAI DALL-E 3 (API)")
print("   Cost: $0.04 per image (1024x1024)")
print("   Quality: Very good")
print("   URL: https://platform.openai.com/playground")
print("\n2. Midjourney")
print("   Cost: $10/month (Basic plan)")
print("   Quality: Best")
print("   URL: https://midjourney.com")
print("\n3. Leonardo.ai")
print("   Cost: Free tier (150 images/day)")
print("   Quality: Good")
print("   URL: https://leonardo.ai")
print("\n" + "=" * 60)
