import requests, time, sys, base64

API_KEY = "sk_V2_hgu_kibn3Pw9lOR_6jpjwIUcAOX0ZFywaaQAg36vhu6tRK2s"
script = """I need to tell you something about your investment strategy. It's trash. Let me explain. While you've been panicking about the stock market, I've been dollar-cost averaging into high-yield dividend stocks. You diversified into crypto? Adorable. I diversified into three different food bowls. Same concept. Better returns. You know why I'm beating the S&P 500? Simple. I don't check my portfolio every five minutes. I sleep eighteen hours a day. That's called emotional discipline. Your financial advisor charges you two percent? I get mine for free. It's called burying things in the backyard. Zero management fees. And compound interest? I've been compounding treats for seven years. That's 49 in dog years. Basically Warren Buffett. Here's what you don't understand. The market rewards patience. I waited six hours for you to come home. Every single day. That's the kind of long-term thinking that builds wealth. So while you're stress-eating over your 401k, I'm living off passive income from being cute. The humans? Obsolete. Your dog. Portfolio manager of the year."""

print("🐕 Step 1: Uploading dog portrait...")
headers = {"X-Api-Key": API_KEY}

# Upload image
files = {"file": open("dog_portrait.jpg", "rb")}
r = requests.post("https://api.heygen.com/v2/avatars/talking_photo", files=files, headers=headers)
print(f"Upload: {r.status_code}")

if r.status_code not in [200,201]:
    print(f"Error: {r.text}")
    sys.exit(1)

avatar_id = r.json().get("data",{}).get("avatar_id")
print(f"Avatar ID: {avatar_id}")

# Create video
print("\n🎬 Step 2: Creating video...")
headers["Content-Type"] = "application/json"

payload = {
    "video_inputs": [{
        "character": {
            "type": "talking_photo",
            "talking_photo_id": avatar_id
        },
        "voice": {
            "type": "text",
            "input_text": script,
            "voice_id": "1bd001e7e50f421d891986aad5158bc8"
        }
    }],
    "dimension": {"width": 1080, "height": 1920}
}

r2 = requests.post("https://api.heygen.com/v2/video/generate", json=payload, headers=headers)
print(f"Create: {r2.status_code}")

if r2.status_code in [200,201]:
    video_id = r2.json().get("data",{}).get("video_id")
    print(f"Video ID: {video_id}\n⏳ Waiting...")
    
    for i in range(60):
        time.sleep(10)
        s = requests.get(f"https://api.heygen.com/v1/video_status.get?video_id={video_id}", headers={"X-Api-Key": API_KEY})
        if s.status_code == 200:
            st = s.json().get("data",{})
            status = st.get("status")
            print(f"[{i+1}/60] {status}")
            if status == "completed":
                vid = requests.get(st["video_url"]).content
                with open("dog_investor.mp4", "wb") as f: f.write(vid)
                print(f"\n✅ SUCCESS! Saved dog_investor.mp4 ({len(vid)/1024/1024:.1f}MB)")
                sys.exit(0)
            elif status == "failed":
                print(f"❌ Failed: {st}")
                sys.exit(1)
else:
    print(f"Error: {r2.text}")
