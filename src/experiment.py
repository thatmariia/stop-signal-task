from supporting_experiment.agent_formal_experiment import FormalExperiment

from config.parser import get_parsed_args
from utils.globals import *


def experiment():
    args = get_parsed_args()
    config.startup(
        n_blocks=args.n_blocks,
        n_trials=args.n_trials
    )

    config_exp.startup(
        size=(2560 / 2, 1440 / 2),
        allowGUI=True,
        fullscr=False
    )
    parallel_ports.startup(
        use=False
    )

    formal_experiment = FormalExperiment()
    formal_experiment.run()

    print("Experiment done!")


if __name__ == "__main__":
    experiment()
