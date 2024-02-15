from make_gabor import *
import pickle
import random
import pandas as pd

n_trials = 90

snr = 1/3
noise_ratio = 1 / (snr+1)
signal_ratio = 1 - noise_ratio

parameters = pd.read_csv('stimuli/parameters.csv')
correct_answer = parameters['correct_answer']

gabor_values_list = []
for trial in range(n_trials):
    gabor_rotation = random.randint(0, 180)
    if correct_answer[trial] == 'f':
        gabor_values = make_gabor(gabor_freq_cm = 5, rotation_deg = gabor_rotation) * signal_ratio * 2
    else:
        gabor_values = make_gabor(gabor_freq_cm = 3, rotation_deg = gabor_rotation) * signal_ratio * 2
    gabor_values_list.append(gabor_values)

with open('gabor_values_list.pkl', 'wb') as file:
    pickle.dump(gabor_values_list, file)









