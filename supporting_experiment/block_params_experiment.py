import pandas as pd
from ast import literal_eval

from globals import *

class BlockParamsExperiment:
    """
    The BlockParams class is responsible for holding the configuration of the block for the experiment.
    """

    def __init__(self, block):
        parameters = pd.read_csv(f'{config.stim_dir}/block_{block}/parameters.csv')
        self.frame_length_use = parameters['frame_length'].apply(literal_eval)
        self.only_noise_frames = parameters['only_noise_frames']
        self.only_gabor_frames = parameters['only_gabor_frames']
        self.gabor_annulus_frames = parameters['gabor_annulus_frames']
        self.correct_answer = parameters['correct_answer']
        self.gabor_freq = parameters['gabor_freq']
