# AI-Powered YouTube Video Production Pipeline

Fully automated end-to-end video production system that generates complete YouTube videos from a single topic input.

## What It Does

```
Input:  "7 Impossible Ancient Discoveries"
Output: Complete video + thumbnail + metadata (ready to upload)
```

## Pipeline Stages

1. **Script Generation** — OpenAI API generates structured narration scripts with scene breakdowns
2. **Footage Sourcing** — Pexels API finds HD stock footage with quality scoring and retry logic
3. **Voiceover Synthesis** — Edge TTS generates narration with dramatic pauses and scene-type pacing
4. **Video Assembly** — MoviePy composites footage with Ken Burns zoom/pan effects, crossfade transitions, letterbox bars, and animated title cards
5. **Thumbnail Generation** — Pillow creates thumbnails with RGBA compositing, gradient overlays, glow effects, and niche-specific colour schemes
6. **SEO Metadata** — Auto-generates titles, descriptions, tags, and hashtags optimised per niche

## Supported Niches

| Niche | Example Topics |
|-------|---------------|
| Ancient | "7 Impossible Ancient Discoveries We Can't Explain" |
| Ocean | "5 Mind-Blowing Ocean Discoveries" |
| Space | "5 Mind-Blowing Space Mysteries" |
| Unsolved | "6 Unsolved Mysteries That Baffle Scientists" |

## Tech Stack

- **Python** — Core language
- **OpenAI API** — Script generation
- **Pexels API** — Stock footage sourcing
- **Edge TTS** — Text-to-speech voiceover
- **MoviePy v2** — Video editing and compositing
- **Pillow** — Thumbnail and image generation

## Usage

```bash
pip install -r requirements.txt
python video_pipeline.py --topic "7 Impossible Ancient Discoveries"
```

### CLI Options

| Flag | Description |
|------|-------------|
| `--topic` | Video topic (required) |
| `--voice` | TTS voice selection |
| `--fast` | Use ultrafast encoding preset |
| `--skip-video` | Generate script/audio only |
| `--skip-footage` | Skip footage download |

## Architecture

```
video_pipeline.py          # CLI entry point
src/
├── script_generator.py    # OpenAI script generation + niche detection
├── footage_downloader.py  # Pexels API with quality scoring + retry
├── voiceover.py           # Edge TTS with dramatic pacing
├── video_editor.py        # MoviePy compositing + Ken Burns effect
├── thumbnail.py           # Pillow thumbnail generation
└── metadata.py            # SEO metadata generation
```

## Author

**Muhammad Saboor** — Melbourne, VIC
