import os
import argparse
import json
from moviepy.editor import AudioFileClip
from pydub import AudioSegment
from pydub.silence import detect_nonsilent


def extract_and_standardize_audio(input_file, output_wav_file):
    """
    Extracts audio from the input file, converts it to mono, 16 kHz,
    and saves it as a WAV file.

    Args:
        input_file (str): Path to the input audio or video file.
        output_wav_file (str): Path to save the standardized WAV file.

    Returns:
        str: The path to the created WAV file, or None if failed.
    """
    try:
        print(f"Loading file: {input_file}")
        audio_clip = AudioFileClip(input_file)
        print("Standardizing audio to 16 kHz mono WAV...")
        audio_clip.write_audiofile(
            output_wav_file, fps=16000, nbytes=2, codec="pcm_s16le"
        )
        print(f"Standardized audio saved to: {output_wav_file}")
        return output_wav_file
    except Exception as e:
        print(f"Error during audio extraction and standardization: {e}")
        return None


def detect_and_export_speech_segments(
    standardized_wav, output_dir, timestamps_file, clips_folder
):
    """
    Detects speech segments in the audio file and exports them.

    Args:
        standardized_wav (str): Path to the standardized WAV audio file.
        output_dir (str): The main directory for all outputs.
        timestamps_file (str): Path to save the JSON timestamps file.
        clips_folder (str): Name of the subfolder to save audio clips.
    """
    try:
        print("Loading standardized WAV for speech detection...")
        audio = AudioSegment.from_wav(standardized_wav)
        print("Detecting non-silent segments...")
        nonsilent_ranges = detect_nonsilent(
            audio, min_silence_len=700, silence_thresh=-50
        )

        if not nonsilent_ranges:
            print("No speech segments detected.")
            return

        print(f"Found {len(nonsilent_ranges)} speech segments.")
        detected_timestamps = []
        segment_clips_dir = os.path.join(output_dir, clips_folder)
        os.makedirs(segment_clips_dir, exist_ok=True)

        for i, (start_ms, end_ms) in enumerate(nonsilent_ranges):
            start_sec = round(start_ms / 1000.0, 2)
            end_sec = round(end_ms / 1000.0, 2)
            detected_timestamps.append({"start": start_sec, "end": end_sec})
            segment_audio = audio[start_ms:end_ms]
            output_filename = f"segment_{i+1:02d}.wav"
            output_path = os.path.join(segment_clips_dir, output_filename)
            print(f"Exporting segment {i+1} to {output_path}...")
            segment_audio.export(output_path, format="wav")

        print(f"Saving timestamps to {timestamps_file}...")
        with open(timestamps_file, "w") as f:
            json.dump(detected_timestamps, f, indent=2)

    except Exception as e:
        print(f"An error occurred during speech detection and export: {e}")


def main():
    """
    Main function to orchestrate the speech segmentation process.
    """
    parser = argparse.ArgumentParser(
        description="Process an audio/video file to extract speech segments."
    )
    parser.add_argument(
        "input_file", type=str, help="Path to the input audio or video file."
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="Path to the directory where all output files will be saved.",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    standardized_audio_path = os.path.join(args.output_dir, "standardized_audio.wav")
    timestamps_path = os.path.join(args.output_dir, "speech_timestamps.json")
    clips_folder_name = "segmented_clips"

    print("--- Starting Speech Segmentation Process ---")
    print("\n--- Task 1: Extracting and Standardizing Audio ---")
    standardized_file = extract_and_standardize_audio(
        args.input_file, standardized_audio_path
    )

    if standardized_file:
        print("\n--- Task 2 & 3: Detecting and Exporting Speech Segments ---")
        detect_and_export_speech_segments(
            standardized_file, args.output_dir, timestamps_path, clips_folder_name
        )

    print("\n--- Process Complete ---")
    print(f"All outputs have been saved in the '{args.output_dir}' directory.")


if __name__ == "__main__":
    main()
