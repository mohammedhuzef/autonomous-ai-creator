"""
AI Video Agent - Pipeline (Step 1-4)
--------------------------------------
Ye script kya karta hai:
1. YouTube se last 7 din ke most viewed Shorts dhoondta hai
2. Un videos ko Gemini 2.5 Pro ko bhejta hai analyze karne ke liye
3. Gemini se scene description + naye AI-generation prompts nikalta hai (image + video)

Agla step (Imagen + Kling) is JSON output ko input ke roop mein use karega.
"""

import requests
import json
import os
from datetime import datetime, timedelta
from google import genai
from google.genai import types
from dotenv import load_dotenv

# .env file se API keys load karo (isse keys code mein kabhi nahi likhni padtin)
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not YOUTUBE_API_KEY or not GEMINI_API_KEY:
    raise ValueError(
        "API keys nahi mili! '.env' file banao project folder mein "
        "(dekho .env.example) aur usme apni YOUTUBE_API_KEY aur GEMINI_API_KEY daalo."
    )

client = genai.Client(api_key=GEMINI_API_KEY)


def get_trending_shorts(max_results=5):
    """
    Last 7 din ke most viewed YouTube Shorts dhoondta hai.
    Returns: list of dicts jisme title aur url hai
    """
    published_after = (datetime.utcnow() - timedelta(days=30)).isoformat("T") + "Z"

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": "shorts",
        "type": "video",
        "order": "viewCount",
        "publishedAfter": published_after,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "error" in data:
        print("YouTube API Error:", data["error"]["message"])
        return []

    # DEBUG: agar items nahi mile to poora response dikhao
    if not data.get("items"):
        print("DEBUG - Full YouTube response:")
        print(json.dumps(data, indent=2))

    videos = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        yt_url = f"https://youtube.com/watch?v={video_id}"
        videos.append({"title": title, "url": yt_url})

    return videos


def analyze_video(youtube_url):
    """
    Gemini ko YouTube URL deta hai aur scene description +
    naye image/video prompts JSON format mein nikalta hai.
    """
    prompt = """
    Is video ko dekho aur SIRF JSON format mein reply do (koi extra text, koi markdown fences nahi):
    {
      "scenes": [
        {"description": "scene mein kya ho raha hai", "mood": "mood/tone"}
      ],
      "image_prompt": "ek naya, original image-generation prompt jo is video ke style/theme se inspired ho (copy nahi, sirf inspired). Prompt mein hamesha 'flat cartoon illustration style' explicitly likhna, koi bhi real insaan/child ki tarah dikhne wali photorealistic image nahi maangni.",
      "video_prompt": "ek chhota motion prompt jo bataye image kaise animate ho, 5 second clip ke liye"
    }
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=types.Content(
            parts=[
                types.Part(file_data=types.FileData(file_uri=youtube_url)),
                types.Part(text=prompt),
            ]
        ),
    )

    text = response.text.strip()
    # Kabhi kabhi Gemini ```json fences bhi bhej deta hai, unhe hata dete hain
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print("JSON parse nahi hua. Raw response ye tha:")
        print(text)
        return None


def generate_image(prompt, filename="generated_image.png"):
    """
    Pollinations AI se free mein image generate karta hai.
    Koi API key nahi chahiye - seedha URL se image mil jaati hai.
    """
    import urllib.parse

    # Style ko strongly enforce karte hain taaki cartoon/illustration hi bane, realistic nahi
    styled_prompt = (
        f"{prompt}, in the style of a flat vector cartoon illustration, "
        f"bold outlines, bright flat colors, Pixar-style character design, "
        f"digital illustration, not photorealistic, family-friendly animation art"
    )

    encoded_prompt = urllib.parse.quote(styled_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model=flux"

    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            return filename
        else:
            print(f"Image generation fail hui. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error image generate karte waqt: {e}")
        return None


def generate_video(image_path, output_path="output_video.mp4", duration=5, fps=24, zoom_amount=0.15):
    """
    Ken Burns effect: static image pe slow zoom-in animation, video mein convert karta hai.
    Koi external AI service nahi chahiye - sab locally compute hota hai.
    """
    try:
        from moviepy import VideoClip  # moviepy 2.x
    except ImportError:
        # pyrefly: ignore [missing-import]
        from moviepy.editor import VideoClip  # moviepy 1.x (fallback)
    from PIL import Image
    import numpy as np

    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    def make_frame(t):
        progress = t / duration
        scale = 1 + zoom_amount * progress  # dheere dheere zoom badhta hai
        new_w, new_h = int(w * scale), int(h * scale)
        resized = img.resize((new_w, new_h), Image.LANCZOS)
        # center se crop karke original size wapas laate hain
        left = (new_w - w) // 2
        top = (new_h - h) // 2
        cropped = resized.crop((left, top, left + w, top + h))
        return np.array(cropped)

    clip = VideoClip(make_frame, duration=duration)
    clip.write_videofile(output_path, fps=fps, codec="libx264", audio=False, logger=None)
    return output_path


def process_video(video, index):
    """Ek single video ko poori pipeline se guzarta hai: analyze -> image -> video"""
    print("=" * 60)
    print(f"VIDEO {index}: {video['title']}")
    print("=" * 60)

    result = analyze_video(video["url"])
    if not result:
        print(f"Video {index} skip kiya - Gemini se result nahi mila.\n")
        return None

    json_filename = f"output_{index}.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"JSON save ho gaya: {json_filename}")

    image_filename = f"generated_image_{index}.png"
    image_path = generate_image(result["image_prompt"], filename=image_filename)
    if not image_path:
        print(f"Video {index} - image generate nahi hui, video skip.\n")
        return None
    print(f"Image save ho gayi: {image_path}")

    video_filename = f"output_video_{index}.mp4"
    video_path = generate_video(image_path, output_path=video_filename)
    print(f"Video save ho gayi: {video_path}\n")

    return {"json": json_filename, "image": image_path, "video": video_path}


def main():
    print("STEP 1: Trending Shorts dhoondh raha hoon (last 30 din)...")
    print("-" * 50)
    shorts = get_trending_shorts()

    if not shorts:
        print("Koi video nahi mila. YouTube API key ya quota check karo.")
        return

    for i, v in enumerate(shorts, start=1):
        print(f"{i}. {v['title']}")
        print(f"   {v['url']}")

    print("\n" + "=" * 60)
    print(f"AB IN {len(shorts)} VIDEOS KO PIPELINE SE GUZAAR RAHA HOON")
    print("=" * 60 + "\n")

    results = []
    for i, video in enumerate(shorts, start=1):
        outcome = process_video(video, i)
        if outcome:
            results.append(outcome)

    print("=" * 60)
    print(f"DONE! {len(results)} / {len(shorts)} videos successfully process hue.")
    print("=" * 60)
    for r in results:
        print(f"  - {r['video']}")


if __name__ == "__main__":
    main()