"""
Stock Footage Downloader
Downloads free HD stock videos from Pexels API.
- Multiple search query variations per scene
- Smart quality filtering (prefers HD, landscape, 10-60s)
- Automatic retry on failure
- Free API: https://www.pexels.com/api/

Author: Muhammad Saboor
"""

import os
import json
import requests

FOOTAGE_DIR = "C:/Users/ashai/OneDrive/Desktop/YouTube Videos/footage"
os.makedirs(FOOTAGE_DIR, exist_ok=True)

PEXELS_API_KEY = os.environ.get(
    "PEXELS_API_KEY",
    "EtVbiQuEYMalKR7MNeCZg5B0hUGDTIX3uS7WYDOpyQddIDVqZP6TU8BD",
)
PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"


def score_video_file(video, video_file):
    """Score a video file by quality, resolution, and duration."""
    score = 0
    w = video_file.get("width", 0)
    h = video_file.get("height", 0)
    quality = video_file.get("quality", "")
    duration = video.get("duration", 0)

    # Resolution scoring
    if quality == "hd" and w >= 1920:
        score += 10
    elif quality == "hd" and w >= 1280:
        score += 7
    elif w >= 1280:
        score += 5
    elif w >= 640:
        score += 2

    # Landscape preferred
    if w > h:
        score += 3

    # Ideal duration: 10-60 seconds
    if 10 <= duration <= 60:
        score += 5
    elif 5 <= duration <= 90:
        score += 2

    return score


def search_pexels_video(query, headers):
    """Search Pexels for the best matching video."""
    try:
        params = {
            "query": query,
            "per_page": 10,
            "orientation": "landscape",
            "size": "large",
        }
        response = requests.get(
            PEXELS_VIDEO_URL, headers=headers, params=params, timeout=15
        )
        response.raise_for_status()
        data = response.json()

        if "videos" not in data or not data["videos"]:
            return None, None

        # Find the best video + file combo
        best_video = None
        best_file = None
        best_score = -1

        for video in data["videos"][:5]:
            for vf in video.get("video_files", []):
                s = score_video_file(video, vf)
                if s > best_score:
                    best_score = s
                    best_video = video
                    best_file = vf

        return best_video, best_file

    except Exception as e:
        print(f"      Search error: {e}")
        return None, None


def download_file(url, filepath, max_retries=3):
    """Download a file with retry logic."""
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, stream=True, timeout=60)
            resp.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(chunk_size=16384):
                    f.write(chunk)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"      Retry {attempt + 1}...")
            else:
                print(f"      Download failed after {max_retries} attempts: {e}")
    return False


def download_footage(scenes, output_dir=FOOTAGE_DIR):
    """Download stock footage for each scene."""
    print("\nDownloading stock footage...")

    if not PEXELS_API_KEY:
        print("  WARNING: No Pexels API key found.")
        print("  Get a free key at: https://www.pexels.com/api/")
        print("  Set it: set PEXELS_API_KEY=your_key_here")
        return generate_placeholder_list(scenes, output_dir)

    headers = {"Authorization": PEXELS_API_KEY}
    downloaded = []

    for scene in scenes:
        query = scene["footage_query"]
        scene_num = scene["scene_num"]
        print(f"  Scene {scene_num}: Searching '{query}'...")

        # Try multiple query variations for better results
        queries = [
            query + " cinematic",
            query + " dramatic dark",
            query,
        ]

        video_found = False
        for q in queries:
            if video_found:
                break

            best_video, best_file = search_pexels_video(q, headers)

            if best_video and best_file:
                video_url = best_file["link"]
                filename = f"scene_{scene_num:02d}.mp4"
                filepath = os.path.join(output_dir, filename)
                dur = best_video.get("duration", "?")
                res = f"{best_file.get('width', '?')}x{best_file.get('height', '?')}"

                print(f"    Downloading {filename} ({dur}s, {res})...")

                if download_file(video_url, filepath):
                    downloaded.append({
                        "scene_num": scene_num,
                        "file": filepath,
                        "source": f"Pexels: {best_video.get('url', '')}",
                        "duration": best_video.get("duration", 0),
                        "query": q,
                    })
                    video_found = True
                    print(f"    OK: {filename}")

        if not video_found:
            print(f"    No footage found for scene {scene_num}")

    print(f"\n  Downloaded {len(downloaded)}/{len(scenes)} clips to {output_dir}/")
    return downloaded


def generate_placeholder_list(scenes, output_dir):
    """Generate a manual download list when no API key is set."""
    placeholder = []
    print("\n  FOOTAGE DOWNLOAD LIST (manual):")
    print("  Go to pexels.com/videos and search for these:\n")

    for scene in scenes:
        entry = {
            "scene_num": scene["scene_num"],
            "search_query": scene["footage_query"],
            "file": os.path.join(output_dir, f"scene_{scene['scene_num']:02d}.mp4"),
            "source": "manual_download",
        }
        placeholder.append(entry)
        print(f"  Scene {scene['scene_num']}: Search '{scene['footage_query']}'")
        print(f"           Save as: scene_{scene['scene_num']:02d}.mp4")

    list_path = os.path.join(output_dir, "footage_list.json")
    with open(list_path, "w") as f:
        json.dump(placeholder, f, indent=2)

    print(f"\n  Footage list saved to: {list_path}")
    print(f"  Download clips manually and place in: {output_dir}/")

    return placeholder
