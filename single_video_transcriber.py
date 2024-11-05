import os
import json
import whisper
import subprocess
from tkinter import filedialog
import tkinter as tk
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Replace hardcoded paths with environment variables
TRANSCRIPTION_OUTPUT_PATH = os.getenv('TRANSCRIPTION_OUTPUT_PATH')

def clean_filename(text):
    """Clean text for use in filenames"""
    return "".join(c for c in text if c.isalnum() or c in (' ', '-', '_')).rstrip()

def extract_audio(video_path, audio_path):
    # Normalize paths
    video_path = os.path.normpath(video_path)
    audio_path = os.path.normpath(audio_path)
    
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",  # No video
        "-acodec", "pcm_s16le",  # Audio codec
        "-ar", "16000",  # Sample rate
        "-ac", "1",  # Mono
        "-f", "wav",  # Force WAV format
        "-y",  # Overwrite output file
        audio_path
    ]
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        
        # Run ffmpeg command
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        
        if os.path.exists(audio_path):
            print(f"Audio extracted successfully to: {audio_path}")
            return True
        else:
            print(f"Audio file not created at: {audio_path}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e.stderr}")
        print(f"Failed command: {' '.join(command)}")
        return False

def transcribe_audio(audio_path):
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    
    print("Transcribing audio (this may take a while)...")
    result = model.transcribe(audio_path)
    
    return result["text"]

def process_video(video_path, output_path):
    print(f"\nProcessing video: {os.path.normpath(video_path)}")
    
    # Create base filename from video path
    base_filename = clean_filename(os.path.splitext(os.path.basename(video_path))[0])
    audio_path = os.path.normpath(os.path.join(os.path.dirname(video_path), f'{base_filename}.wav'))
    
    print("Extracting audio from video...")
    if not extract_audio(video_path, audio_path):
        print("Failed to extract audio from video. Aborting...")
        return
        
    if not os.path.exists(audio_path):
        print(f"Audio file not found at: {audio_path}. Aborting...")
        return
        
    print("Transcribing audio...")
    transcription = transcribe_audio(audio_path)
    
    # Save transcription to selected output path
    transcription_file_path = os.path.normpath(os.path.join(output_path, f'{base_filename}.txt'))
    with open(transcription_file_path, 'w', encoding='utf-8') as file:
        file.write(transcription)
    
    print(f"Transcription saved to: {transcription_file_path}")
    
    # Clean up
    os.remove(audio_path)
    print("Temporary audio file cleaned up")

def main():
    # Create root window but hide it
    root = tk.Tk()
    root.withdraw()

    # Open file dialog for video selection
    video_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[
            ("Video files", "*.mp4 *.avi *.mkv *.mov *.flv"),
            ("All files", "*.*")
        ]
    )
    
    if not video_path:
        print("No file selected. Exiting...")
        return

    # Open directory dialog for output location
    output_path = filedialog.askdirectory(
        title="Select Output Directory for Transcription"
    )

    if not output_path:
        print("No output directory selected. Exiting...")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    process_video(video_path, output_path)

if __name__ == "__main__":
    main()

