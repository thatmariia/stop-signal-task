import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import scipy.stats as stats

from make_noise import *
from make_gabor import *
from make_annulus import *
from make_fixation import *

def single_trial(
    ref_rate_hz = 120, stim_dir = "stimuli", snr = 1/3, stop_trial = True, 
    only_noise_ms = 500, only_gabor_ms = 500, trial_length_ms = 2000, noise_freq_hz = 40, gabor_freq_hz = 30, ann_freq_hz = 24):
    
    component_lengths = ref_rate_hz / np.array([noise_freq_hz, gabor_freq_hz, ann_freq_hz])
    noise_frame_length, gabor_frame_length, ann_frame_length = tuple([int(i) for i in component_lengths])

    noise_frames = int(only_noise_ms/1000 * ref_rate_hz)
    if stop_trial:
        only_gabor_frames = int(only_gabor_ms/1000 * ref_rate_hz)
        gabor_ann_frames = int(trial_length_ms/1000 * ref_rate_hz) - only_gabor_frames
    else:
        only_gabor_frames = int(trial_length_ms/1000 * ref_rate_hz)
        gabor_ann_frames = 0
    
    noise_counter, gabor_counter, ann_counter, image_counter = 0, 0, 0, 0
    gabor_on, ann_on = 0, 0
    frame_lengths_arr = np.empty(1)
    frame_length = 0

    #only noise
    for i in range(noise_frames):
        if noise_counter == 0:
            new_image = True
        if new_image:
            image_counter += 1
            frame_lengths_arr = np.append(frame_lengths_arr, frame_length)
            frame_length = 1
            new_image = False
        else:
            frame_length += 1
        noise_counter += 1
        if noise_counter == noise_frame_length: 
            noise_counter = 0 

    #add gabor
    for i in range(only_gabor_frames):
        if noise_counter == 0:
            new_image = True
        if gabor_counter == 0:
            gabor_on = -gabor_on + 1
            new_image = True
        if new_image:
            frame_lengths_arr = np.append(frame_lengths_arr, frame_length)
            frame_length = 1
            new_image = False
        else:
            frame_length += 1
        noise_counter += 1
        gabor_counter += 1
        if noise_counter == noise_frame_length: 
            noise_counter = 0 
        if gabor_counter == gabor_frame_length: 
            gabor_counter = 0 

    #add annulus
    for i in range(gabor_ann_frames):
        if noise_counter == 0:
            new_image = True
        if gabor_counter == 0:
            gabor_on = -gabor_on + 1
            new_image = True
        if ann_counter == 0:
            ann_on = -ann_on + 1
            new_image = True
        if new_image:
            frame_lengths_arr = np.append(frame_lengths_arr, frame_length)
            frame_length = 1
            new_image = False
        else:
            frame_length += 1
        noise_counter += 1
        gabor_counter += 1
        ann_counter += 1
        if noise_counter == noise_frame_length: noise_counter = 0 
        if gabor_counter == gabor_frame_length: gabor_counter = 0 
        if ann_counter == ann_frame_length: ann_counter = 0 
    
    frame_lengths_arr = np.append(frame_lengths_arr, frame_length)[2:]
    frame_lengths_arr = [int(i) for i in frame_lengths_arr]

    return frame_lengths_arr, noise_frames, only_gabor_frames, gabor_ann_frames