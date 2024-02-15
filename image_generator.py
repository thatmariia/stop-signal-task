import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import pickle
import os
import scipy.stats as stats

from make_noise import *
from make_gabor import *
from make_annulus import *
from make_fixation import *

number = 20
n_trials = 90

snr = 1/3
noise_ratio = 1 / (snr+1)
signal_ratio = 1 - noise_ratio
image_size = 1024
my_dpi = 109
gabor_freq_prob = 0.5
stim_dir = "stimuli/block_-1"

parameters = pd.read_csv('stimuli/parameters.csv')
correct_answer = parameters['correct_answer']
stop_trials = parameters.loc[parameters['correct_answer'] == 'miss', 'trial']
# high frequency = 'f', low frequency = 'j'

# load image values
fixation_values = make_fixation() * signal_ratio * 2
annulus_values = make_annulus() * signal_ratio * 2
with open('noise_values_list.pkl', 'rb') as file:
    noise_values_list = pickle.load(file)
with open('gabor_values_list.pkl', 'rb') as file:
    gabor_values_list = pickle.load(file)

def make_dir(stim_dir):
    stim_dirs = [stim_dir + "/trial_" + str(i) for i in range(n_trials)]
    stim_dirs_ann = [stim_dirs[i] + "/annulus" for i in range(n_trials)]
    for i in range(0, n_trials):
        try:
            os.mkdir(stim_dirs[i])
            os.mkdir(stim_dirs_ann[i])
        except OSError:
            print('Directory {} alredy exists. Files overwritten.'.format(stim_dirs[i])) 
make_dir(stim_dir)

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

def make_noise_img(number):
    for i in range(number):
        noise_values = noise_values_list[i]
        filename = stim_dir + f"/noise/{i}.png"
        plotter(noise_values + fixation_values, filename)
#make_noise_img(number = number)

def make_annulus_img(number):
    for i in range(number):
        noise_values = noise_values_list[i]
        annulus_values = make_annulus() * signal_ratio * 2
        filename = stim_dir + f"/noise_annulus/{i}.png"
        plotter(noise_values + annulus_values + fixation_values, filename)
#make_annulus_img(number = number)

def make_gabor_img(n_trials, number):
    for trial in range(n_trials):
        gabor_values = gabor_values_list[trial]
        for i in range(number):
            noise_values = noise_values_list[i]
            filename = stim_dir + f"/trial_{trial}/{i}.png"
            plotter(noise_values + gabor_values + fixation_values, filename)
make_gabor_img(n_trials = 20, number = 20)

def make_gabor_annulus_img(number):
    for trial in stop_trials:
        gabor_values = gabor_values_list[trial]
        for i in range(number):
            noise_values = noise_values_list[i]
            filename = stim_dir + f"/trial_{trial}/annulus/{i}.png"
            plotter(noise_values + gabor_values + annulus_values + fixation_values, filename)
make_gabor_annulus_img(number = number)






