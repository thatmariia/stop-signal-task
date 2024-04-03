# Written by Yiming Zhao (2024)

import os
import time
import random
from PIL import Image
from psychopy import visual, event, core, sound, parallel
from psychopy.event import Mouse
from ast import literal_eval
import numpy as np
import pandas as pd

# Parameters
n_blocks = 1
number = 20
noise_freq_hz, gabor_freq_hz, ann_freq_hz = 40, 30, 24
refresh_rate = 120
timer = core.Clock()

# Set-up EEG ports
global pp_write_address
global trigger_data

# Write address
pp_write_address = 0x4050
port_write = parallel.ParallelPort(address = pp_write_address)

# Create a window
bg_scale = [-1 + 2 * (90/255)] * 3
win = visual.Window(units = "pix",
                       allowGUI = False,
                       size = (2560, 1440),
                       color = bg_scale,
                       screen = 0,
                       fullscr = False,
                       waitBlanking = False)

# Record the refresh rate
refresh_rate_real = win.getActualFrameRate(nIdentical=60, nMaxFrames=100, nWarmUpFrames=10, threshold=1)
print(f"Refresh rate: {refresh_rate_real}")

# Don't record frame intervals
win.recordFrameIntervals = False

# Calculate the number of frames of every component
component_lengths = refresh_rate / np.array([noise_freq_hz, gabor_freq_hz, ann_freq_hz])
noise_frame_length, gabor_frame_length, ann_frame_length = tuple([int(i) for i in component_lengths])

# Load sound
# Sound found on Freesound.org, made by "pan14" 
correct_sound = sound.Sound('correct.wav', stereo = True)
# Sound found on Freesound.org, made by "Autistic Lucario" 
incorrect_sound = sound.Sound('incorrect.wav', stereo = True)
# Sound found on Freesound.org, made by "kantouth"
fail_to_stop_sound = sound.Sound('fail_to_stop.wav', stereo = True)          

