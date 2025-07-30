from typing import Any


class Runner:
    """Base class for all runners."""

    PASS = "pass"
    FAIL = "fail"
    UNRESOLVED = "unresolved"

    def __init__(self) -> None:
        pass

    def run(self, inp: str) -> Any:
        return (inp, Runner.UNRESOLVED)
