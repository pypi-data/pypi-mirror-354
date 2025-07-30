import argparse

from videoslice.download import download_args, download_video
from videoslice.program_runner import ProgramRunner
from videoslice.runner import Runner
from videoslice.slice import cut_video_args, slice_video


def main() -> None:
    print("[Video Slice]: Hello from videoslice!")
    parser = argparse.ArgumentParser(description="Video slicing utility")
    parser.add_argument(
        "--start",
        "-s",
        type=str,
        required=True,
        help="Start time in HH:MM:SS format",
    )
    parser.add_argument(
        "--end", "-e", type=str, required=True, help="End time in HH:MM:SS format"
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        required=True,
        help="Path to save the downloaded video file",
    )
    parser.add_argument(
        "--output", "-o", type=str, required=True, help="Path to save the sliced video"
    )
    parser.add_argument(
        "--url", "-u", type=str, required=False, help="URL of the video to download"
    )
    parser.add_argument(
        "--log",
        "-l",
        action="store_true",
        help="Enable logging of yt-dlp command and output",
    )
    args = parser.parse_args()

    start = args.start
    end = args.end
    input_video = args.input
    output = args.output
    url = args.url
    log = args.log
    ytdlp_args = download_args(url, input_video)
    ffmpeg_args = cut_video_args(start, end, input_video, output)

    if url is not None:
        # download video
        res = download_video(ytdlp_args, log=log)
        if res.returncode != 0:
            print("Error downloading video. Exiting.")
            return

    # slice video
    slice_video(ffmpeg_args, log=log)


if __name__ == "__main__":
    # example
    # videoslice -s 00:04:22 -e 00:05:40 -i cursor.mp4 -o cursor.mp4 -u https://youtu.be/sLaxGAL_Pl0 --log
    main()
