import numpy as np


class Config:
    """
    The Config class is responsible for configuring both the experiment and the image generation.
    """

    def __init__(self):
        self.stim_dir = None

        self.n_blocks = None
        self.n_trials = None
        self.number = None

        self.refresh_rate = None

        self.noise_freq_hz = None
        self.gabor_freq_hz = None
        self.ann_freq_hz = None

        self.noise_frame_length = None
        self.gabor_frame_length = None
        self.ann_frame_length = None

    def startup(
            self,
            stim_dir="stimuli",
            n_blocks=4,
            n_trials=90,
            number=20,
            refresh_rate=120,
            noise_freq_hz=40,
            gabor_freq_hz=30,
            ann_freq_hz=24
    ):
        """
        Initialize the configuration.

        :param stim_dir: name of the directory where the stimuli are stored (default: "stimuli")
        :param n_blocks: number of blocks (default: 4)
        :param n_trials: number of trials (default: 90)
        :param number: number of images of every type in trial (default: 20)
        :param refresh_rate: refresh rate of the monitor (default: 120)
        :param noise_freq_hz: frequency of the noise (default: 40)
        :param gabor_freq_hz: frequency of the gabor (default: 30)
        :param ann_freq_hz: frequency of the annulus (default: 24)
        """

        self.stim_dir = stim_dir

        self.n_blocks = n_blocks
        self.n_trials = n_trials
        self.number = number

        self.refresh_rate = refresh_rate

        self.noise_freq_hz = noise_freq_hz
        self.gabor_freq_hz = gabor_freq_hz
        self.ann_freq_hz = ann_freq_hz

        self._calculate_frame_lengths()

    def _calculate_frame_lengths(self):
        # Calculate the number of frames of every component
        component_lengths = self.refresh_rate / np.array([
            self.noise_freq_hz, self.gabor_freq_hz, self.ann_freq_hz
        ])
        self.noise_frame_length, self.gabor_frame_length, self.ann_frame_length = tuple([
            int(i) for i in component_lengths
        ])


