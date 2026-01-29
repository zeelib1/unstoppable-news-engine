import requests, time, sys

API_KEY = "sk_V2_hgu_kibn3Pw9lOR_6jpjwIUcAOX0ZFywaaQAg36vhu6tRK2s"
script = """I need to tell you something about your investment strategy. It's trash. Let me explain. While you've been panicking about the stock market, I've been dollar-cost averaging into high-yield dividend stocks. You diversified into crypto? Adorable. I diversified into three different food bowls. Same concept. Better returns. You know why I'm beating the S&P 500? Simple. I don't check my portfolio every five minutes. I sleep eighteen hours a day. That's called emotional discipline. Your financial advisor charges you two percent? I get mine for free. It's called burying things in the backyard. Zero management fees. And compound interest? I've been compounding treats for seven years. That's 49 in dog years. Basically Warren Buffett. Here's what you don't understand. The market rewards patience. I waited six hours for you to come home. Every single day. That's the kind of long-term thinking that builds wealth. So while you're stress-eating over your 401k, I'm living off passive income from being cute. The humans? Obsolete. Your dog. Portfolio manager of the year."""

print("🐕 Creating Dog Investor Video...\n")
headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

payload = {
    "video_inputs": [{
        "character": {
            "type": "avatar",
            "avatar_id": "josh_lite3_20230714",
            "avatar_style": "normal"
        },
        "voice": {
            "type": "text",
            "input_text": script,
            "voice_id": "1bd001e7e50f421d891986aad5158bc8"
        }
    }],
    "dimension": {"width": 1080, "height": 1920}
}

r = requests.post("https://api.heygen.com/v2/video/generate", json=payload, headers=headers)
print(f"Create: {r.status_code}")

if r.status_code in [200,201]:
    video_id = r.json().get("data",{}).get("video_id")
    print(f"Video ID: {video_id}\nWaiting...\n")
    
    for i in range(60):
        time.sleep(10)
        s = requests.get(f"https://api.heygen.com/v1/video_status.get?video_id={video_id}", headers=headers)
        if s.status_code == 200:
            st = s.json().get("data",{})
            print(f"[{i+1}] {st.get('status')}")
            if st.get("status") == "completed":
                vid = requests.get(st["video_url"]).content
                with open("dog_investor.mp4", "wb") as f: f.write(vid)
                print(f"\n✅ Saved! ({len(vid)/1024/1024:.1f}MB)")
                sys.exit(0)
else:
    print(f"Error: {r.text}")
