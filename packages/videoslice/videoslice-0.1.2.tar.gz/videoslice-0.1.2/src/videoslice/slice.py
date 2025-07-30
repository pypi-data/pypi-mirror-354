from typing import List

from videoslice.program_runner import ProgramRunner


def slice_video(ffmpeg_args: List[str], log=True) -> int:
    """Slices a video using ffmpeg."""
    p = ProgramRunner(ffmpeg_args)
    return p.run(log=log)


def slice_video_args(start, end, source, destination) -> List[str]:
    """
    Cuts a video from start to end time.
        :param start: Start time in HH:MM:SS format.
        :param end: End time in HH:MM:SS format.
        :param source: Path to the source video file.
        :param destination: Path to save the cut video file.
    """
    args = [
        "ffmpeg",
        "-ss",
        start,
        "-to",
        end,
        "-i",
        source,
        "-vcodec",
        "libx264",
        "-acodec",
        "aac",
        "-c",
        "copy",
        "-y",
        destination,
    ]

    return args
