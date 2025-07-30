import subprocess
from typing import List

from videoslice.program_runner import ProgramRunner
from videoslice.runner import Runner


def download_video(ytdlp_args: List[str], log=True) -> subprocess.CompletedProcess:
    p = ProgramRunner(program=ytdlp_args)
    (res, outcome) = p.run()
    if log:
        print("Running yt-dlp command:", " ".join(ytdlp_args))
        if res.stdout:
            print("Output:", res.stdout)
        if res.stderr:
            print("Error:", res.stderr)
        if outcome == Runner.PASS:
            print("yt-dlp command executed successfully.")
        if outcome == Runner.FAIL:
            print("yt-dlp command failed.")
        if outcome == Runner.UNRESOLVED:
            print("yt-dlp command was unresolved.")
        if outcome == Runner.FAIL or outcome == Runner.UNRESOLVED:
            print("Exiting due to failure or unresolved state.")
    return res


def download_args(url: str, destination: str) -> List[str]:
    """
    Downloads a video from a given URL using yt-dlp.
        :param url: URL of the video to download.
        :param destination: Path to save the downloaded video file.
    """
    args = [
        "yt-dlp",
        "-f",
        "'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b'",
        url,
        "-o",
        destination,
        "--cookies-from-browser",
        "chrome",
    ]
    return args
