Descriptions:
This repository contains Python codes for a stop-signal task and for generating images with gabors, annulus, and a random noise background. Participants will need to fixate on a fixation in the center of the screen throughout the experiment. Random visual noise will change at 40 Hz (evoking a 40 Hz EEG response) and will be presented for 500 ms to 1000 ms. The Gabor embedded in visual noise will flicker at 30 Hz and will be presented for 1200 ms to 2000 ms. In stop trials, the annulus embedded in visual noise will flicker at 24 Hz and will be presented after the Gabor. The stop-signal delay which refers to the time between the onset of the Gabor and the onset of the annulus will range from 0 ms to 500 ms. A between-trial interval with a blank screen will be presented for 1500 ms to 2000 ms. All presenting times will be randomly drawn from uniform distributions.

Procedure:
1. Generate images using image_generator.py.
2. Run the experiment using piloting_rev.py.

Note. 
1. All images with the same number in the same trial share the same noise background.
2. If you are running the experiment with a limited RAM, it would be better to put the code in a large disk and manually increase virtual memory to avoid memory errors.
3. Need to be careful with EEG triggers in piloting_rev.py.
