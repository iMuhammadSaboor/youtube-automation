"""
AI Voiceover Generator
Uses Edge TTS (Microsoft) - completely FREE, no API key needed.
Generates natural-sounding narration with dramatic pacing.

Author: Muhammad Saboor
"""

import asyncio
import os
import edge_tts

AUDIO_DIR = "C:/Users/ashai/OneDrive/Desktop/YouTube Videos/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Voice options (all free, no API key)
VOICES = {
    "narrator": "en-US-GuyNeural",            # Best for documentary narration
    "male_us": "en-US-GuyNeural",             # American male
    "male_uk": "en-GB-RyanNeural",            # British male
    "male_au": "en-AU-WilliamNeural",         # Australian male
    "female_us": "en-US-JennyNeural",         # American female
    "female_uk": "en-GB-SoniaNeural",         # British female
    "male_deep": "en-US-ChristopherNeural",   # Deep dramatic male
}

# Pacing per scene type - slower = more dramatic
PACING = {
    "intro": {"rate": "-8%", "pitch": "+0Hz"},
    "section": {"rate": "-5%", "pitch": "+0Hz"},
    "outro": {"rate": "-3%", "pitch": "+0Hz"},
}


async def _generate_audio(text, output_path, voice="en-US-GuyNeural", rate="-5%", pitch="+0Hz"):
    """Generate TTS audio from text."""
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)


def add_dramatic_pauses(text):
    """Insert natural pauses for cinematic narration feel."""
    # Longer pauses after sentences
    text = text.replace(". ", ". ... ")
    text = text.replace("? ", "? ... ")
    text = text.replace("! ", "! ... ")

    # Dramatic pause before reveal/contrast words
    dramatic = [
        "but", "however", "yet", "incredibly", "remarkably",
        "astonishingly", "mysteriously", "the truth is",
        "the answer", "the problem", "even more", "despite",
        "what makes", "the most", "no one", "to this day",
    ]
    for word in dramatic:
        text = text.replace(f" {word} ", f" ... {word} ")
        cap = word[0].upper() + word[1:]
        text = text.replace(f" {cap} ", f" ... {cap} ")

    return text


def generate_voiceover(scenes, voice_name="narrator", output_dir=AUDIO_DIR):
    """Generate voiceover audio for each scene and full narration."""
    print("\nGenerating AI voiceover...")

    voice = VOICES.get(voice_name, VOICES["narrator"])
    print(f"  Voice: {voice}")

    # ── Build full narration with dramatic pacing ──
    full_narration = ""
    for scene in scenes:
        text = scene["narration"]

        if scene["type"] == "intro":
            full_narration += text + " ...... "
        elif scene["type"] == "section":
            full_narration += (
                f"Number {scene['scene_num']}. ... {scene['title']}. ...... "
            )
            full_narration += add_dramatic_pauses(text) + " ...... "
        elif scene["type"] == "outro":
            full_narration += " ...... " + text

    # Generate full narration MP3
    full_path = os.path.join(output_dir, "full_narration.mp3")
    print("  Generating full narration...")

    pacing = PACING["section"]
    asyncio.run(
        _generate_audio(full_narration, full_path, voice,
                        rate=pacing["rate"], pitch=pacing["pitch"])
    )
    print(f"  Full narration: {full_path}")

    # ── Generate individual scene audio (for flexible editing) ──
    scene_paths = []
    for scene in scenes:
        scene_path = os.path.join(output_dir, f"scene_{scene['scene_num']:02d}.mp3")
        text = scene["narration"]

        if scene["type"] == "section":
            text = f"{scene['title']}. ...... {add_dramatic_pauses(text)}"

        pacing = PACING.get(scene["type"], PACING["section"])

        asyncio.run(
            _generate_audio(text, scene_path, voice,
                            rate=pacing["rate"], pitch=pacing["pitch"])
        )
        scene_paths.append(scene_path)
        print(f"  Scene {scene['scene_num']} audio saved")

    total = len(scene_paths) + 1
    print(f"\n  Generated {total} audio files in {output_dir}/")
    return full_path, scene_paths


async def list_voices():
    """List all available English voices."""
    voices = await edge_tts.list_voices()
    english = [v for v in voices if v["Locale"].startswith("en-")]
    for v in english:
        print(f"  {v['ShortName']:35s} | {v['Gender']:8s} | {v['Locale']}")


if __name__ == "__main__":
    test_scenes = [
        {
            "scene_num": 0, "type": "intro", "title": "Intro",
            "narration": "What if everything we thought we knew about ancient history was wrong?",
        },
        {
            "scene_num": 1, "type": "section", "title": "The Great Pyramid",
            "narration": "Standing for over 4,500 years, the Great Pyramid remains one of the most precisely engineered structures ever built.",
        },
    ]
    generate_voiceover(test_scenes)
