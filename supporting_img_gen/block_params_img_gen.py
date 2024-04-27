import pandas as pd
from globals import *


class BlockParamsImgGen:
    """
    The BlockParamsImgGen class is responsible for holding the configuration of the block for the image generation.
    """

    def __init__(self):

        self.gabor_freq = None
        self.correct_answer = None
        self.snr_vec = None

    def update(self, block):
        parameters = pd.read_csv(f'{config.stim_dir}/block_{block}/parameters.csv')
        self.gabor_freq = parameters['gabor_freq']
        self.correct_answer = parameters['correct_answer']
        self.snr_vec = parameters['snr']
