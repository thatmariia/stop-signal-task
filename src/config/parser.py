import argparse


def get_parsed_args():
    parser = argparse.ArgumentParser(prog="stop-signal-task")
    parser = Parser(parser)
    args = parser.parse_args()
    return args


class Parser:

    def __init__(self, parser):
        self.parser = parser
        self._add_arguments()

    def parse_args(self):
        args, _ = self.parser.parse_known_args()
        return args

    def _add_arguments(self):
        self.parser.add_argument(
            "--n_blocks",
            type=int,
            default=4,
            help="Number of blocks"
        )
        self.parser.add_argument(
            "--n_trials",
            type=int,
            default=90,
            help="Number of trials"
        )