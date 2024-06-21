import numpy as np


class ConfigImgGen:
    """
    The ConfigImgGen class is responsible for configuring the image generation.
    """

    def __init__(self):
        self.image_size = None
        self.my_dpi = None
        self.gabor_freq_prob = None

        self.plot = None

        self.screen_width_px = None
        self.screen_height_px = None
        self.diagonal_cm = None
        self.ppcm = None

    def startup(
            self,
            image_size=1024,
            my_dpi=109,
            gabor_freq_prob=0.5,
            plot=False,
            screen_width_px=1512,
            screen_height_px=982,
            diagonal_cm=36.068
    ):
        """
        Initialize the configuration.

        :param image_size: size of the image in pixels, square (default: 1024)
        :param my_dpi: dots per inch (default: 109)
        :param gabor_freq_prob: probability of the gabor frequency (default: 0.5)
        :param plot: whether to plot the images (default: False)
        :param screen_width_px: width of the screen in pixels (default: 1512)
        :param screen_height_px: height of the screen in pixels (default: 982)
        :param diagonal_cm: diagonal of the screen in centimeters (default: 36.068)
        """

        self.image_size = image_size
        self.my_dpi = my_dpi
        self.gabor_freq_prob = gabor_freq_prob

        self.plot = plot

        # change depending on device
        self.screen_width_px = screen_width_px
        self.screen_height_px = screen_height_px
        self.diagonal_cm = diagonal_cm
        # pixels per centimeter
        self.ppcm = np.sqrt(self.screen_width_px ** 2 + self.screen_height_px ** 2) / self.diagonal_cm
