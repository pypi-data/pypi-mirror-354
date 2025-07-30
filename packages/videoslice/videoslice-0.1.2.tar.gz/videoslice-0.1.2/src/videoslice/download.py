from typing import List
from videoslice.program_runner import ProgramRunner


def download_runner(ytdlp_args: List[str], log=True) -> int:
    """
    Downloads a video using yt-dlp with the provided arguments.
        :param ytdlp_args: Arguments for yt-dlp as a string.
        :param log: Whether to log the output command.
        :return: Exit code of the yt-dlp command.
    """
    p = ProgramRunner(" ".join(ytdlp_args))
    return p.run(log=log)


def youtube_download_args(url: str, destination: str) -> List[str]:
    """
    Downloads a video using yt-dlp.
        :param url: URL YouTube video.
        :param destination: Path to save video file.
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
