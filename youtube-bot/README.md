# 🤖 YouTube Automation Bot - Proof of Concept

**Generates videos, thumbnails, and uploads to YouTube with human approval**

---

## 📊 COST PER VIDEO

### Budget Setup: **$0.05/video**
- GPT-3.5 Turbo: $0.02
- Google Cloud TTS: $0.03
- FFmpeg: Free
- Pexels Stock: Free
- Stable Diffusion: Free
- YouTube API: Free

### Premium Setup: **$0.48/video**
- GPT-4: $0.20
- ElevenLabs TTS: $0.20
- FFmpeg: Free
- Pexels Stock: Free
- DALL-E 3: $0.08
- YouTube API: Free

---

## 🚀 QUICK START

### 1. Install Dependencies

```bash
cd /root/clawd/youtube-bot
pip install -r requirements.txt

# Install FFmpeg (if not already installed)
sudo apt update && sudo apt install ffmpeg -y
```

### 2. Set Up API Keys

Create a `.env` file:

```bash
# OpenAI (for scripts)
OPENAI_API_KEY=sk-...

# ElevenLabs (for voiceover)
ELEVENLABS_API_KEY=...

# Google Cloud (for TTS alternative)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Pexels (for stock footage)
PEXELS_API_KEY=...
```

### 3. YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials
5. Download `client_secret.json` to this directory
6. Rename it to `youtube_client_secret.json`

### 4. Run the Bot

```bash
python bot.py
```

---

## 🔧 REAL API INTEGRATION EXAMPLES

### OpenAI Script Generation

```python
import openai

def generate_script(topic):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a YouTube scriptwriter."},
            {"role": "user", "content": f"Write a 3-minute video script about: {topic}"}
        ]
    )
    return response.choices[0].message.content
```

### ElevenLabs Voiceover

```python
from elevenlabs import generate, set_api_key

set_api_key("YOUR_ELEVENLABS_KEY")

def create_voiceover(text, output_path):
    audio = generate(
        text=text,
        voice="Adam",  # Or any voice ID
        model="eleven_monolingual_v1"
    )
    
    with open(output_path, "wb") as f:
        f.write(audio)
```

### Google Cloud TTS (Budget Alternative)

```python
from google.cloud import texttospeech

def generate_speech(text, output_path):
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-J"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
```

### Pexels Stock Footage

```python
import requests

def search_pexels_videos(query, per_page=5):
    headers = {"Authorization": "YOUR_PEXELS_API_KEY"}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={per_page}"
    
    response = requests.get(url, headers=headers)
    videos = response.json()["videos"]
    
    return [
        {
            "url": video["video_files"][0]["link"],
            "duration": video["duration"]
        }
        for video in videos
    ]
```

### FFmpeg Video Assembly

```python
import ffmpeg

def create_video(audio_path, images, output_path):
    # Create video from images
    (
        ffmpeg
        .input('image_%d.jpg', pattern_type='sequence', framerate=1/5)
        .output('temp_video.mp4')
        .run()
    )
    
    # Add audio
    (
        ffmpeg
        .input('temp_video.mp4')
        .input(audio_path)
        .output(output_path, vcodec='libx264', acodec='aac', shortest=None)
        .run()
    )
```

### DALL-E 3 Thumbnail

```python
import openai

def generate_thumbnail(title, output_path):
    response = openai.Image.create(
        model="dall-e-3",
        prompt=f"YouTube thumbnail: {title}, bold text, high contrast, eye-catching",
        size="1792x1024",  # YouTube thumbnail size
        quality="standard"
    )
    
    image_url = response.data[0].url
    
    # Download and save
    import requests
    img_data = requests.get(image_url).content
    with open(output_path, 'wb') as f:
        f.write(img_data)
```

### YouTube Upload

```python
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def upload_to_youtube(video_path, title, description, tags):
    # Authenticate
    flow = InstalledAppFlow.from_client_secrets_file(
        'youtube_client_secret.json',
        scopes=['https://www.googleapis.com/auth/youtube.upload']
    )
    credentials = flow.run_local_server(port=8080)
    youtube = build('youtube', 'v3', credentials=credentials)
    
    # Upload
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "28"  # Science & Technology
            },
            "status": {
                "privacyStatus": "private"  # Start private for review
            }
        },
        media_body=video_path
    )
    
    response = request.execute()
    return response["id"]  # Video ID
```

---

## 📋 WORKFLOW

