import pandas as pd
import numpy as np
from scipy.stats import gamma
import scipy.stats as stats
from PIL import Image
from psychopy import visual
from single_trial import *

def multi_trial(n_trials=90, stop_trial_prob=1/3, gabor_freq_prob=0.5, stim_dir="stimuli"):

    # binomial distribution; the probability of stop_trial is stop_trial_prop; draw n_trials numbers
    stop_trials = stats.bernoulli.rvs(p=stop_trial_prob, size=n_trials)
    # transform the generated random numbers into Boolean values
    stop_trials = [bool(i) for i in stop_trials]

    # set the probability of high and low spatial frequency conditions
    gabor_freq_set = stats.bernoulli.rvs(p=gabor_freq_prob, size=n_trials)
    gabor_freq = np.where(gabor_freq_set == 0, 3.5, 4)
    
    # randomly draw the length of cue intervals and response intervals from a uniform distribution
    snr_vec = np.random.gamma(10, 1/60, n_trials)
    only_noise_ms_vec = [random.uniform(500, 1000) for _ in range(n_trials)]
    only_gabor_ms_vec = [random.uniform(0, 500) for _ in range(n_trials)]
    trial_length_ms_vec = [random.uniform(1200, 2000) for _ in range(n_trials)]

    frame_length_use = []
    noise_frames_use = []
    gabor_frames_use = []
    annulus_frames_use = []
    correct_answer = []
    
    for i in range(n_trials):
        frame_lengths_arr, noise_frames, only_gabor_frames, gabor_ann_frames = single_trial(
                                                                            snr = snr_vec[i],
                                                                            stop_trial = stop_trials[i],
                                                                            only_noise_ms = only_noise_ms_vec[i],
                                                                            only_gabor_ms = only_gabor_ms_vec[i],
                                                                            trial_length_ms = trial_length_ms_vec[i])
        # generate correct answers trial by trial
        if stop_trials[i] == True:
            correct_answer.append("miss")
        else:
            if gabor_freq[i] == 3.5:
                correct_answer.append("j")
            else:
                correct_answer.append("f")
        frame_length_use.append(frame_lengths_arr)
        noise_frames_use.append(noise_frames)
        gabor_frames_use.append(only_gabor_frames)
        annulus_frames_use.append(gabor_ann_frames)
    
    parameters = pd.DataFrame({'trial': list(range(n_trials)), 'correct_answer': correct_answer, 'gabor_freq': gabor_freq, 'snr': snr_vec, 'only_noise_frames': noise_frames_use, 'only_gabor_frames': gabor_frames_use, 'gabor_annulus_frames': annulus_frames_use, 'frame_length': frame_length_use})
    parameters.to_csv(stim_dir + "/parameters.csv", index = False)
    
    return frame_length_use
