from supporting_img_gen.agent_image_generator import ImageGenerator

from config.parser import get_parsed_args
from utils.globals import *


def image_generator():
    args = get_parsed_args()
    config.startup(
        n_blocks=args.n_blocks,
        n_trials=args.n_trials
    )

    config_gen.startup()

    img_generator = ImageGenerator()
    img_generator.generate()


if __name__ == "__main__":
    image_generator()

