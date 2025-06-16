# Day 62: AI Movie Plot Generator 🎬

## Overview
A Python tool that generates movie pitches from 2-3 keywords (e.g., `love, horror, travel`). Creates a title, plot, genre prediction, and poster, saving output as JSON and PNG. Built for a 100-day AI learning journey.

## Features
- **Input**: 2-3 keywords via CLI.
- **Title**: Catchy names like "Lost Heart Love".
- **Plot**: Template-based stories blending keywords with transitions.
- **Genre**: Predicts top 2 genres (e.g., "Horror (82%), Romance (15%)").
- **Poster**: 400x600 image with `picsum.photos` background, dynamic font, and tagline.
- **Output**: Saves `movie_pitch.json` and `poster_<title>.png` in `day_62`.
- **Preview**: Auto-opens poster.

## Sample Output
```
🎥 Title: Lost Heart Love
🧠 Keywords: love, horror, travel
📜 Plot: Traveler falls for a mysterious stranger, but their romance faces a supernatural curse in a haunted town when a chilling cursed relic emerges. Their horror drives a climactic ritual.
🎯 Predicted Genre: Horror (82%), Romance (15%)
🖼️ Poster: C:\Users\uday kumar\Python-AI\ud-ai-journey\day_62\poster_lost_heart_love.png
```

## Setup
1. Save `movie_plot_generator.py` in `C:\Users\uday kumar\Python-AI\ud-ai-journey\day_62`.
2. Install dependencies:
   ```bash
   pip install scikit-learn Pillow requests
   ```
3. Ensure directory is writable:
   ```bash
   icacls "C:\Users\uday kumar\Python-AI\ud-ai-journey\day_62" /grant Everyone:F
   ```

## Usage
1. Run in PowerShell:
   ```bash
   cd "C:\Users\uday kumar\Python-AI\ud-ai-journey\day_62"
   & "C:/Users/uday kumar/AppData/Local/Programs/Python/Python312/python.exe" "movie_plot_generator.py"
   ```
2. Enter 2-3 keywords (e.g., `love, horror, travel`).
3. Check `day_62` for `movie_pitch.json` and `poster_<title>.png`.

## Notes
- **Plot Variation**: Random templates create different plots for the same keywords. Use `random.seed(42)` for consistency.
- **Fallback**: Gradient poster if `picsum.photos` fails.

## Future Enhancements
- Scrape IMDB for better genre classification.
- Build a Streamlit web UI.
- Add voice input or trailer text.

## Troubleshooting
- **Files Missing**: Check permissions or run PowerShell as Admin:
  ```bash
  Start-Process powershell -Verb runAs
  ```
- **Poster Issues**: Verify `Pillow` and internet connection.

---
## ❤️ Credits

Built with curiosity and love for movies!
--- 
**June 16, 2025**