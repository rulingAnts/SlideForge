# SlideForge

A Python tkinter application that creates YouTube-compatible MP4 videos from audio files and images, with the ability to export a single combined video.

## Features

- **Easy-to-use GUI**: Simple tkinter interface for all operations
- **Multiple audio formats**: Supports WAV, MP3, M4A, AAC, FLAC, OGG, WMA
- **Multiple image formats**: Supports JPG, PNG, TIFF, BMP, GIF
- **Batch processing**: Process multiple files at once
- **720p output**: Creates YouTube-compatible 720p MP4 videos
- **Flexible association**: Associate images with audio files individually or in bulk
- **Combined export**: Concatenate all generated videos into a single file, with a 1-second black transition and subtle audio click between each clip

## Requirements

When **running from source**, you need:
- Python 3.6 or higher
- ffmpeg on your system PATH

**Pre-built binaries** include a bundled copy of ffmpeg — no extra installation required.

### Installing ffmpeg (source builds only)

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
git clone https://github.com/rulingAnts/SlideForge.git
cd SlideForge
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

5. **Export a combined video** (optional):
   - After creating 2 or more videos, the "Export Combined Video" button becomes active
   - Click it to merge all videos into a single file
   - A 1-second black screen with a subtle audio click separates each clip

## Pre-built Releases

Download a pre-built binary for your platform from the [Releases](https://github.com/rulingAnts/SlideForge/releases) page.
No Python installation required. **ffmpeg is bundled inside the download** — no separate ffmpeg installation needed.

| Platform | File |
|---|---|
| macOS (Apple Silicon) | `SlideForge-macos-arm64.dmg` |
| Windows x64 | `SlideForge-windows-x64.exe` |
| Linux x86-64 | `SlideForge-linux-x86_64.AppImage` |

## How It Works

The application uses ffmpeg to combine static images with audio files to create videos:

- Video resolution: 1280×720 (720p)
- Video codec: H.264 (libx264)
- Audio codec: AAC
- Audio bitrate: 192 kbps
- Pixel format: yuv420p (for maximum compatibility)
- The image is scaled and padded to fit 720p while maintaining aspect ratio
- Video duration matches the audio duration

## License

Copyright © 2025 Seth Johnston. Licensed under the [GNU Affero General Public License v3.0](LICENSE).

In short: you are free to use, modify, and distribute this software, but any distributed or network-hosted version must also be released under the same AGPL-3.0 terms with source code available.

## Acknowledgements

Developed with AI assistance from [GitHub Copilot Chat](https://github.com/features/copilot) in Visual Studio Code.

## Third-Party Notices

### FFmpeg

Pre-built binaries of SlideForge include a copy of **FFmpeg 7.1**, obtained
via [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg) at build time.
The bundled FFmpeg binary is compiled with GPL-licensed components
(`--enable-gpl --enable-libx264 --enable-libx265 --enable-libvidstab`) and is
therefore distributed under the **GNU General Public License, version 2 or
later (GPL-2.0-or-later)**.

> **Copyright © 2000–2024 the FFmpeg developers**
>
> This program is free software; you can redistribute it and/or modify it
> under the terms of the GNU General Public License as published by the Free
> Software Foundation; either version 2 of the License, or (at your option)
> any later version.

- **License text:** <https://www.gnu.org/licenses/old-licenses/gpl-2.0.html>
- **Source code:** <https://ffmpeg.org/download.html>
- **Project home:** <https://ffmpeg.org/>

The FFmpeg binary is compiled against the following notable third-party
libraries (among others):

| Library | License | Copyright |
|---|---|---|
| libx264 | GPL 2+ | Copyright © 2003–2024 the x264 project |
| libx265 | GPL 2+ | Copyright © 2013–2024 MulticoreWare, Inc. |
| libvpx | BSD 3-Clause | Copyright © 2010–2024 the WebM project authors |
| libopus | BSD 3-Clause | Copyright © 2001–2023 Xiph.Org Foundation |
| libvorbis | BSD 3-Clause | Copyright © 2002–2020 Xiph.Org Foundation |
| libtheora | BSD 3-Clause | Copyright © 2002–2020 Xiph.Org Foundation |
| libmp3lame | LGPL 2+ | Copyright © The LAME Project |
| libsvtav1 | BSD + AOMedia | Copyright © 2019 Alliance for Open Media |
| libaom | BSD 2-Clause | Copyright © 2016 The WebM project |
| libvmaf | BSD 2-Clause | Copyright © 2016–2024 Netflix, Inc. |
| libwebp | BSD 3-Clause | Copyright © 2010 Google LLC |
| libass | ISC | Copyright © 2006–2022 Grigori Goronzy |
| libfreetype | FTL or GPL 2+ | Copyright © 1996–2024 David Turner et al. |
| libharfbuzz | MIT | Copyright © 2010–2024 Behdad Esfahbod et al. |

A full list of included libraries can be obtained by running the bundled
binary with `ffmpeg -buildconf`.

> **Note on license interaction:** SlideForge itself is AGPL-3.0-or-later.
> FFmpeg is invoked as a separate subprocess and constitutes a separate,
> independent program distributed in aggregate. The GPL-2.0-or-later terms
> apply to the FFmpeg binary; the AGPL-3.0-or-later terms apply to
> SlideForge. Users who redistribute either component must comply with the
> respective license.

### imageio-ffmpeg (build-time only)

The [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg) Python package
is used **at build time only** (inside GitHub Actions) to obtain the pre-built
FFmpeg binary. It is not distributed with SlideForge.

- **License:** BSD 2-Clause
- **Copyright:** Copyright © 2014–2024 the imageio contributors
