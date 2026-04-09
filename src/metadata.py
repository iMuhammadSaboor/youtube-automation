"""
YouTube Metadata Generator
Generates optimized title, description, tags, and hashtags.
Auto-detects niche for relevant SEO optimization.

Author: Muhammad Saboor
"""

import os

OUTPUT_DIR = "C:/Users/ashai/OneDrive/Desktop/YouTube Videos"


def detect_niche(topic):
    """Detect content niche from topic keywords."""
    t = topic.lower()
    if any(w in t for w in ["ocean", "sea", "underwater", "deep", "marine"]):
        return "ocean"
    if any(w in t for w in ["space", "universe", "cosmic", "star", "planet", "galaxy"]):
        return "space"
    if any(w in t for w in ["unsolved", "mystery", "crime", "disappear", "missing"]):
        return "unsolved"
    if any(w in t for w in ["ancient", "discover", "ruins", "pyramid", "archaeol"]):
        return "ancient"
    return "general"


NICHE_META = {
    "ancient": {
        "desc": "mysterious and unexplained discoveries from the ancient world. From impossible engineering feats to artifacts that defy modern science, these findings continue to puzzle researchers and historians.",
        "tags": [
            "ancient discoveries", "ancient history", "archaeology",
            "ancient civilizations", "ancient technology", "history documentary",
            "ancient mysteries", "lost civilizations", "ancient artifacts",
        ],
        "hashtags": "#AncientMysteries #Archaeology #History #Documentary",
    },
    "ocean": {
        "desc": "most terrifying and unexplained discoveries from the depths of our oceans. From bizarre deep-sea creatures to structures that should not exist, the ocean holds secrets we are only beginning to uncover.",
        "tags": [
            "ocean mysteries", "deep sea", "underwater discoveries",
            "ocean documentary", "marine mysteries", "deep ocean",
            "underwater exploration", "ocean floor", "sea creatures",
        ],
        "hashtags": "#OceanMysteries #DeepSea #Underwater #Documentary",
    },
    "space": {
        "desc": "most mind-blowing mysteries of the cosmos that science still cannot explain. From unexplained signals to invisible forces shaping the universe, space holds more questions than answers.",
        "tags": [
            "space mysteries", "universe", "cosmos", "astronomy",
            "space documentary", "cosmic mysteries", "space exploration",
            "astrophysics", "dark energy", "space facts",
        ],
        "hashtags": "#SpaceMysteries #Universe #Cosmos #Astronomy",
    },
    "unsolved": {
        "desc": "most chilling unsolved mysteries that continue to baffle investigators and researchers. These cases remain open, with no definitive answers despite decades of investigation.",
        "tags": [
            "unsolved mysteries", "true crime", "cold cases",
            "unexplained events", "mystery documentary", "unsolved cases",
            "strange disappearances", "crime documentary", "investigation",
        ],
        "hashtags": "#UnsolvedMysteries #TrueCrime #Unexplained #Mystery",
    },
    "general": {
        "desc": "most fascinating mysteries and discoveries that challenge everything we thought we knew. These mind-blowing facts will leave you questioning reality.",
        "tags": [
            "mysteries", "unexplained", "facts", "documentary",
            "mind blowing", "education", "discovery", "unknown",
        ],
        "hashtags": "#Mysteries #Facts #Documentary #Education",
    },
}


def generate_metadata(topic, scenes, safe_topic):
    """Generate optimized YouTube title, description, and tags."""
    print("\nGenerating YouTube metadata...")

    niche = detect_niche(topic)
    meta = NICHE_META.get(niche, NICHE_META["general"])
    print(f"  Niche: {niche}")

    title = topic

    section_titles = [s["title"] for s in scenes if s["type"] == "section"]

    # Build timestamps from word counts
    timestamps = []
    current_time = 0
    for scene in scenes:
        mins = current_time // 60
        secs = current_time % 60
        timestamps.append(f"{mins}:{secs:02d} {scene['title']}")
        words = len(scene["narration"].split())
        current_time += int(words / 2.5)  # ~150 wpm

    description = f"""{topic}

In this video, we explore the {meta['desc']}

TIMESTAMPS:
{chr(10).join(timestamps)}

TOPICS COVERED:
{chr(10).join(f'- {t}' for t in section_titles)}

If you enjoyed this video, please LIKE, SUBSCRIBE, and hit the BELL for more content like this!

{meta['hashtags']}

DISCLAIMER: This video is for educational and entertainment purposes only. All footage is sourced from royalty-free stock video libraries."""

    # Build tag list
    tags = [topic.lower(), "documentary", "educational"]
    tags.extend(meta["tags"])
    for t in section_titles:
        tags.append(t.lower())

    # Save metadata file
    metadata_path = os.path.join(OUTPUT_DIR, f"{safe_topic}_metadata.txt")
    with open(metadata_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("YOUTUBE UPLOAD METADATA\n")
        f.write("Copy-paste each section into YouTube Studio\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"TITLE:\n{title}\n\n")
        f.write(f"DESCRIPTION:\n{description}\n\n")
        f.write(f"TAGS (comma separated):\n{', '.join(tags)}\n\n")
        f.write("CATEGORY: Education\n")
        f.write("VISIBILITY: Public\n")

    print(f"  Metadata saved: {metadata_path}")
    print(f"  Tags: {len(tags)}")
    return {"title": title, "description": description, "tags": tags}
