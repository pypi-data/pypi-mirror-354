# Videoslice

![PyPI - Version](https://img.shields.io/pypi/v/videoslice)
![PyPI - Downloads](https://img.shields.io/pypi/dm/videoslice)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/mmsaki/videoslice)
![GitHub License](https://img.shields.io/github/license/mmsaki/videoslice)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/mmsaki/videoslice)
![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/msakiart)

Videoslice is a Python package that provides a simple way to slice videos into smaller segments based on specified time intervals. 


Use it to create clips from longer videos, making it easier to manage and share specific parts of your video content.

## Installation

You can install Videoslice using pip:

```bash
pip install videoslice
```

## Usage

Here's a basic example of how to use Videoslice:

>[!NOTE]
> Make sure you have `ffmpeg` installed on your system, as Videoslice relies on it for video processing.
> - [Download ffmpeg](https://ffmpeg.org/download.html)
> - [Download yt-dlp](https://github.com/yt-dlp/yt-dlp)

1. Download video from a YouTube URL + slice it:

```sh
videoslice --url https://youtu.be/sLaxGAL_Pl0 \
--start 00:00:10 \
--end 00:00:20 \
--input input_video.mp4 \
--output output_video.mp4 \
--log
```

2. Slice an existing video file:

```sh
videoslice --start 00:01:00 \
--end 00:01:30 \
--input existing_video.mp4 \
--output sliced_video.mp4 \
--log
```


## Command Line Options

You can view the command line options and their descriptions by running:

```sh
videoslice --help
```

<details>
<summary>Command Line Options</summary>

```text
usage: videoslice [-h] --start START --end END --input INPUT --output OUTPUT --url URL [--log]

Video slicing utility

options:
  -h, --help            show this help message and exit
  --start START, -s START
                        Start time in HH:MM:SS format
  --end END, -e END     End time in HH:MM:SS format
  --input INPUT, -i INPUT
                        Path to save the downloaded video file
  --output OUTPUT, -o OUTPUT
                        Path to save the sliced video
  --url URL, -u URL     URL of the video to download
  --log, -l             Enable logging of yt-dlp command and output