```
1. Generate Topic (GPT-4)
   ↓
2. Write Script (GPT-4)
   ↓
3. Create Voiceover (ElevenLabs/Google TTS)
   ↓
4. Fetch Stock Footage (Pexels)
   ↓
5. Assemble Video (FFmpeg)
   ↓
6. Generate Thumbnail (DALL-E 3)
   ↓
7. 👤 HUMAN REVIEW
   ↓
8. Upload to YouTube (if approved)
```

---

## ⚙️ CONFIGURATION

Edit `bot.py` to customize:

```python
class Config:
    # Your niche
    CHANNEL_NICHE = "tech tutorials"  # Change this
    
    # Video settings
    VIDEO_LENGTH_WORDS = 500  # ~3-4 minutes
    VIDEO_WIDTH = 1920
    VIDEO_HEIGHT = 1080
    
    # Voice settings (ElevenLabs)
    VOICE_ID = "Adam"  # Or any voice you prefer
```

---

## 🎯 NICHES THAT WORK WELL

✅ **Automated Content (YouTube Allows):**
- Educational tutorials
- News summaries (with commentary)
- Data visualizations (stocks, sports)
- Meditation/ambience (with original audio)
- How-to guides
- Product reviews (with original takes)

❌ **Avoid (YouTube Penalizes):**
- Generic motivational quotes
- Scraped top 10 lists
- Pure AI-generated faces (no original content)
- Mass-produced clickbait

---

## 🚨 YOUTUBE ToS COMPLIANCE

### ✅ What You MUST Do:
1. **Review every video** before publishing
2. **Add original value** (commentary, insights, unique angle)
3. **Engage with comments** (shows human involvement)
4. **Quality over quantity** (1-2 videos/week max for automation)

### ❌ What Will Get You Banned:
1. 100% hands-off automation
2. No original value added
3. Scraped/repurposed content
4. Mass uploading (10+ videos/day)

---

## 📈 SCALING STRATEGY

### Month 1: Proof of Concept
- Generate 5 videos
- Test different niches
- Refine script templates
- Cost: $2-5

### Month 2: Consistent Output
- 2 videos/week (8 total)
- Optimize workflow
- Build audience
- Cost: $8-15

### Month 3: Monetization
- 12+ videos published
- Apply for YouTube Partner Program
- Start earning revenue
- Cost: $12-20

### Break-Even Point:
- 1,000 subscribers + 4,000 watch hours
- YouTube earnings: $50-500/month
- ROI: Positive by month 4-6

---

## 🛠️ TROUBLESHOOTING

### "FFmpeg not found"
```bash
sudo apt install ffmpeg -y
```

### "YouTube quota exceeded"
- Default: 10,000 quota/day
- Each upload: ~1,600 quota
- Max: 6 uploads/day
- Solution: Request quota increase from Google

### "ElevenLabs voice sounds robotic"
- Use "eleven_turbo_v2" model
- Adjust stability/clarity sliders
- Add pauses with "..." in script

### "Video gets flagged as spam"
- Add more original commentary
- Use unique footage combinations
- Engage with early comments
- Post consistently (not in bursts)

---

## 🔗 API DOCUMENTATION

- [OpenAI](https://platform.openai.com/docs)
- [ElevenLabs](https://elevenlabs.io/docs)
- [Google Cloud TTS](https://cloud.google.com/text-to-speech/docs)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Pexels API](https://www.pexels.com/api/)
- [DALL-E 3](https://platform.openai.com/docs/guides/images)
- [FFmpeg](https://ffmpeg.org/documentation.html)

---

## 📊 ANALYTICS & OPTIMIZATION

Track these metrics:
- CTR (Click-Through Rate): Target 5-8%
- AVD (Average View Duration): Target 50%+
- Engagement (likes/comments): Target 2-4%

Optimize:
- Test 3 thumbnail variants
- A/B test video titles
- Analyze top-performing topics
- Adjust script length based on retention

---

## ⚡ ADVANCED FEATURES (Coming Soon)

- [ ] A/B thumbnail testing
- [ ] SEO keyword research
- [ ] Competitor analysis
- [ ] Batch video generation
- [ ] YouTube Shorts automation
- [ ] Multi-language support
- [ ] Analytics dashboard

---

## 📄 LICENSE

MIT License - Use at your own risk. Always comply with YouTube ToS.

---

## 💬 SUPPORT

Issues? Questions? Improvements?
- Open an issue on GitHub
- Or modify the code - it's yours!

---

**Built with ❤️ for content creators who want to scale**
