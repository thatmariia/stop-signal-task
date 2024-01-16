import os
from PIL import Image
from psychopy import visual, event, core
import pickle
import pandas as pd

# create a window
win = visual.Window(size = [1440, 960], units="pix", fullscr = True)
n_trials = 1
n_blocks = 1
timer = core.Clock()
# record the refresh rate
refresh_rate = win.getActualFrameRate(nIdentical=60, nMaxFrames=100,
    nWarmUpFrames=10, threshold=1)
print(f"Refresh rate: {refresh_rate}")

# EEG related?
# Set-up EEG ports
##global pp_write_address
##global trigger_data
# Write address
##pp_write_address = 0x4050
##port_write = parallel.ParallelPort(address = pp_write_address)
# Read address
##pp_read_address = 0x4051
##port_read = parallel.ParallelPort(address = pp_read_address) # statusDefault is 125

# load the frame_length_use from multi_trial.py
with open('frame_length_use.pkl', 'rb') as file:
    frame_length_use = pickle.load(file)
with open('noise_frames_use.pkl', 'rb') as file:
    noise_frames_use = pickle.load(file)
with open('image.pkl', 'rb') as file:
    stim_img = pickle.load(file)

# store images into a list
for trial in range(n_trials):
    for img in range(len(stim_img[trial])):
        stim_img[trial][img] = visual.ImageStim(
            win = win,
            image = stim_img[trial][img],
            colorSpace = 'rgb1',
            pos = (0, 0),
            size = (1000, 1000),
            units = 'pix')

# instructions
thin_img = visual.ImageStim(win = win, image = Image.open("instruction/thin.png"), pos = (350, 80))
thin_img.draw()
thick_img = visual.ImageStim(win = win, image = Image.open("instruction/thick.png"), pos = (-350, 80))
thick_img.draw()
thin_text = visual.TextStim(win, text = "thin gabor: press 'j'", color = (1,1,1), pos = (350, -250))
thin_text.draw()
thick_text = visual.TextStim(win, text = "thick gabor: press 'f'", color = (1,1,1), pos = (-350, -250))
thick_text.draw()
introduction_text = visual.TextStim(win, text = "press 'space' to start", color = (1,1,1), pos = (0, -350))
introduction_text.draw()
win.flip()
keys = event.waitKeys(keyList=['space'])               

# show images
for block in range(n_blocks):
    response_list = []
    rt_list = []
    for trial in range(n_trials):
        ##timer.reset()
        frame_counter = 0
        rt = 0
        key_record = True
        for img in range(len(stim_img[trial])):
            # Another possible way to draw and flip the image: use time.sleep and calculate time using (frames/refresh rate)
            for frame in range(frame_length_use[trial][img]):
                win.mouseVisible = False
                # when the gabor starts to show up, reset the timer
                if frame_counter == noise_frames_use[trial]:
                    timer.reset()
                stim_img[trial][img].draw()
                win.flip()
                frame_counter += 1
                # record keyboard responses and RT
                response = event.getKeys(keyList = ['f','j'])
                # when having multiple keyboard responses, only record the first one
                if len(response) > 0 and key_record:
                    rt = timer.getTime()
                    print(f"Block {block+1}: Trial {trial+1}: Response: {response[0]} RT: {rt}")
                    response_list.append(response[0])
                    rt_list.append(rt)
                    key_record = False
        # rt == 0 means that no keyboard response was made
        if rt == 0:
            print(f"Block {block+1}: Trial {trial+1}: Response: Miss")
            response_list.append("Miss")
            rt_list.append(rt)
        ##a = timer.getTime()
        #print(f"length of trial {trial+1}: {a}")
        
    df = pd.DataFrame({'Keyboard_response': response_list, 'RT': rt_list})
    df.to_csv('stimuli/output.csv', index = False)
        
    text = visual.TextStim(win, text = f"Block {block+1} ends. Good work! Press 'space' to enter the next block.")
    text.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])