# GRN Video Generator

A Python tkinter application that creates YouTube-compatible MP4 videos from audio files and images.

## Features

- **Easy-to-use GUI**: Simple tkinter interface for all operations
- **Multiple audio formats**: Supports WAV, MP3, M4A, AAC, FLAC, OGG, WMA
- **Multiple image formats**: Supports JPG, PNG, TIFF, BMP, GIF
- **Batch processing**: Process multiple files at once
- **720p output**: Creates YouTube-compatible 720p MP4 videos
- **Flexible association**: Associate images with audio files individually or in bulk

## Requirements

- Python 3.6 or higher
- ffmpeg (must be installed on your system)

### Installing ffmpeg

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

#### macOS
```bash
brew install ffmpeg
```

#### Windows
Download and install from [ffmpeg.org](https://ffmpeg.org/download.html)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/rulingAnts/GRN_video_generator.git
cd GRN_video_generator
```

2. The application uses only Python standard library modules (tkinter, subprocess, threading), so no additional Python packages are required.

3. Ensure ffmpeg is installed and available in your system PATH.

## Usage

1. Run the application:
```bash
python video_generator.py
```

2. **Select a folder** containing your audio files by clicking "Select Folder"

3. **Associate images** with audio files:
   - Double-click on an audio file to select its image
   - Or click "Select Image for Selected File" after selecting a file
   - Or use "Select Images for All" to go through all files one by one

4. **Create videos** by clicking the "Create Videos" button:
   - Choose an output folder
   - The app will generate a 720p MP4 video for each audio-image pair

## How It Works

The application uses ffmpeg to combine static images with audio files to create videos:

- Video resolution: 1280x720 (720p)
- Video codec: H.264 (libx264)
- Audio codec: AAC
- Audio bitrate: 192 kbps
- Pixel format: yuv420p (for maximum compatibility)
- The image is scaled and padded to fit 720p while maintaining aspect ratio
- Video duration matches the audio duration

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
