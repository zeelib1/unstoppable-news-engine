#!/usr/bin/env python3
"""
Create talking hamster video with D-ID API
"""
import os
import sys
import time
import requests
import base64

# D-ID API credentials
API_KEY = "enZvbmltaXJkYW1qYW5vdmljQGdtYWlsLmNvbQ:0UpLCtPMhIjAKT7n5rj8M"
BASE_URL = "https://api.d-id.com"

headers = {
    "Authorization": f"Basic {API_KEY}",
    "Content-Type": "application/json"
}

print("🎬 Creating talking hamster with D-ID API...")

# Step 1: Upload image
print("\n📤 Step 1: Uploading hamster portrait...")

with open("hamster_portrait.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

# Step 2: Upload audio
print("📤 Step 2: Uploading audio...")

with open("hamster_voice.mp3", "rb") as f:
    audio_data = base64.b64encode(f.read()).decode()

# Step 3: Create talk
print("🎤 Step 3: Creating talking video...")

payload = {
    "source_url": f"data:image/jpeg;base64,{image_data}",
    "script": {
        "type": "audio",
        "audio_url": f"data:audio/mpeg;base64,{audio_data}"
    },
    "config": {
        "fluent": True,
        "pad_audio": 0.0
    }
}

response = requests.post(
    f"{BASE_URL}/talks",
    json=payload,
    headers=headers
)

if response.status_code != 201:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
    sys.exit(1)

talk_id = response.json()["id"]
print(f"✅ Talk created! ID: {talk_id}")

# Step 4: Poll for completion
print("\n⏳ Step 4: Waiting for video generation...")
print("(This takes 1-2 minutes)")

max_attempts = 60
attempt = 0

while attempt < max_attempts:
    time.sleep(5)
    attempt += 1
    
    status_response = requests.get(
        f"{BASE_URL}/talks/{talk_id}",
        headers=headers
    )
    
    status_data = status_response.json()
    status = status_data.get("status")
    
    print(f"  Attempt {attempt}: Status = {status}")
    
    if status == "done":
        video_url = status_data.get("result_url")
        print(f"\n✅ Video ready!")
        print(f"📥 Downloading from: {video_url}")
        
        # Download video
        video_response = requests.get(video_url)
        with open("hamster_talking.mp4", "wb") as f:
            f.write(video_response.content)
        
        print("✅ Saved: hamster_talking.mp4")
        print(f"Size: {len(video_response.content) / 1024 / 1024:.1f} MB")
        sys.exit(0)
    
    elif status == "error":
        print(f"❌ Error: {status_data.get('error')}")
        sys.exit(1)

print("⏰ Timeout waiting for video")
sys.exit(1)
