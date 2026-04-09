"""
Professional Video Editor & Assembler
Creates cinematic faceless YouTube videos with:
- Ken Burns (slow zoom / pan) effect on all footage
- Crossfade transitions between scenes
- Cinematic letterbox bars (top + bottom)
- Animated section title overlays with accent card
- Proportional scene timing based on narration length
- 1080p @ 30fps output

Author: Muhammad Saboor
"""

import os
import random
import numpy as np
from PIL import Image as PILImage, ImageDraw, ImageFont
from moviepy import *

OUTPUT_DIR = "C:/Users/ashai/OneDrive/Desktop/YouTube Videos"
FOOTAGE_DIR = "C:/Users/ashai/OneDrive/Desktop/YouTube Videos/footage"
AUDIO_DIR = "C:/Users/ashai/OneDrive/Desktop/YouTube Videos/audio"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Video settings
WIDTH = 1920
HEIGHT = 1080
FPS = 30
LETTERBOX = 50          # Black bar height (top + bottom)
TRANSITION = 0.8        # Crossfade duration in seconds

# Ken Burns effect options
KB_EFFECTS = ["zoom_in", "zoom_out", "pan_left", "pan_right"]


# ── Ken Burns Effect ─────────────────────────────────────────────


def apply_ken_burns(clip, target_w=WIDTH, target_h=HEIGHT, effect=None):
    """
    Apply cinematic Ken Burns (slow zoom / pan) effect to a clip.
    Uses VideoClip(make_frame) for maximum compatibility.
    """
    if effect is None:
        effect = random.choice(KB_EFFECTS)

    try:
        duration = clip.duration

        # Scale clip to 130% of target so there's room to zoom / pan
        scale = 1.3
        clip = clip.resized(height=int(target_h * scale))
        if clip.w < int(target_w * scale):
            clip = clip.resized(width=int(target_w * scale))

        source = clip

        def make_frame(t):
            frame = source.get_frame(t)
            h, w = frame.shape[:2]
            progress = t / max(duration, 0.01)

            # Zoom factor
            if effect == "zoom_in":
                zoom = 1.0 + 0.25 * progress
            elif effect == "zoom_out":
                zoom = 1.25 - 0.25 * progress
            else:
                zoom = 1.1

            crop_w = min(int(target_w * scale / zoom), w)
            crop_h = min(int(target_h * scale / zoom), h)

            # Pan offset
            if effect == "pan_right":
                cx = int(w * (0.35 + 0.3 * progress))
            elif effect == "pan_left":
                cx = int(w * (0.65 - 0.3 * progress))
            else:
                cx = w // 2
            cy = h // 2

            x1 = max(0, min(cx - crop_w // 2, w - crop_w))
            y1 = max(0, min(cy - crop_h // 2, h - crop_h))

            cropped = frame[y1 : y1 + crop_h, x1 : x1 + crop_w]

            if cropped.shape[0] < 2 or cropped.shape[1] < 2:
                return np.zeros((target_h, target_w, 3), dtype=np.uint8)

            img = PILImage.fromarray(cropped)
            img = img.resize((target_w, target_h), PILImage.LANCZOS)
            return np.array(img)

        new_clip = VideoClip(make_frame, duration=duration).with_fps(FPS)

        if source.audio:
            new_clip = new_clip.with_audio(source.audio)
        return new_clip

    except Exception as e:
        print(f"    Ken Burns failed ({e}), using simple resize")
        return clip.resized((target_w, target_h))


# ── Title Overlay ────────────────────────────────────────────────


def create_section_title(number, title, duration, target_w=WIDTH, target_h=HEIGHT):
    """Create an animated title card overlay for a section."""
    img = PILImage.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Card position and size
    card_x = 50
    card_y = target_h - 195
    card_w = 700
    card_h = 115

    # Semi-transparent background with gradient
    for i in range(card_h):
        alpha = int(185 - 35 * (i / card_h))
        draw.line(
            [(card_x, card_y + i), (card_x + card_w, card_y + i)],
            fill=(8, 8, 25, alpha),
        )

    # Red accent bar on left edge
    draw.rectangle(
        [(card_x, card_y), (card_x + 5, card_y + card_h)],
        fill=(220, 40, 40, 255),
    )

    # Fonts
    try:
        font_num = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 44)
        font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
    except (OSError, IOError):
        font_num = ImageFont.load_default()
        font_title = ImageFont.load_default()

    # Number
    draw.text(
        (card_x + 22, card_y + 12), f"#{number}",
        fill=(220, 40, 40, 255), font=font_num,
    )

    # Title (truncate if needed)
    display = title.upper()
    if len(display) > 38:
        display = display[:35] + "..."
    draw.text(
        (card_x + 22, card_y + 64), display,
        fill=(255, 255, 255, 240), font=font_title,
    )

    # Convert RGBA to clip + mask
    frame = np.array(img)
    rgb = frame[:, :, :3]
    alpha = frame[:, :, 3].astype(float) / 255.0

    show_for = min(4.5, duration)
    clip = ImageClip(rgb).with_duration(show_for)
    mask = ImageClip(alpha, is_mask=True).with_duration(show_for)
    clip = clip.with_mask(mask)
    clip = clip.with_start(1.0)  # Slight delay before appearing

    try:
        clip = clip.with_effects([vfx.CrossFadeIn(0.5), vfx.CrossFadeOut(0.8)])
    except Exception:
        pass

    return clip


# ── Placeholder ──────────────────────────────────────────────────


def create_placeholder_clip(scene, duration):
    """Dark gradient placeholder when no footage is available."""
    img = PILImage.new("RGB", (WIDTH, HEIGHT), (10, 12, 25))
    draw = ImageDraw.Draw(img)

    for y in range(HEIGHT):
        r = int(10 + 18 * (y / HEIGHT))
        g = int(12 + 8 * (y / HEIGHT))
        b = int(25 + 30 * (y / HEIGHT))
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 54)
    except (OSError, IOError):
        font = ImageFont.load_default()

    title = scene.get("title", "")
    bbox = draw.textbbox((0, 0), title, font=font)
    tx = (WIDTH - (bbox[2] - bbox[0])) // 2
    ty = HEIGHT // 2 - 30

    for dx in range(-3, 4):
        for dy in range(-3, 4):
            draw.text((tx + dx, ty + dy), title, fill=(0, 0, 0), font=font)
    draw.text((tx, ty), title, fill=(255, 255, 255), font=font)

    frame = np.array(img)
    return ImageClip(frame).with_duration(duration).with_fps(FPS)


# ── Main assembly ────────────────────────────────────────────────


def assemble_video(scenes, audio_path, footage_files, safe_topic, fast_mode=False):
    """Assemble final video: footage + Ken Burns + transitions + titles + letterbox."""
    print("\nAssembling final video...")

    # Load narration
    narration = AudioFileClip(audio_path)
    total_duration = narration.duration
    print(f"  Narration: {total_duration:.1f}s ({total_duration / 60:.1f} min)")

    # Proportional scene durations (based on word count)
    total_words = sum(len(s["narration"].split()) for s in scenes)

    scene_clips = []
    current_time = 0.0

    for i, scene in enumerate(scenes):
        scene_num = scene["scene_num"]
        words = len(scene["narration"].split())
        scene_dur = max((words / total_words) * total_duration, 3.0)

        label = f"  Scene {scene_num} ({scene['type']}): {scene_dur:.1f}s"

        # ── Find footage file ──
        footage_path = None
        search_dirs = [
            FOOTAGE_DIR,
            "C:/Users/ashai/youtube-automation/footage",
        ]
        for d in search_dirs:
            p = os.path.join(d, f"scene_{scene_num:02d}.mp4")
            if os.path.exists(p):
                footage_path = p
                break

        if not footage_path and footage_files:
            for ff in footage_files:
                if isinstance(ff, dict) and ff.get("scene_num") == scene_num:
                    if os.path.exists(ff.get("file", "")):
                        footage_path = ff["file"]
                        break

        # ── Build clip ──
        if footage_path:
            clip = VideoFileClip(footage_path)

            # Loop if too short
            if clip.duration < scene_dur:
                loops = int(scene_dur / clip.duration) + 1
                clip = concatenate_videoclips([clip] * loops)

            clip = clip.subclipped(0, min(scene_dur, clip.duration))

            # Ken Burns
            if not fast_mode:
                kb = random.choice(KB_EFFECTS)
                clip = apply_ken_burns(clip, WIDTH, HEIGHT, kb)
                print(f"{label} [{kb}] - footage")
            else:
                clip = clip.resized((WIDTH, HEIGHT))
                print(f"{label} - footage (fast)")
        else:
            clip = create_placeholder_clip(scene, scene_dur)
            print(f"{label} - placeholder")

        # ── Section title overlay ──
        if scene["type"] == "section":
            title_clip = create_section_title(scene_num, scene["title"], scene_dur)
            clip = CompositeVideoClip([clip, title_clip], size=(WIDTH, HEIGHT))

        # ── Crossfade in ──
        if i > 0:
            try:
                clip = clip.with_effects([vfx.CrossFadeIn(TRANSITION)])
            except Exception:
                pass

        clip = clip.with_start(current_time)
        scene_clips.append(clip)

        overlap = TRANSITION if i < len(scenes) - 1 else 0
        current_time += scene_dur - overlap

    # ── Composite all scenes ──
    print("\n  Compositing scenes...")
    video = CompositeVideoClip(scene_clips, size=(WIDTH, HEIGHT))

    # ── Letterbox bars ──
    print("  Adding cinematic letterbox bars...")
    top_bar = (
        ColorClip((WIDTH, LETTERBOX), color=(0, 0, 0))
        .with_duration(video.duration)
    )
    bottom_bar = (
        ColorClip((WIDTH, LETTERBOX), color=(0, 0, 0))
        .with_duration(video.duration)
        .with_position(("center", HEIGHT - LETTERBOX))
    )
    video = CompositeVideoClip([video, top_bar, bottom_bar], size=(WIDTH, HEIGHT))

    # ── Audio ──
    audio_dur = min(video.duration, narration.duration)
    video = video.with_audio(narration.subclipped(0, audio_dur))

    # ── Export ──
    output_path = os.path.join(OUTPUT_DIR, f"{safe_topic}.mp4")
    print(f"\n  Exporting to: {output_path}")
    print("  This may take several minutes...")

    video.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=8,
        bitrate="8000k",
    )

    # Cleanup
    video.close()
    narration.close()
    for c in scene_clips:
        try:
            c.close()
        except Exception:
            pass

    file_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n  Final video: {output_path}")
    print(f"  Duration: {total_duration:.1f}s ({total_duration / 60:.1f} min)")
    print(f"  File size: {file_mb:.1f} MB")
    return output_path


if __name__ == "__main__":
    print("Video editor loaded. Run via: python video_pipeline.py --topic '...'")
