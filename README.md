# AI-Powered YouTube Video Production Pipeline

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?logo=openai)
![Status](https://img.shields.io/badge/Status-Working-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

> **One command = one complete YouTube video.** Fully automated pipeline from topic to upload-ready video with AI narration, stock footage, thumbnails, and SEO metadata.

---

## What It Does

```
Input:   python video_pipeline.py --topic "7 Impossible Ancient Discoveries"
Output:  Complete video (MP4) + thumbnail (PNG) + metadata (TXT)
         Ready to upload to YouTube
```

### Pipeline Stages

```
Topic Input
  --> Script Generation (OpenAI API)
  --> Stock Footage Sourcing (Pexels API, quality scoring)
  --> AI Voiceover (Edge TTS, dramatic pacing)
  --> Video Assembly (MoviePy, Ken Burns effects, transitions)
  --> Thumbnail Generation (Pillow, RGBA compositing, glow effects)
  --> SEO Metadata (title, description, tags, hashtags)
```

## Supported Niches

| Niche | Example Topics |
|-------|---------------|
| Ancient | "7 Impossible Ancient Discoveries We Can't Explain" |
| Ocean | "5 Mind-Blowing Ocean Discoveries" |
| Space | "5 Mind-Blowing Space Mysteries" |
| Unsolved | "6 Unsolved Mysteries That Baffle Scientists" |

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core pipeline |
| OpenAI API | Script generation |
| Pexels API | HD stock footage with quality scoring |
| Edge TTS | AI voiceover with dramatic pacing |
| MoviePy v2 | Video compositing, Ken Burns, crossfades |
| Pillow | Thumbnail with gradients and glow effects |

## CLI Options

| Flag | Description |
|------|-------------|
| `--topic` | Video topic (required) |
| `--voice` | TTS voice selection |
| `--fast` | Ultrafast encoding preset |
| `--skip-video` | Generate script/audio only |
| `--skip-footage` | Skip footage download |

## Architecture

```
video_pipeline.py          # CLI entry point - runs all stages
src/
├── script_generator.py    # OpenAI script generation + niche detection
├── footage_downloader.py  # Pexels API with quality scoring + retry
├── voiceover.py           # Edge TTS with dramatic pacing
├── video_editor.py        # MoviePy compositing + Ken Burns effect
├── thumbnail.py           # Pillow thumbnail generation
└── metadata.py            # SEO metadata generation
```

## Quick Start

```bash
pip install -r requirements.txt
python video_pipeline.py --topic "7 Impossible Ancient Discoveries"
```

## Key Design Decisions

- **Modular pipeline** - each stage has defined inputs/outputs, can run independently
- **Quality scoring** - footage is ranked by resolution, relevance, and duration before selection
- **Retry logic** - API failures don't crash the pipeline, they retry with fallbacks
- **Niche-aware** - colour schemes, pacing, and metadata adapt to content type

## Author

**Muhammad Saboor** — Melbourne, VIC
Final-year Bachelor of Data Science, Victoria University
[GitHub](https://github.com/iMuhammadSaboor) | bmuhammadsaboor@gmail.com
