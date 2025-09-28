
---

# 🎤 Speech Segmentation Script

A Python tool that processes audio or video files to **detect speech**, log timestamps, and export the identified segments into individual audio clips.

---

## 🚀 Core Features

* **Audio Extraction & Standardization**
  Extracts audio from media files and converts it to a standard format (`.wav`, 16 kHz, mono).

* **Speech Detection**
  Analyzes audio to identify speech activity using silence detection.

* **Timestamp Logging**
  Stores detected timestamps in a structured `speech_timestamps.json` file.

* **Audio Segmentation**
  Splits the standardized audio into smaller clips based on detected speech events.

---

## ⚙️ How to Run

### 1. Prerequisites

* Python 3.7+
* **FFmpeg** (must be installed and accessible in your system’s PATH):

  * macOS/Linux → install via `brew` / `apt-get`
  * Windows → [Download FFmpeg](https://ffmpeg.org/download.html) and add the `bin/` folder to PATH

### 2. Setup & Execution

```bash
# 1. Create and activate a virtual environment
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the script
python main.py vid.mp4 ./<output_folder>
```

---

## 📂 Output Structure

```
<output_folder>/
├── standardized_audio.wav   # Full standardized audio track
├── speech_timestamps.json   # JSON file with start/end times
└── segmented_clips/         # Individual speech clips
    ├── segment_01.wav
    ├── segment_02.wav
    └── ...
```

---

## 📊 Performance Tuning & Final Analysis

The script was tested on a **1:41 minute anime clip**.

* **V1 (Initial run)** produced a working baseline but with issues.
* **V2 (Tuned run)** gave much more accurate segmentation.

Below is the detailed evaluation:

---

### 🔎 Initial Analysis of Segmentation Results (V1)

*Parameters: `min_silence_len=500`, `silence_thresh=-40`*

| Segment File     | Timestamp      | Description                       | Quality                |
| :--------------- | :------------- | :-------------------------------- | :--------------------- |
| `segment_01.wav` | `1.54–5.52`    | scratching sounds                 | Fine                   |
| `segment_02.wav` | `6.37–9.17`    | eerie sound effect                | Clear                  |
| `segment_04.wav` | `23.01–23.82`  | <1 sec scratch                    | **Bad (Fragmented)**   |
| `segment_05.wav` | `25.43–26.24`  | "METOO"                           | **Bad (Missed prior)** |
| `segment_06.wav` | `30.56–30.98`  | part of longer dialogue           | **Bad (Fragmented)**   |
| `segment_07.wav` | `32.72–35.15`  | "is this because of my leg?"      | Clear                  |
| `segment_09.wav` | `38.31–42.11`  | "we can fix it, I can fix it all" | Clear                  |
| `segment_17.wav` | `65.41–101.44` | 36s of background music           | **Redundant**          |

**Findings (V1):**

* ❌ Fragmented speech (conversations split into multiple clips).
* ❌ Missed quiet sound effects.
* ❌ Generated redundant, non-speech clips.

---

### 🔧 Tuned Segmentation Results (V2)

*Parameters: `min_silence_len=700`, `silence_thresh=-50`*

| Segment File     | Timestamp     | Description               | Quality                     |
| :--------------- | :------------ | :------------------------ | :-------------------------- |
| `segment_01.wav` | `1.54–5.52`   | scratching captured fully | Clear                       |
| `segment_02.wav` | `6.37–19.11`  | siren sound               | **Clear (merged properly)** |
| `segment_03.wav` | `21.36–26.24` | scratching sound          | Clear                       |
| `segment_08.wav` | `39.52–52.09` | dialogues back and forth  | **Massive improvement**     |
| `segment_09.wav` | `52.6–58.0`   | "let’s throw this away…"  | Clear                       |
| `segment_12.wav` | `62.4–101.44` | dialogue + noise tail     | Clear (minor redundancy)    |

**Improvements (V2):**

* ✅ Fragmentation solved (8 clips merged into 1 coherent dialogue).
* ✅ Quiet effects captured successfully.
* ✅ Reduced redundancy & improved logical cohesion.

---

## ✅ Conclusion

The **tuned segmentation** produced a more accurate and coherent set of clips.

* Speech is **less fragmented**.
* Important but quiet sounds are **captured**.
* Redundant segments are **minimized**.

👉 The trade-off: slight over-sensitivity capturing faint background noise — but the gains in dialogue accuracy far outweigh this.

---

## 📌 Note

Since this internship centers around **anime/manga**, here’s another project of mine:

📖 **MangaVerse – A Manga Discovery App**
🔗 [GitHub Repository](https://github.com/vansh212121/MangaVerse)

---
