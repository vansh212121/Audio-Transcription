Speech Segmentation Script
A Python script that processes an audio or video file to detect speech, log timestamps, and export the identified speech segments as individual audio clips.

Core Features
Audio Extraction & Standardization: Extracts audio from media files and converts it to a standard format (.wav, 16 kHz, mono).

Speech Detection: Analyzes audio to find the start and end times of speech activity using silence detection.

Timestamp Logging: Stores the detected timestamps in a structured speech_timestamps.json file.

Audio Segmentation: Splits the source audio into smaller clips based on the detected speech events.

How to Run
1. Prerequisites

Python 3.7+

ffmpeg: Must be installed and accessible in your system's PATH.

macOS/Linux: Use a package manager like brew or apt-get.

Windows: Download from the official FFmpeg website and add the bin folder to your PATH.

2. Setup and Execution

# 1. Create and activate a virtual environment
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows (PowerShell):
.\\venv\\Scripts\\Activate.ps1

# 2. Install the required dependencies
pip install -r requirements.txt

# 3. Run the script
python main.py vid.mp4 ./<output_folder>

Output Structure
The script will generate an output folder with the following structure:

<output_folder>/
├── standardized_audio.wav   # The full audio track, standardized.
├── speech_timestamps.json   # JSON file with start/end times of speech.
└── segmented_clips/         # Folder containing all the final clips.
    ├── segment_01.wav
    └── ...

Performance Tuning and Final Analysis
The script was tested on a complex 1:41 minute anime clip. An initial run (V1) produced a good baseline, but after a detailed analysis, it revealed opportunities for improvement. A data-driven tuning process was performed to enhance the segmentation quality.

Here is the detailed report from my analysis, i checked every segment and compared it with the original and noted every difference i could find.
### Initial Analysis of Segmentation Results (V1)

*Parameters: `min_silence_len=500`, `silence_thresh=-40`*

| Segment File | Timestamp (from JSON) | Content Description (User Notes) | Quality Assessment |
| :--- | :--- | :--- | :--- |
| `segment_01.wav` | `{"start": 1.54, "end": 5.52}` | scratching sounds, audio matches 1.5 to 5.5 in video | Fine (Classified as audio) |
| `segment_02.wav` | `{"start": 6.37, "end": 9.17}` | eerie sound effect | Clear Audio |
| `segment_03.wav` | `{"start": 18.19, "end": 19.11}` | some background electric noise | Clear Audio |
| `segment_04.wav` | `{"start": 23.01, "end": 23.82}` | barely a second long, video has scratching from 21-23s | **Bad Audio (Fragmented)** |
| `segment_05.wav` | `{"start": 25.43, "end": 26.24}` | "METOO" (or similar dialogue) | **Bad Audio (Missed prior sound)**|
| `segment_06.wav` | `{"start": 30.56, "end": 30.98}` | not even a second, part of a longer dialogue from 30.5-64s | **Bad Audio (Fragmented)** |
| `segment_07.wav` | `{"start": 32.72, "end": 35.15}` | "is this because of my leg?" | Clear Audio |
| `segment_08.wav` | `{"start": 35.39, "end": 37.15}` | "we just need to fix it" | Clear Audio |
| `segment_09.wav` | `{"start": 38.31, "end": 42.11}` | "we can fix it, i can fix it all music starts again" | Clear Audio |
| `segment_10.wav` | `{"start": 42.45, "end": 43.43}` | "shinzou wo" | Clear Audio |
| `segment_11.wav` | `{"start": 44.11, "end": 46.12}` | "sasageyo!!" | Clear Audio |
| `segment_12.wav` | `{"start": 48.01, "end": 52.09}` | "Eren, get up you damn coward" | Clear Audio |
| `segment_13.wav` | `{"start": 52.6, "end": 54.44}` | "tatakae" | Clear Audio |
| `segment_14.wav` | `{"start": 55.49, "end": 58.0}` | "I wanna say that too (laughing)" | Clear Audio |
| `segment_15.wav` | `{"start": 59.34, "end": 60.59}` | "of course you did" | Okay Audio (Slightly off) |
| `segment_16.wav` | `{"start": 64.08, "end": 64.67}` | not even a second long, weird background noise | **Redundant Segment** |
| `segment_17.wav` | `{"start": 65.41, "end": 101.44}`| 36 seconds of background music/nullified sound | **Redundant Segment** |