# Define a function for the formal experiment
def experiment(n_trials, block):
    # Define a function to show images
    def show(list_name):
        stim = list_name[trial][img_index]
        for frame in range(frame_length_use[trial][img_counter]):
            stim.draw()
            win.flip()
            win.mouseVisible = False

    response_list = []
    rt_list = []
    trial_sum, accu = 0, 0
    
    # Load parameters from a pre-generated csv
    parameters = pd.read_csv(f'stimuli/block_{block}/parameters.csv')
    frame_length_use = parameters['frame_length'].apply(literal_eval)
    only_noise_frames = parameters['only_noise_frames']
    only_gabor_frames = parameters['only_gabor_frames']
    gabor_annulus_frames = parameters['gabor_annulus_frames']
    correct_answer = parameters['correct_answer']
    gabor_freq = parameters['gabor_freq']
    
    # Generate a random trial order
    trial_order = list(range(n_trials))
    random.shuffle(trial_order)
    
    # Create a random img order
    img_order = []
    for i in range(n_trials):
        img_order_part = []
        first_part = list(range(number))
        random.shuffle(first_part)
        img_order_part.extend(first_part)
        # 5 is used here because the number of img_index in each trial is always below 20*(5+1)=120
        # Img_index is changed every 3 frames (because the noise_img is changed every 3 frames)
        for _ in range(5):
            part = list(range(number))
            random.shuffle(part)
            # In case two images with the same noise background are drawn together
            while img_order_part[-1] == part[0]:
                random.shuffle(part)
            img_order_part.extend(part)
        img_order.append(img_order_part)
    
    # Load noise images
    noise_img = [[] for _ in range(n_trials)]
    for trial in range(n_trials):
        for i in range(number):
            file = Image.open(f'stimuli/block_{block}/trial_{trial}/noise_{i}.png')
            img = visual.ImageStim(win=win, image=file, colorSpace='rgb1', size=(1500, 1500), units='pix')
            noise_img[trial].append(img)
    
    # Load noise_gabor images
    noise_gabor_img = [[] for _ in range(n_trials)]
    for trial in range(n_trials):
        for i in range(number):
            file = Image.open(f'stimuli/block_{block}/trial_{trial}/gabor_{i}.png')
            img = visual.ImageStim(win=win, image=file, colorSpace='rgb1', size=(1500, 1500), units='pix')
            noise_gabor_img[trial].append(img)
    
    # Load noise_annulus images
    noise_annulus_img = [[] for _ in range(n_trials)]
    for trial in range(n_trials):
        if correct_answer[trial] == "miss":
            for i in range(number):
                file = Image.open(f'stimuli/block_{block}/trial_{trial}/annulus_{i}.png')
                img = visual.ImageStim(win=win, image=file, colorSpace='rgb1', size=(1500, 1500), units='pix')
                noise_annulus_img[trial].append(img)
            else:
                noise_annulus_img[trial].append(0)
    
    # Load noise_gabor_annulus images
    noise_gabor_annulus_img = [[] for _ in range(n_trials)]
    for trial in range(n_trials):
        if correct_answer[trial] == "miss":
            for i in range(number):
                file = Image.open(f'stimuli/block_{block}/trial_{trial}/gabor_ann_{i}.png')
                img = visual.ImageStim(win=win, image=file, colorSpace='rgb1', size=(1500, 1500), units='pix')
                noise_gabor_annulus_img[trial].append(img)
        else:
            noise_gabor_annulus_img[trial].append(0)
    
    text = visual.TextStim(win, text="Press 'space' to start.", height=45)
    text.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    
    # Show images
    response = event.getKeys(keyList = ['f','j'])
    for trial in trial_order:
        port_write.setData(1)
        key_record = True
        img_order_use = img_order[trial_sum]
        noise_counter, gabor_counter, ann_counter, img_counter, noise_img_counter, gabor_on, ann_on, frame_length, rt = 0, 0, 0, 0, 0, 0, 0, 0, 0
        win.flip()
        
        # Between-trial intervals
        trial_interval = int(np.random.uniform(refresh_rate * 1.5, refresh_rate * 2))
        for frame in range(trial_interval):
            win.flip()
            win.mouseVisible = False
        
        port_write.setData(2)
        # Only noise
        timer.reset()
        for frame in range(only_noise_frames[trial]):
            if noise_counter == 0:
                # img_index is used to locate the corresponding noise image
                # All images in the same trial with the same img_index has the same noise background
                img_index = img_order_use[noise_img_counter]
                noise_img_counter += 1
                new_image = True
            # Show a new image
            if new_image:
                show(noise_img)
                img_counter += 1
                new_image = False
            noise_counter += 1
            # If the number of frames of the currect image is equal to the component length
            # It is time to start a new image
            if noise_counter == noise_frame_length: 
                noise_counter = 0
        
        if gabor_freq[trial] == 3.5:
            port_write.setData(3)
        else:
            port_write.setData(4)
        # Add gabor
        for frame in range(only_gabor_frames[trial]):
            if noise_counter == 0:
                img_index = img_order_use[noise_img_counter]
                noise_img_counter += 1
                new_image = True
            if gabor_counter == 0:
                # If the previous gabor_on is 1, change it into 0, vice versa
                # This is used to control on and off of gabors
                gabor_on = -gabor_on + 1
                new_image = True
            if new_image:
                if gabor_on == 0:
                    show(noise_img)
                else :
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
        if correct_answer[trial] == "miss":
            port_write.setData(5)
        for frame in range(gabor_annulus_frames[trial]):
            if noise_counter == 0:
                img_index = img_order_use[noise_img_counter]
                noise_img_counter += 1
                new_image = True
            if gabor_counter == 0:
                gabor_on = -gabor_on + 1
                new_image = True
            if ann_counter == 0:
                ann_on = -ann_on + 1
                new_image = True
            if new_image:
                if gabor_on == 1 & ann_on == 0:
                    show(noise_gabor_img)
                elif gabor_on == 0 & ann_on == 0:
                    show(noise_img)
                elif gabor_on == 1 & ann_on == 1:
                    show(noise_gabor_annulus_img)
                else:
                    show(noise_annulus_img)
                img_counter += 1
                new_image = False
            noise_counter += 1
            gabor_counter += 1
            ann_counter += 1
            if noise_counter == noise_frame_length: noise_counter = 0 
            if gabor_counter == gabor_frame_length: gabor_counter = 0 
            if ann_counter == ann_frame_length: ann_counter = 0
        
        port_write.setData(6)
        response = event.getKeys(keyList = ['f','j'])
        response_list.append(response)
        # Record RT & keyboard responses
        timeee = timer.getTime()
        print(trial, timeee)
        if len(response_list[trial_sum]) == 0:
            response_list[trial_sum].append("miss")
        
        # Auditory feedback on trial accuracy
        if response_list[trial_sum][0] == correct_answer[trial]:
            #port_write.setData(6)
            correct_sound.play()
            accu += 1
        elif (response_list[trial_sum][0] != correct_answer[trial]) & (correct_answer[trial] == "miss"):
            #port_write.setData(7)
            fail_to_stop_sound.play()
        else:
            #port_write.setData(8)
            incorrect_sound.play()
        trial_sum += 1
    
    # Output the accuracy rate and a csv file
    accuracy_rate = accu / n_trials
    re_correct_answer = [correct_answer[i] for i in trial_order]
    output = pd.DataFrame({'trial': trial_order, 'correct_answer': re_correct_answer, 'response': response_list})
    output.to_csv(f"data/block_{block}.csv", index = False)
    
    return accuracy_rate
    
