# Written by Yiming Zhao (2024)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import os
import scipy.stats as stats
from make_noise import *
from make_gabor import *
from make_annulus import *
from make_fixation import *
from multi_trial import *
from single_trial import *

# Parameters
n_trials = 90
n_blocks = 3
number = 20
image_size = 1024
my_dpi = 109
gabor_freq_prob = 0.5
stim_dir = "stimuli"

# Define a function to make directories
def make_dir(stim_dir):
    stim_dirs_block = [stim_dir + "/block_" + str(i) for i in range(n_blocks)]
    for block in range(n_blocks):
        try:
            os.mkdir(stim_dirs_block[block])
        except OSError:
            print(f'Directory block_{block} alredy exists. Files overwritten.')
        for trial in range(n_trials):
            stim_dirs_trial = stim_dirs_block[block] + f"/trial_{trial}"
            try:
                os.mkdir(stim_dirs_trial)
            except OSError:
                print(f'Directory trial_{trial} alredy exists. Files overwritten.')

# Define a function to generate images
def plotter(value_matrix, image_name):
    plt.figure(figsize = (image_size/my_dpi, image_size/my_dpi), dpi = my_dpi)
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    plt.imshow(value_matrix, vmin = 0, vmax = 1, cmap = 'gray')
    plt.savefig(image_name, dpi = my_dpi, transparent = True)
    plt.close('all')
    plt.clf()
    plt.cla()

# Define a function to generate images with only noise
def make_noise_img(number):
    noise_values_list = []
    for i in range(number):
        noise_values = (make_noise() - 0.25) * 2*noise_ratio + 0.5*signal_ratio
        noise_values_list.append(noise_values)
        filename = f"{stim_dir}/block_{block}/trial_{trial}/noise_{i}.png"
        plotter(noise_values + fixation_values, filename)
    return noise_values_list

# Define a function to generate images with noise & annulus
def make_annulus_img(number):
    for i in range(number):
        filename = f"{stim_dir}/block_{block}/trial_{trial}/annulus_{i}.png"
        plotter(noise_values_list[i] + annulus_values + fixation_values, filename)

# Define a function to generate images with gabor & noise
def make_gabor_img(number):
    gabor_rotation = random.randint(0, 180)
    if gabor_freq[trial] == 4:
        gabor_values = make_gabor(gabor_freq_cm = 4, rotation_deg = gabor_rotation) * signal_ratio * 2
    else:
        gabor_values = make_gabor(gabor_freq_cm = 3.5, rotation_deg = gabor_rotation) * signal_ratio * 2
    for i in range(number):
        filename = f"{stim_dir}/block_{block}/trial_{trial}/gabor_{i}.png"
        plotter(noise_values_list[i] + gabor_values + fixation_values, filename)
    return gabor_values

# Define a function to generate images with gabor, annulus, & noise
def make_gabor_annulus_img(number):
    for i in range(number):
        filename = f"{stim_dir}/block_{block}/trial_{trial}/gabor_ann_{i}.png"
        plotter(noise_values_list[i] + gabor_values + annulus_values + fixation_values, filename)

# Generate images
make_dir(stim_dir)
for block in range(n_blocks):
    # Generate parameters for all trials using multi_trial.py
    multi_trial(n_trials=n_trials, stim_dir=f'{stim_dir}/block_{block}')
    # Read parameters
    parameters = pd.read_csv(f'{stim_dir}/block_{block}/parameters.csv')
    gabor_freq = parameters['gabor_freq']
    correct_answer = parameters['correct_answer']
    snr_vec = parameters['snr']
    
    for trial in range(n_trials):
        snr = snr_vec[trial]
        noise_ratio = 1 / (snr+1)
        signal_ratio = 1 - noise_ratio
        fixation_values = make_fixation() * signal_ratio * 2
        annulus_values = make_annulus() * signal_ratio * 2
        # Generate images without annulus
        noise_values_list = make_noise_img(number)
        gabor_values = make_gabor_img(number)
        # Generate images with annulus
        if correct_answer[trial] == 'miss':
            make_annulus_img(number)
            make_gabor_annulus_img(number)






