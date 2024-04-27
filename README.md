Descriptions:

This repository contains Python codes for a stop-signal task and for generating images with gabors, annulus, and a random noise background. Participants will need to fixate on a fixation in the center of the screen throughout the experiment. Random visual noise will change at 40 Hz (evoking a 40 Hz EEG response) and will be presented for 500 ms to 1000 ms. The Gabor embedded in visual noise will flicker at 30 Hz and will be presented for 1200 ms to 2000 ms. In stop trials, the annulus embedded in visual noise will flicker at 24 Hz and will be presented after the Gabor. The stop-signal delay which refers to the time between the onset of the Gabor and the onset of the annulus will range from 0 ms to 500 ms. A between-trial interval with a blank screen will be presented for 1500 ms to 2000 ms. All presenting times will be randomly drawn from uniform distributions.

Requirements:
* Python 3.10
* For packages, see requirements.txt

Procedure:
1. Download and unpack the [zipped folders](https://amsuni-my.sharepoint.com/:f:/r/personal/m_turchina_uva_nl/Documents/stop-signal-task-zips?csf=1&web=1&e=zjwXDo) into the root directory
2. Open main.py
3. Set `project_part = ProjectPart.IMG_GEN` to generate images or `project_part = ProjectPart.EXPERIMENT` to run the experiment
4. Run main.py