using my analysis, i made some changes and repeated the same process, here is the result.
### Analysis of Tuned Segmentation Results (V2)

*Parameters: `min_silence_len=700`, `silence_thresh=-50`*

| Segment File | Timestamp (from JSON) | Content Description (User Notes) | Quality Assessment |
| :--- | :--- | :--- | :--- |
| `segment_01.wav` | `{"start": 1.54, "end": 5.52}` | scratching captured in one segment | Clear Audio |
| `segment_02.wav` | `{"start": 6.37, "end": 19.11}` | ambulance or police car sound | Clear Audio, **Combined it fully this time** |
| `segment_03.wav` | `{"start": 21.36, "end": 26.24}` | scratching sound, missed the previous time but got it this time | Clear Audio |
| `segment_04.wav` | `{"start": 29.83, "end": 31.43}` | captures the pause from dialogue and removes scratching sound | Clear Audio |
| `segment_05.wav` | `{"start": 32.72, "end": 37.15}` | birds flapping sound | Clear Audio |
| `segment_06.wav` | `{"start": 37.39, "end": 37.89}` | not even a second long | Redundant |
| `segment_07.wav` | `{"start": 38.31, "end": 39.15}` | "uhmmmm" | Clear Audio |
| `segment_08.wav` | `{"start": 39.52, "end": 52.09}` | dialogues back and forth | **Massive improvement**, captures all dialogue in one segment |
| `segment_09.wav` | `{"start": 52.6, "end": 58.0}` | "lets throw this away and then eren get up you damn..." | Clear Audio |
| `segment_10.wav` | `{"start": 58.62, "end": 59.46}` | "ummm" | Clear Audio |
| `segment_11.wav` | `{"start": 61.35, "end": 62.15}` | background noise, it is loud enough to be captured | Redundant |
| `segment_12.wav` | `{"start": 62.4, "end": 101.44}`| captures a dialogue and the rest of the 17 seconds is noise | Clear Audio |


V1 Findings & Issues
The initial run with default parameters (min_silence_len=500, silence_thresh=-40) produced 17 segments. Key issues included:

Speech Fragmentation: A single conversation was incorrectly split across eight separate clips.

Low Sensitivity: Quiet but important sound effects were completely missed.

Redundancy: Several very short, non-speech clips were generated.

Tuning Process & V2 Improvements
Based on the V1 analysis, the script's parameters were adjusted to be more sensitive and patient with pauses (min_silence_len=700, silence_thresh=-50). The second run (V2) produced a superior set of 12 segments:

Fragmentation Solved: The eight-clip conversation was correctly consolidated into a single, coherent segment.

Sensitivity Fixed: The previously missed quiet sound effect was successfully captured.

Logical Cohesion: The total number of segments was reduced, and related audio events were merged logically.

Conclusion
The data-driven tuning process was highly successful, resolving the key issues from the initial run. The final output is a more accurate and logically structured set of audio clips that successfully fulfills the project requirements. The increased sensitivity resulted in the minor, expected trade-off of capturing a few faint background noises, which is far outweighed by the significant gains in dialogue accuracy.


(P.S. Since this internship is centered on anime/manga, I thought I’d also share my previous project:
📖 Manga Verse – A Manga Discovery App
https://github.com/vansh212121/MangaVerse

It’s a personal project I built around the manga, so I’m really excited about the chance to contribute to something in this space.)