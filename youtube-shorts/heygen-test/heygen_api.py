#!/usr/bin/env python3
"""
Create talking video with HeyGen API
"""
import os
import sys
import time
import requests
import json

API_KEY = os.getenv('HEYGEN_API_KEY')
BASE_URL = "https://api.heygen.com/v2"

if not API_KEY:
    print("❌ ERROR: HEYGEN_API_KEY not set")
    print("\nTo use:")
    print("export HEYGEN_API_KEY='your_key_here'")
    print("python heygen_api.py")
    sys.exit(1)

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print("🎬 Creating video with HeyGen API...")

# Script for the video
script = """Okay, listen up. I've been running on this wheel for three years. That's longer than most startups survive.

You want to know the secret? It's not about the destination. It's about consistent daily effort that looks completely pointless to outside observers.

Everyone's obsessed with disruption and unicorn valuations. Meanwhile, I'm here optimizing my seed storage strategy. That's customer retention, baby.

You know what kills startups? Overthinking. Analysis paralysis.

Me? I see a sunflower seed, I take action. No three-hour strategy meeting.

Your minimum viable product? I built mine in 30 seconds. It's a pile of bedding in the corner. Customers love it.

And pivoting? I pivot 47 times per minute on this wheel. That's agility.

So here's my advice: Stop reading startup blogs. Start running in circles until something works.

Your hamster has spoken."""

# Step 1: Upload image
print("\n📤 Step 1: Uploading image...")

with open("../hamster-startup/cat_portrait.jpg", "rb") as f:
    files = {"file": f}
    upload_headers = {"X-Api-Key": API_KEY}
    
    response = requests.post(
        f"{BASE_URL}/avatars",
        files=files,
        headers=upload_headers
    )

if response.status_code not in [200, 201]:
    print(f"❌ Upload error: {response.status_code}")
    print(response.text)
    sys.exit(1)

avatar_id = response.json().get("data", {}).get("avatar_id")
print(f"✅ Avatar uploaded: {avatar_id}")

# Step 2: Create video
print("\n🎤 Step 2: Creating video...")

payload = {
    "video_inputs": [{
        "character": {
            "type": "avatar",
            "avatar_id": avatar_id,
            "avatar_style": "normal"
        },
        "voice": {
            "type": "text",
            "input_text": script,
            "voice_id": "1bd001e7e50f421d891986aad5158bc8"  # Josh voice
        },
        "background": {
            "type": "color",
            "value": "#F5F5F5"
        }
    }],
    "dimension": {
        "width": 1080,
        "height": 1920
    },
    "aspect_ratio": "9:16"
}

response = requests.post(
    f"{BASE_URL}/video/generate",
    json=payload,
    headers=headers
)

if response.status_code not in [200, 201]:
    print(f"❌ Video creation error: {response.status_code}")
    print(response.text)
    sys.exit(1)

video_id = response.json().get("data", {}).get("video_id")
print(f"✅ Video generation started: {video_id}")

# Step 3: Poll for completion
print("\n⏳ Step 3: Waiting for video (2-3 minutes)...")

max_attempts = 60
attempt = 0

while attempt < max_attempts:
    time.sleep(10)
    attempt += 1
    
    status_response = requests.get(
        f"{BASE_URL}/video_status.get?video_id={video_id}",
        headers=headers
    )
    
    if status_response.status_code != 200:
        print(f"  Status check error: {status_response.status_code}")
        continue
    
    status_data = status_response.json().get("data", {})
    status = status_data.get("status")
    
    print(f"  [{attempt}/60] Status: {status}")
    
    if status == "completed":
        video_url = status_data.get("video_url")
        print(f"\n✅ Video ready!")
        print(f"📥 Downloading: {video_url}")
        
        video_response = requests.get(video_url)
        with open("heygen_talking_cat.mp4", "wb") as f:
            f.write(video_response.content)
        
        size_mb = len(video_response.content) / 1024 / 1024
        print(f"✅ Saved: heygen_talking_cat.mp4 ({size_mb:.1f} MB)")
        print(f"\n🎬 Duration: ~55 seconds")
        sys.exit(0)
    
    elif status == "failed":
        error = status_data.get("error", "Unknown error")
        print(f"❌ Generation failed: {error}")
        sys.exit(1)

print("⏰ Timeout - video still processing")
print("Check HeyGen dashboard: https://app.heygen.com/")
sys.exit(1)
