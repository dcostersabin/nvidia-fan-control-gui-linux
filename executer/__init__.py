from subprocess import Popen
from subprocess import PIPE
from abc import ABC, abstractmethod


class CommandExecutor(ABC):
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.return_code = None
        self.errors = []
        self.output = None

    def execute(self):
        self._run()

    def _run(self):
        try:
            self._run_command()
        except (
            OSError,
            IndexError,
            PermissionError,
            Exception,
        ) as e:
            self.errors.append(e)
            self.errors(e)

    @abstractmethod
    def commands(self) -> list:
        return []

    @abstractmethod
    def post_execution(self):
        pass

    @abstractmethod
    def error(self, e: Exception):
        pass

    def _run_command(self):
        process: Popen = Popen(
            self.commands(),
            stdout=PIPE,
            shell=True,
        )

        self.output = process.communicate(
            timeout=self.timeout,
        )[
            0
        ].decode("utf-8")
        self.return_code = process.wait(timeout=self.timeout * 10)
        self.post_execution()
