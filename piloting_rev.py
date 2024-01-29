import os
import time
import random
from PIL import Image
from psychopy import visual, event, sound
from psychopy.event import Mouse
from ast import literal_eval
import numpy as np
import pandas as pd

# Parameters
win = visual.Window(size=[1440, 960], units="pix", fullscr=True)
n_blocks = 0
number = 20
noise_freq_hz, gabor_freq_hz, ann_freq_hz = 20, 15, 15
refresh_rate = 60
mouse = event.Mouse(visible=False)
mouse.setVisible(False)

# Record the refresh rate
# refresh_rate = win.getActualFrameRate(nIdentical=60, nMaxFrames=100, nWarmUpFrames=10, threshold=1)
# print(f"Refresh rate: {refresh_rate}")

component_lengths = refresh_rate / np.array([noise_freq_hz, gabor_freq_hz, ann_freq_hz])
noise_frame_length, gabor_frame_length, ann_frame_length = tuple([int(i) for i in component_lengths])

# Load sound
# Sound found on Freesound.org, made by "pan14" 
correct_sound = sound.Sound('correct.wav', stereo = True)
# Sound found on Freesound.org, made by "Autistic Lucario" 
incorrect_sound = sound.Sound('incorrect.wav', stereo = True)
# Sound found on Freesound.org, made by "kantouth"
fail_to_stop_sound = sound.Sound('fail_to_stop.wav', stereo = True)

# Load noise and noise_annulus images
noise_img = []
for i in range(number):
    file = Image.open(f'stimuli/noise/{i}.png')
    img = visual.ImageStim(win=win, image=file, colorSpace='rgb1', pos=(0, 0), size=(1000, 1000), units='pix')
    noise_img.append(img)
noise_annulus_img = []
for i in range(number):
    file = Image.open(f'stimuli/noise_annulus/{i}.png')
    img = visual.ImageStim(win=win, image=file, colorSpace='rgb1', pos=(0, 0), size=(1000, 1000), units='pix')
    noise_annulus_img.append(img)

# Define a function to show images
def show(list_name):
    if list_name == noise_gabor_annulus_img:
        stim = list_name[trial][img_index]
    else:
        stim = list_name[img_index]
    for i in range(frame_length_use[trial][img_counter]):
        stim.draw()
        win.flip()
        win.mouseVisible = False

# Instructions
low_img = visual.ImageStim(win=win, image=Image.open("instruction/low.png"), pos=(350, 80))
low_img.draw()
high_img = visual.ImageStim(win=win, image=Image.open("instruction/high.png"), pos=(-350, 80))
high_img.draw()
low_text = visual.TextStim(win, text="Low spatial frequency: press 'j'", pos=(350, -270), height=35)
low_text.draw()
high_text = visual.TextStim(win, text="High spatial frequency: press 'f'", pos=(-350, -270), height=35)
high_text.draw()
introduction_text = visual.TextStim(win, text="Press 'space' to practice.", pos=(0, -380), height=35)
introduction_text.draw()
win.flip()
keys = event.waitKeys(keyList=['space'])               

