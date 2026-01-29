#!/usr/bin/env python3
"""
Create talking hamster with D-ID API (v2 - using URLs)
"""
import os
import sys
import time
import requests

API_KEY = "enZvbmltaXJkYW1qYW5vdmljQGdtYWlsLmNvbQ:0UpLCtPMhIjAKT7n5rj8M"
BASE_URL = "https://api.d-id.com"

headers = {
    "Authorization": f"Basic {API_KEY}",
    "Content-Type": "application/json"
}

print("🎬 Creating talking hamster with D-ID API (v2)...")

# Step 1: Upload image to D-ID
print("\n📤 Uploading image...")

with open("hamster_portrait.jpg", "rb") as f:
    files = {"image": ("hamster.jpg", f, "image/jpeg")}
    upload_headers = {"Authorization": f"Basic {API_KEY}"}
    
    response = requests.post(
        f"{BASE_URL}/images",
        files=files,
        headers=upload_headers
    )

if response.status_code not in [200, 201]:
    print(f"❌ Image upload error: {response.status_code}")
    print(response.text)
    sys.exit(1)

image_url = response.json()["url"]
print(f"✅ Image uploaded: {image_url}")

# Step 2: Upload audio
print("\n📤 Uploading audio...")

with open("hamster_voice.mp3", "rb") as f:
    files = {"audio": ("voice.mp3", f, "audio/mpeg")}
    
    response = requests.post(
        f"{BASE_URL}/audios",
        files=files,
        headers=upload_headers
    )

if response.status_code not in [200, 201]:
    print(f"❌ Audio upload error: {response.status_code}")
    print(response.text)
    sys.exit(1)

audio_url = response.json()["url"]
print(f"✅ Audio uploaded: {audio_url}")

# Step 3: Create talk
print("\n🎤 Creating talking video...")

payload = {
    "source_url": image_url,
    "script": {
        "type": "audio",
        "audio_url": audio_url
    },
    "config": {
        "fluent": True,
        "pad_audio": 0.0,
        "stitch": True
    }
}

response = requests.post(
    f"{BASE_URL}/talks",
    json=payload,
    headers=headers
)

if response.status_code != 201:
    print(f"❌ Talk creation error: {response.status_code}")
    print(response.text)
    sys.exit(1)

talk_id = response.json()["id"]
print(f"✅ Talk created! ID: {talk_id}")

# Step 4: Poll for completion
print("\n⏳ Waiting for video generation (1-2 minutes)...")

max_attempts = 60
attempt = 0

while attempt < max_attempts:
    time.sleep(5)
    attempt += 1
    
    status_response = requests.get(
        f"{BASE_URL}/talks/{talk_id}",
        headers=headers
    )
    
    if status_response.status_code != 200:
        print(f"  Status check error: {status_response.status_code}")
        continue
    
    status_data = status_response.json()
    status = status_data.get("status")
    
    print(f"  [{attempt}/60] Status: {status}")
    
    if status == "done":
        video_url = status_data.get("result_url")
        print(f"\n✅ Video ready!")
        print(f"📥 Downloading: {video_url}")
        
        video_response = requests.get(video_url)
        with open("hamster_talking.mp4", "wb") as f:
            f.write(video_response.content)
        
        size_mb = len(video_response.content) / 1024 / 1024
        print(f"✅ Saved: hamster_talking.mp4 ({size_mb:.1f} MB)")
        sys.exit(0)
    
    elif status == "error":
        error_msg = status_data.get("error", {})
        print(f"❌ Generation error: {error_msg}")
        sys.exit(1)

print("⏰ Timeout - video still processing")
sys.exit(1)
