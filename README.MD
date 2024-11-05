# Single Video Transcriber

A simple Python script that transcribes video files to text using OpenAI's Whisper model.

## Prerequisites

- Python 3.10 or higher
- FFmpeg installed on your system
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/tuckwoor/single_video_transcriber.git
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Ensure FFmpeg is installed on your system:
   - Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)
   - Mac: `brew install ffmpeg`
   - Linux: `sudo apt-get install ffmpeg`

## Usage

1. Run the script:

```bash
python single_video_transcriber.py
```

2. Select your video file when prompted
3. Choose where to save the transcription
4. Wait for the transcription to complete

The script will:
- Extract audio from the video
- Transcribe the audio using Whisper
- Save the transcription as a text file
- Clean up temporary files

## Supported Video Formats

- MP4
- AVI
- MKV
- MOV
- FLV

## License
This project is licensed under the GNU General Public License (GPL).
