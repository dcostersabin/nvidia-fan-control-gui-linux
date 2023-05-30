import xmltodict
from executer import CommandExecutor


class NvidiaSmi(CommandExecutor):
    def __init__(self):
        super(NvidiaSmi, self).__init__()
        self.data = {}

    def commands(self):
        return ["nvidia-smi -q -x"]

    def post_execution(self):
        self.data.update(xmltodict.parse(self.output))

    def error(self, e: Exception):
        pass


def main():
    NvidiaSmi().execute()


if __name__ == "__main__":
    main()
