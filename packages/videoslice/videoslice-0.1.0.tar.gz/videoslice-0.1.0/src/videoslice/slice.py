import subprocess
from typing import List

from videoslice.program_runner import ProgramRunner
from videoslice.runner import Runner


def slice_video(ffmpeg_args: List[str], log=True) -> subprocess.CompletedProcess:
    """Slices a video using ffmpeg."""
    p2 = ProgramRunner(program=ffmpeg_args)

    (res, outcome2) = p2.run()

    if log:
        print("[Video Slice] Running ffmpeg command:", " ".join(ffmpeg_args))
        if res.stdout:
            print("Output:", res.stdout)
        if res.stderr:
            print("Error:", res.stderr)
        if outcome2 == Runner.PASS:
            print("ffmpeg command executed successfully.")
        if outcome2 == Runner.FAIL:
            print("ffmpeg command failed.")
        if outcome2 == Runner.UNRESOLVED:
            print("ffmpeg command was unresolved.")
    return res


def cut_video_args(start, end, source, destination) -> List[str]:
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
        destination,
    ]

    return args