# Formal experiment
for block in range(-1, n_blocks):
    response_list = []
    trial_sum, accu = 0, 0
    
    # Load parameters from a pre-generated csv
    parameters = pd.read_csv(f'stimuli/block_{block}/parameters.csv')
    frame_length_use = parameters['frame_length'].apply(literal_eval)
    only_noise_frames = parameters['only_noise_frames']
    only_gabor_frames = parameters['only_gabor_frames']
    gabor_annulus_frames = parameters['gabor_annulus_frames']
    correct_answer = parameters['correct_answer']
    
    # Show pre-trial texts
    if block == -1:
        n_trials = 2
        loading_text = visual.TextStim(win, text="Loading images ...", height=45)
        loading_text.draw()
        win.flip()
    elif block == 0:
        n_trials = 0
        loading_text = visual.TextStim(win, text="Loading images ...", height=45)
        text.draw()
        win.flip()
    else:
        n_trials = 0
        text = visual.TextStim(win, text=f"Block {block} ends. Good job! Now please take a 30s break.", height=45)
        text.draw()
        win.flip()
    
    # Generate random trial order
    trial_order = list(range(n_trials))
    random.shuffle(trial_order)
    
    # Load noise_gabor_annulus images
    noise_gabor_annulus_img = [[] for _ in range(n_trials)]
    for trial in range(n_trials):
        if correct_answer[trial] == "miss":
            for i in range(number):
                file = Image.open(f'stimuli/block_{block}/trial_{trial}/annulus/{i}.png')
                img = visual.ImageStim(win=win, image=file, colorSpace='rgb1', pos=(0, 0), size=(1000, 1000), units='pix')
                noise_gabor_annulus_img[trial].append(img)
        else:
            noise_gabor_annulus_img[trial].append(0)
    
    text = visual.TextStim(win, text="Press 'space' to start.", height=45)
    text.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    
    # Reset the keyboard
    response = event.getKeys(keyList = ['f','j'])
    # Show images
    for trial in trial_order:
        noise_counter, gabor_counter, ann_counter, img_counter, gabor_on, ann_on, frame_length = 0, 0, 0, 0, 0, 0, 0
        
        win.flip()
        
        # Load noise_gabor images
        noise_gabor_img = []
        for i in range(number):
            file = Image.open(f'stimuli/block_{block}/trial_{trial}/{i}.png')
            img = visual.ImageStim(win=win, image=file, colorSpace='rgb1', pos=(0, 0), size=(1000, 1000), units='pix')
            noise_gabor_img.append(img)
        
        # Between-trial intervals
        time_load = timer.getTime()
        trial_interval = int(np.random.uniform(refresh_rate * (1.5-time_load), refresh_rate * (2-time_load)))
        for frame in range(trial_interval):
            win.flip()
            win.mouseVisible = False
        
        # Only noise
        for frame in range(only_noise_frames[trial]):
            if noise_counter == 0:
                img_index = random.randint(0, number - 1)
                new_image = True
            if new_image:
                show(noise_img)
                img_counter += 1
                new_image = False
            noise_counter += 1
            if noise_counter == noise_frame_length: 
                noise_counter = 0
        
        # Add gabor
        for frame in range(only_gabor_frames[trial]):
            if noise_counter == 0:
                img_index = random.randint(0, number - 1)
                new_image = True
            if gabor_counter == 0:
                gabor_on = -gabor_on + 1
                new_image = True
            if new_image:
                if gabor_on == 0:
                    show(noise_img)
                if gabor_on == 1:
                    show(noise_gabor_img)
                img_counter += 1
                new_image = False
            noise_counter += 1
            gabor_counter += 1
            if noise_counter == noise_frame_length: 
                noise_counter = 0 
            if gabor_counter == gabor_frame_length: 
                gabor_counter = 0 

        # Add annulus
        for frame in range(gabor_annulus_frames[trial]):
            if noise_counter == 0:
                img_index = random.randint(0, number - 1)
                new_image = True
            if gabor_counter == 0:
                gabor_on = -gabor_on + 1
                new_image = True
            if ann_counter == 0:
                ann_on = -ann_on + 1
                new_image = True
            if new_image:
                if gabor_on == 1 & ann_on == 1:
                    show(noise_gabor_annulus_img)
                if gabor_on == 0 & ann_on == 1:
                    show(noise_annulus_img)
                if gabor_on == 1 & ann_on == 0:
                    show(noise_gabor_img)
                if gabor_on == 0 & ann_on == 0:
                    show(noise_img)
                img_counter += 1
                new_image = False
            noise_counter += 1
            gabor_counter += 1
            ann_counter += 1
            if noise_counter == noise_frame_length: noise_counter = 0 
            if gabor_counter == gabor_frame_length: gabor_counter = 0 
            if ann_counter == ann_frame_length: ann_counter = 0
            
        response = event.getKeys(keyList = ['f','j'])
        response_list.append(response)
        if len(response_list[trial_sum]) == 0:
            response_list[trial_sum].append("miss")
        
        # Auditory feedback on trial accuracy
        if response_list[trial_sum][0] == correct_answer[trial]:
            correct_sound.play()
            accu += 1
        elif (response_list[trial_sum][0] != correct_answer[trial]) & (correct_answer[trial] == "miss"):
            fail_to_stop_sound.play()
        else:
            incorrect_sound.play()
        trial_sum += 1
    
    if block == -1:
        accuracy_rate = accu / n_trials
        text = visual.TextStim(win, text=f"Practice ends. Good job! Your accuracy rate is {accuracy_rate*100}%.", height=35)
        text.draw()
        text = visual.TextStim(win, text="Press 'space' to start the formal experiment.", pos=(0, -200), height=35)
        text.draw()
        win.flip()
        keys = event.waitKeys(keyList=['space'])  
