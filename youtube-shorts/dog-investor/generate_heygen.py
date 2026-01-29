#!/usr/bin/env python3
"""
Generate talking dog investor video with HeyGen API
"""
import os
import sys
import time
import requests
import base64

API_KEY = "sk_V2_hgu_kibn3Pw9lOR_6jpjwIUcAOX0ZFywaaQAg36vhu6tRK2s"
BASE_URL = "https://api.heygen.com/v2"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print("🐕 Creating Dog Investor Video with HeyGen API...")
print("=" * 60)

# The script
script = """I need to tell you something about your investment strategy.

It's trash. Let me explain.

While you've been panicking about the stock market, I've been dollar-cost averaging into high-yield dividend stocks.

You diversified into crypto? Adorable. I diversified into three different food bowls. Same concept. Better returns.

You know why I'm beating the S&P 500? 

Simple. I don't check my portfolio every five minutes. I sleep eighteen hours a day. That's called emotional discipline.

Your financial advisor charges you two percent? I get mine for free. It's called burying things in the backyard. Zero management fees.

And compound interest? I've been compounding treats for seven years. That's 49 in dog years. Basically Warren Buffett.

Here's what you don't understand. The market rewards patience.

I waited six hours for you to come home. Every single day. That's the kind of long-term thinking that builds wealth.

So while you're stress-eating over your 401k, I'm living off passive income from being cute.

The humans? Obsolete.

Your dog. Portfolio manager of the year."""

print(f"\n📝 Script: {len(script)} characters")
print(f"⏱️  Estimated length: ~60-65 seconds")

# Step 1: Upload avatar image
print("\n" + "=" * 60)
print("📤 STEP 1: Uploading dog portrait...")
print("=" * 60)

# Read and encode image
with open("dog_portrait.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

# Upload image
upload_payload = {
    "image": f"data:image/jpeg;base64,{image_data}",
}

response = requests.post(
    f"{BASE_URL}/avatars",
    json=upload_payload,
    headers=headers
)

if response.status_code not in [200, 201]:
    print(f"❌ Upload failed: {response.status_code}")
    print(f"Response: {response.text}")
    sys.exit(1)

avatar_data = response.json()
print(f"✅ Avatar uploaded successfully!")
print(f"Avatar ID: {avatar_data.get('data', {}).get('avatar_id', 'N/A')}")

avatar_id = avatar_data.get("data", {}).get("avatar_id")

if not avatar_id:
    print("❌ No avatar_id received")
    print(f"Full response: {avatar_data}")
    sys.exit(1)

# Step 2: Create video
print("\n" + "=" * 60)
print("🎬 STEP 2: Creating talking video...")
print("=" * 60)

video_payload = {
    "video_inputs": [{
        "character": {
            "type": "avatar",
            "avatar_id": avatar_id,
            "avatar_style": "normal"
        },
        "voice": {
            "type": "text",
            "input_text": script,
            "voice_id": "1bd001e7e50f421d891986aad5158bc8",  # Josh - authoritative
            "speed": 1.0
        },
        "background": {
            "type": "color",
            "value": "#1a1a2e"  # Dark professional background
        }
    }],
    "dimension": {
        "width": 1080,
        "height": 1920
    },
    "aspect_ratio": "9:16",
    "test": False
}

response = requests.post(
    f"{BASE_URL}/video/generate",
    json=video_payload,
    headers=headers
)

if response.status_code not in [200, 201]:
    print(f"❌ Video generation failed: {response.status_code}")
    print(f"Response: {response.text}")
    sys.exit(1)

video_data = response.json()
video_id = video_data.get("data", {}).get("video_id")

if not video_id:
    print("❌ No video_id received")
    print(f"Full response: {video_data}")
    sys.exit(1)

print(f"✅ Video generation started!")
print(f"Video ID: {video_id}")

# Step 3: Poll for completion
print("\n" + "=" * 60)
print("⏳ STEP 3: Waiting for video generation...")
print("=" * 60)
print("(This typically takes 2-3 minutes)")

max_attempts = 60
attempt = 0

while attempt < max_attempts:
    time.sleep(10)
    attempt += 1
    
    status_response = requests.get(
        f"{BASE_URL}/video_status.get",
        params={"video_id": video_id},
        headers=headers
    )
    
    if status_response.status_code != 200:
        print(f"  ⚠️  Status check error: {status_response.status_code}")
        continue
    
    status_data = status_response.json()
    data = status_data.get("data", {})
    status = data.get("status", "unknown")
    
    print(f"  [{attempt}/60] Status: {status}")
    
    if status == "completed":
        video_url = data.get("video_url")
        
        if not video_url:
            print("❌ No video URL in response")
            print(f"Response: {status_data}")
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("✅ VIDEO READY!")
        print("=" * 60)
        print(f"📥 Downloading from: {video_url}")
        
        # Download video
        video_response = requests.get(video_url)
        
        with open("dog_investor_talking.mp4", "wb") as f:
            f.write(video_response.content)
        
        size_mb = len(video_response.content) / 1024 / 1024
        
        print(f"✅ Saved: dog_investor_talking.mp4")
        print(f"📊 Size: {size_mb:.1f} MB")
        print(f"⏱️  Duration: ~60-65 seconds")
        print("\n" + "=" * 60)
        print("🎉 SUCCESS!")
        print("=" * 60)
        sys.exit(0)
    
    elif status == "failed":
        error = data.get("error", "Unknown error")
        print(f"\n❌ Generation failed: {error}")
        print(f"Full response: {status_data}")
        sys.exit(1)
    
    elif status == "processing":
        progress = data.get("progress", 0)
        print(f"      Progress: {progress}%")

print("\n⏰ Timeout - video still processing after 10 minutes")
print("Check HeyGen dashboard: https://app.heygen.com/")
sys.exit(1)
