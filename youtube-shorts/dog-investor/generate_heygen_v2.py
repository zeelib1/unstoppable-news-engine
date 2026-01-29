#!/usr/bin/env python3
"""
Generate talking dog with HeyGen API v2 (corrected endpoints)
"""
import os
import sys
import time
import requests

API_KEY = "sk_V2_hgu_kibn3Pw9lOR_6jpjwIUcAOX0ZFywaaQAg36vhu6tRK2s"

print("🐕 Creating Dog Investor Video with HeyGen...")
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

# Step 1: Create talking photo directly
print("\n" + "=" * 60)
print("🎬 Creating talking dog video...")
print("=" * 60)

headers = {
    "X-Api-Key": API_KEY
}

# Upload image as multipart
with open("dog_portrait.jpg", "rb") as f:
    files = {
        "image": ("dog.jpg", f, "image/jpeg")
    }
    
    data = {
        "text": script,
        "voice_id": "1bd001e7e50f421d891986aad5158bc8",  # Josh voice
        "dimension": "vertical",  # For Shorts (9:16)
    }
    
    response = requests.post(
        "https://api.heygen.com/v1/talking_photo",
        files=files,
        data=data,
        headers=headers
    )

if response.status_code not in [200, 201]:
    print(f"❌ Request failed: {response.status_code}")
    print(f"Response: {response.text}")
    sys.exit(1)

result = response.json()
print(f"✅ Request successful!")

# Get video ID
if "data" in result and "id" in result["data"]:
    video_id = result["data"]["id"]
elif "id" in result:
    video_id = result["id"]
else:
    print(f"❌ No video ID in response: {result}")
    sys.exit(1)

print(f"Video ID: {video_id}")

# Step 2: Poll for completion
print("\n" + "=" * 60)
print("⏳ Waiting for generation (2-3 minutes)...")
print("=" * 60)

max_attempts = 60
attempt = 0

while attempt < max_attempts:
    time.sleep(10)
    attempt += 1
    
    status_response = requests.get(
        f"https://api.heygen.com/v1/talking_photo/{video_id}",
        headers=headers
    )
    
    if status_response.status_code != 200:
        print(f"  ⚠️  Check failed: {status_response.status_code}")
        continue
    
    status_data = status_response.json()
    data = status_data.get("data", status_data)
    status = data.get("status", "unknown")
    
    print(f"  [{attempt}/60] Status: {status}")
    
    if status == "completed":
        video_url = data.get("video_url") or data.get("url")
        
        if not video_url:
            print(f"❌ No video URL: {status_data}")
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("✅ VIDEO READY!")
        print("=" * 60)
        print(f"📥 Downloading...")
        
        video_response = requests.get(video_url)
        
        with open("dog_investor_talking.mp4", "wb") as f:
            f.write(video_response.content)
        
        size_mb = len(video_response.content) / 1024 / 1024
        
        print(f"✅ Saved: dog_investor_talking.mp4 ({size_mb:.1f} MB)")
        print("\n🎉 SUCCESS!")
        sys.exit(0)
    
    elif status == "failed" or status == "error":
        print(f"❌ Failed: {data.get('error', 'Unknown')}")
        sys.exit(1)

print("⏰ Timeout")
sys.exit(1)
