from supporting_img_gen.agent_image_generator import ImageGenerator

from utils.globals import *


def image_generator():
    # remove arguments for the real img gen & experiment
    config.startup(
        n_blocks=2,
        n_trials=4
    )

    config_gen.startup()

    img_generator = ImageGenerator()
    img_generator.generate()


if __name__ == "__main__":
    image_generator()

