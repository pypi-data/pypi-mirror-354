from typing import Optional, Callable
from pathlib import Path
import io


class Logger:
    def ispath(self):
        return isinstance(self.source, str) or isinstance(self.source, Path)

    def __init__(self, dest: list | str | Path | io.TextIOWrapper | Callable):
        self.source = dest
        self.dest = dest
        if self.ispath():
            self.dest = open(dest, "w")

    def log(self, *args):
        dest = self.dest
        if isinstance(dest, list):
            dest.append(args)
            return
        if isinstance(dest, Callable):
            dest(args)
            return

        s = "\t".join(str(i) for i in args)

        if isinstance(dest, io.TextIOWrapper):
            dest.write(s)
            dest.write("\n")
            return

        raise Exception("Unknown type")

    def __del__(self):
        if self.ispath():
            self.dest.close()


def create_logger(
    dest: Optional[list | str | Path | io.TextIOWrapper | Callable],
) -> Optional[Callable]:
    if dest is None:
        return

    log = Logger(dest)
    return log.log