#########################
# Instructions
low_img = visual.ImageStim(win=win, image=Image.open("instruction/low.png"), pos=(600, 80))
low_img.draw()
high_img = visual.ImageStim(win=win, image=Image.open("instruction/high.png"), pos=(-600, 80))
high_img.draw()
low_text = visual.TextStim(win, text="Low spatial frequency: press 'j'", pos=(600, -360), height=35)
low_text.draw()
high_text = visual.TextStim(win, text="High spatial frequency: press 'f'", pos=(-600, -360), height=35)
high_text.draw()
introduction_text = visual.TextStim(win, text="Press 'space' to practice.", pos=(0, -420), height=35)
introduction_text.draw()
win.flip()
keys = event.waitKeys(keyList=['space'])

# Practice trials
#text = visual.TextStim(win, text="Loading images ...", height=45)
#text.draw()
#win.flip()
#accuracy_rate = experiment(n_trials=0, block=-1)
#text = visual.TextStim(win, text=f"Practice ends. Good job! Your accuracy rate is {accuracy_rate*100}%.", height=35)
#text.draw()
#text = visual.TextStim(win, text="Press 'space' to start the formal experiment.", pos=(0, -200), height=35)
#text.draw()
#win.flip()
#keys = event.waitKeys(keyList=['space'])
text = visual.TextStim(win, text="Loading images ...", height=45)
text.draw()
win.flip()

# Formal experiment
for my_block in range(n_blocks):
    accuracy_rate = experiment(n_trials=10, block=my_block)
    # This is the ending text for the last block
    if my_block == n_blocks - 1:
        text = visual.TextStim(win, text=f"This is the end of the experiment. Good job! Your accuracy rate is {accuracy_rate*100}%.", height=35)
        text.draw()
        text = visual.TextStim(win, text="Thank you for your participation!", pos=(0, -200), height=35)
        text.draw()
        win.flip()
        time.sleep(5)
    else:
        text = visual.TextStim(win, text=f"Block {my_block+1} ends. Good job! Your accuracy rate is {accuracy_rate*100}%.", height=35)
        text.draw()
        text = visual.TextStim(win, text="Now please take a 3min break.", pos=(0, -200), height=35)
        text.draw()
        win.flip()
