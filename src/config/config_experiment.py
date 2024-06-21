from psychopy import visual, core

from utils.globals import *


class ConfigExperiment:
    """
    The ConfigExperiment class is responsible for configuring the experiment.
    """

    def __init__(self):

        self.timer = None

        self.bg_scale = None
        self.win = None

        self.use_real_refresh_rate = None

    def startup(
            self,
            bg_scale=tuple([-1 + 2 * (90 / 255)] * 3),
            size=(2560, 1440),
            allowGUI=False,
            fullscr=True,
            use_real_refresh_rate=False
    ):
        """
        Initialize the configuration.

        :param bg_scale: background color (default is gray)
        :param size: size of the window (default: 2560x1440)
        :param allowGUI: whether to allow the GUI (default: False)
        :param fullscr: whether to go full screen (default: True)
        :param use_real_refresh_rate: whether to try and measure the real refresh rate (default: False)
        """

        self.timer = core.Clock()

        self.win = visual.Window(
            units="pix",
            allowGUI=allowGUI,
            size=size,
            color=list(bg_scale),
            screen=0,
            fullscr=fullscr,
            waitBlanking=False
        )
        # Don't record frame intervals
        self.win.recordFrameIntervals = False

        self.use_real_refresh_rate = use_real_refresh_rate

    def _handle_real_refresh_rate(self):
        if self.use_real_refresh_rate:
            # Record the refresh rate
            refresh_rate_real = self.win.getActualFrameRate(
                nIdentical=60,
                nMaxFrames=100,
                nWarmUpFrames=10,
                threshold=1
            )
            print(f"Refresh rate: {refresh_rate_real}")

            if refresh_rate_real is not None:
                config.refresh_rate = int(refresh_rate_real)
