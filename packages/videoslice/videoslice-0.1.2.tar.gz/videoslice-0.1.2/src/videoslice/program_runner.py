import subprocess
from typing import List, Union


class ProgramRunner:
    """Class that take in a program and runs it"""

    def __init__(self, program: Union[str, List[str]]) -> None:
        self.program = program

    def run(self, log=True) -> int:
        p = subprocess.Popen(
            self.program,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            shell=isinstance(self.program, str),
            text=True,
        )

        if log:
            for line in p.stdout:
                print(line, end="")
        return p.wait()
