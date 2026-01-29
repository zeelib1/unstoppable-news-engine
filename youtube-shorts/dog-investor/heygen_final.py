#!/usr/bin/env python3
import requests
import time
import sys

API_KEY = "sk_V2_hgu_kibn3Pw9lOR_6jpjwIUcAOX0ZFywaaQAg36vhu6tRK2s"

script = """I need to tell you something about your investment strategy. It's trash. Let me explain.

While you've been panicking about the stock market, I've been dollar-cost averaging into high-yield dividend stocks.

You diversified into crypto? Adorable. I diversified into three different food bowls. Same concept. Better returns.

You know why I'm beating the S&P 500? Simple. I don't check my portfolio every five minutes. I sleep eighteen hours a day. That's called emotional discipline.

Your financial advisor charges you two percent? I get mine for free. It's called burying things in the backyard. Zero management fees.

And compound interest? I've been compounding treats for seven years. That's 49 in dog years. Basically Warren Buffett.

Here's what you don't understand. The market rewards patience. I waited six hours for you to come home. Every single day. That's the kind of long-term thinking that builds wealth.

So while you're stress-eating over your 401k, I'm living off passive income from being cute. The humans? Obsolete. Your dog. Portfolio manager of the year."""

print("🐕 HeyGen API - Dog Investor Video")
print("=" * 60)

headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

# Method 1: Try streaming avatar endpoint
payload = {
    "quality": "high",
    "avatar_name": "josh_lite3_20230714",
    "voice": {
        "type": "text",
        "voice_id": "1bd001e7e50f421d891986aad5158bc8",
        "input_text": script
    },
    "dimension": {"width": 1080, "height": 1920}
}

print("\n📤 Attempting video creation...")
response = requests.post(
    "https://api.heygen.com/v2/video/generate",
    json=payload,
    headers=headers
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

if response.status_code in [200, 201]:
    data = response.json()
    video_id = data.get("data", {}).get("video_id")
    
    if video_id:
        print(f"\n✅ Video ID: {video_id}")
        print("⏳ Polling for completion...")
        
        for i in range(60):
            time.sleep(10)
            status_resp = requests.get(
                f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
                headers=headers
            )
            
            if status_resp.status_code == 200:
                status_data = status_resp.json().get("data", {})
                status = status_data.get("status")
                print(f"  [{i+1}/60] {status}")
                
                if status == "completed":
                    url = status_data.get("video_url")
                    video = requests.get(url).content
                    with open("dog_investor.mp4", "wb") as f:
                        f.write(video)
                    print(f"\n✅ Saved: dog_investor.mp4 ({len(video)/1024/1024:.1f}MB)")
                    sys.exit(0)
                elif status == "failed":
                    print(f"❌ Failed: {status_data.get('error')}")
                    sys.exit(1)
else:
    print(f"\n❌ Failed to create video")
    print("Full response:", response.text)

print("\n💡 Alternative: Upload files to Drive for manual creation")
