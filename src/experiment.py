from supporting_experiment.agent_formal_experiment import FormalExperiment

from utils.globals import *


def experiment():
    # remove arguments for the real img gen & experiment
    config.startup(
        n_blocks=2,
        n_trials=4
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
