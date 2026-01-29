import requests, time, sys

API_KEY = "sk_V2_hgu_kibn3Pw9lOR_6jpjwIUcAOX0ZFywaaQAg36vhu6tRK2s"
script = """I need to tell you something about your investment strategy. It's trash. Let me explain. While you've been panicking about the stock market, I've been dollar-cost averaging into high-yield dividend stocks. You diversified into crypto? Adorable. I diversified into three different food bowls. Same concept. Better returns. You know why I'm beating the S&P 500? Simple. I don't check my portfolio every five minutes. I sleep eighteen hours a day. That's called emotional discipline. Your financial advisor charges you two percent? I get mine for free. It's called burying things in the backyard. Zero management fees. And compound interest? I've been compounding treats for seven years. That's 49 in dog years. Basically Warren Buffett. Here's what you don't understand. The market rewards patience. I waited six hours for you to come home. Every single day. That's the kind of long-term thinking that builds wealth. So while you're stress-eating over your 401k, I'm living off passive income from being cute. The humans? Obsolete. Your dog. Portfolio manager of the year."""

print("🐕 Trying HeyGen v1 Streaming Avatar...")
headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

# Try v1/streaming.new endpoint
payload = {
    "quality": "high",
    "avatar_name": "Wayne_20240711",  # Try a known avatar
    "voice": {
        "type": "text",
        "voice_id": "1bd001e7e50f421d891986aad5158bc8",
        "input_text": script
    },
    "dimension": {"width": 1080, "height": 1920},
    "background": "#1a1a2e"
}

r = requests.post("https://api.heygen.com/v1/streaming.new", json=payload, headers=headers)
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:500]}")

if r.status_code in [200,201]:
    print("\n✅ Success! Processing...")
    data = r.json()
    print(data)
else:
    # Try alternative endpoint
    print("\nTrying v1/video/generate...")
    r2 = requests.post("https://api.heygen.com/v1/video/generate", json=payload, headers=headers)
    print(f"Status: {r2.status_code}")
    print(f"Response: {r2.text[:500]}")
