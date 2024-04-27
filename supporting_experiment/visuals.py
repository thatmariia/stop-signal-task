from psychopy import visual
from PIL import Image

from globals import *


class Visuals:
    """
    The Visuals class is responsible for displaying the instructions and the end of the blocks and experiment.
    """

    def show_instructions(self):
        """
        Shows the instructions for the experiment.
        """

        img_low = Image.open("instruction/low.png")
        img_high = Image.open("instruction/high.png")

        # Instructions
        low_img = visual.ImageStim(
            win=config_exp.win,
            image=img_low,
            pos=(600, 80)
        )
        low_img.draw()

        high_img = visual.ImageStim(
            win=config_exp.win,
            image=img_high,
            pos=(-600, 80)
        )
        high_img.draw()

        low_text = visual.TextStim(
            config_exp.win,
            text="Low spatial frequency: press 'j'",
            pos=(600, -360),
            height=35
        )
        low_text.draw()

        high_text = visual.TextStim(
            config_exp.win,
            text="High spatial frequency: press 'f'",
            pos=(-600, -360),
            height=35
        )
        high_text.draw()

        introduction_text = visual.TextStim(
            config_exp.win,
            text="Press 'space' to practice.",
            pos=(0, -420),
            height=35
        )
        introduction_text.draw()

        config_exp.win.flip()

    def show_after_experiment_screen(self, accuracy_rate):
        """
        Shows the end of the experiment screen.

        :param accuracy_rate: the accuracy rate of the last block
        """

        text = visual.TextStim(
            config_exp.win,
            text=f"This is the end of the experiment. Good job! Your accuracy rate is {accuracy_rate * 100}%.",
            height=35
        )
        text.draw()
        text = visual.TextStim(
            config_exp.win,
            text="Thank you for your participation!",
            pos=(0, -200),
            height=35
        )
        text.draw()

    def show_after_block_screen(self, block, accuracy_rate):
        """
        Shows the end of the block screen.

        :param block: the block number
        :param accuracy_rate: the accuracy rate of the block
        """

        text = visual.TextStim(
            config_exp.win,
            text=f"Block {block + 1} ends. Good job! Your accuracy rate is {accuracy_rate * 100}%.",
            height=35
        )
        text.draw()
        text = visual.TextStim(
            config_exp.win,
            text="Now please take a 3 min break.",
            pos=(0, -200),
            height=35
        )
        text.draw()
