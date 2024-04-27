from supporting.project_part import ProjectPart
from image_generator import image_generator
from piloting_rev import piloting_rev

from globals import *


if __name__ == '__main__':
    # ProjectPart.IMG_GEN or ProjectPart.EXPERIMENT
    project_part = ProjectPart.EXPERIMENT

    # remove arguments for the real img gen & experiment
    config.startup(
        n_blocks=2,
        n_trials=4
    )

    if project_part == ProjectPart.IMG_GEN:
        config_gen.startup()

        image_generator()

    elif project_part == ProjectPart.EXPERIMENT:
        # remove arguments for the experiment
        config_exp.startup(
            size=(2560 / 2, 1440 / 2),
            allowGUI=True,
            fullscr=False
        )
        parallel_ports.startup(
            use=False
        )

        piloting_rev()
