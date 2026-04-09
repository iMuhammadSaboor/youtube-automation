"""
YouTube Faceless Video Pipeline
One command = one complete video ready to upload.

Supports 4 niches: Ancient, Ocean, Space, Unsolved
Auto-detects niche from topic keywords.

Usage:
    python video_pipeline.py --topic "7 IMPOSSIBLE Ancient Discoveries"
    python video_pipeline.py --topic "10 Scariest Ocean Discoveries" --voice male_uk
    python video_pipeline.py --topic "5 Space Mysteries" --fast
    python video_pipeline.py --topic "7 Unsolved Mysteries" --skip-footage --skip-video

Author: Muhammad Saboor
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from script_generator import generate_script
from footage_downloader import download_footage
from voiceover import generate_voiceover
from thumbnail import create_thumbnail
from metadata import generate_metadata

BASE_DIR = "C:/Users/ashai/OneDrive/Desktop/YouTube Videos"


def run_pipeline(topic, voice="narrator", skip_video=False, skip_footage=False, fast=False):
    """Run the full video production pipeline."""
    start = time.time()

    print("=" * 65)
    print("  YOUTUBE FACELESS VIDEO PIPELINE")
    print("=" * 65)
    print(f"  Topic:  {topic}")
    print(f"  Voice:  {voice}")
    print(f"  Fast:   {fast}")
    print("=" * 65)

    # ── Step 1: Script ──────────────────────────────────────────
    print("\n" + "-" * 55)
    print("[1/6] GENERATING SCRIPT")
    print("-" * 55)
    script, scenes, safe_topic = generate_script(topic)

    # ── Step 2: Footage ─────────────────────────────────────────
    print("\n" + "-" * 55)
    print("[2/6] DOWNLOADING FOOTAGE")
    print("-" * 55)
    if not skip_footage:
        footage = download_footage(scenes)
    else:
        print("  Skipped (--skip-footage)")
        footage = []

    # ── Step 3: Voiceover ───────────────────────────────────────
    print("\n" + "-" * 55)
    print("[3/6] GENERATING VOICEOVER")
    print("-" * 55)
    audio_path, scene_audios = generate_voiceover(scenes, voice_name=voice)

    # ── Step 4: Thumbnail ───────────────────────────────────────
    print("\n" + "-" * 55)
    print("[4/6] CREATING THUMBNAIL")
    print("-" * 55)
    thumb_path = create_thumbnail(
        topic,
        output_path=os.path.join(BASE_DIR, f"{safe_topic}_thumbnail.png"),
    )

    # ── Step 5: Metadata ────────────────────────────────────────
    print("\n" + "-" * 55)
    print("[5/6] GENERATING METADATA")
    print("-" * 55)
    meta = generate_metadata(topic, scenes, safe_topic)

    # ── Step 6: Video Assembly ──────────────────────────────────
    print("\n" + "-" * 55)
    print("[6/6] ASSEMBLING VIDEO")
    print("-" * 55)
    video_path = None
    if not skip_video:
        try:
            from video_editor import assemble_video
            video_path = assemble_video(scenes, audio_path, footage, safe_topic, fast_mode=fast)
        except Exception as e:
            print(f"  Video assembly error: {e}")
            print("  Script, audio, thumbnail, and metadata are still available.")
    else:
        print("  Skipped (--skip-video)")

    # ── Summary ─────────────────────────────────────────────────
    elapsed = time.time() - start
    print("\n" + "=" * 65)
    print("  PIPELINE COMPLETE!")
    print("=" * 65)
    print(f"  Time: {elapsed:.0f}s ({elapsed / 60:.1f} min)")
    print()
    print(f"  OUTPUT FILES (all in {BASE_DIR}):")
    print(f"  {'Script:':<14} scripts/{safe_topic}.txt")
    print(f"  {'Scenes:':<14} scripts/{safe_topic}_scenes.json")
    print(f"  {'Audio:':<14} audio/full_narration.mp3")
    print(f"  {'Thumbnail:':<14} {safe_topic}_thumbnail.png")
    print(f"  {'Metadata:':<14} {safe_topic}_metadata.txt")
    if video_path:
        print(f"  {'Video:':<14} {os.path.basename(video_path)}")
    print()
    print("  NEXT STEPS:")
    print("  1. Review the script and listen to the audio")
    if video_path:
        print("  2. Upload video to YouTube")
        print("  3. Upload thumbnail")
        print(f"  4. Paste metadata from {safe_topic}_metadata.txt")
    else:
        if skip_video:
            print("  2. Run again without --skip-video to assemble the video")
        else:
            print("  2. Check the error above, then re-run the pipeline")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="YouTube Faceless Video Pipeline - One command, one video.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported niches (auto-detected from topic):
  Ancient   "7 IMPOSSIBLE Ancient Discoveries"
  Ocean     "10 Scariest Ocean Discoveries"
  Space     "5 Mind-Blowing Space Mysteries"
  Unsolved  "7 Unsolved Mysteries That Still Haunt Us"

Examples:
  python video_pipeline.py --topic "7 IMPOSSIBLE Ancient Discoveries"
  python video_pipeline.py --topic "10 Scariest Ocean Discoveries" --voice male_uk
  python video_pipeline.py --topic "5 Space Mysteries" --fast
  python video_pipeline.py --topic "7 Unsolved Mysteries" --skip-footage --skip-video
        """,
    )
    parser.add_argument("--topic", type=str, required=True, help="Video topic")
    parser.add_argument(
        "--voice", type=str, default="narrator",
        choices=["narrator", "male_us", "male_uk", "male_au",
                 "female_us", "female_uk", "male_deep"],
        help="Voice for narration (default: narrator)",
    )
    parser.add_argument("--skip-video", action="store_true", help="Skip video assembly")
    parser.add_argument("--skip-footage", action="store_true", help="Skip footage download")
    parser.add_argument("--fast", action="store_true",
                        help="Fast mode: skip Ken Burns effects for quicker rendering")

    args = parser.parse_args()
    run_pipeline(
        args.topic,
        voice=args.voice,
        skip_video=args.skip_video,
        skip_footage=args.skip_footage,
        fast=args.fast,
    )


if __name__ == "__main__":
    main()
