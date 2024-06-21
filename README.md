## Descriptions:

This repository contains Python codes for a stop-signal task and for generating images with gabors, annulus, and a random noise background. Participants will need to fixate on a fixation in the center of the screen throughout the experiment. Random visual noise will change at 40 Hz (evoking a 40 Hz EEG response) and will be presented for 500 ms to 1000 ms. The Gabor embedded in visual noise will flicker at 30 Hz and will be presented for 1200 ms to 2000 ms. In stop trials, the annulus embedded in visual noise will flicker at 24 Hz and will be presented after the Gabor. The stop-signal delay which refers to the time between the onset of the Gabor and the onset of the annulus will range from 0 ms to 500 ms. A between-trial interval with a blank screen will be presented for 1500 ms to 2000 ms. All presenting times will be randomly drawn from uniform distributions.


## Installation & usage:

1. Before running the code, make sure you have installed Python 3.10.

2. Clone the repository and navigate to the root folder:
```sh
git clone https://github.com/thatmariia/stop-signal-task
cd stop-signal-task
```

3. Download and unpack the [zipped folders](https://amsuni-my.sharepoint.com/:f:/r/personal/m_turchina_uva_nl/Documents/stop-signal-task-zips?csf=1&web=1&e=zjwXDo) into the root directory of the project

4. Install the packages with pip: 
```sh
pip install -e .
```
This will install the package and its dependencies in editable mode, allowing you to make changes to the source code and have them reflected immediately.

5. You can now run either: `py_image_generation` and `py_experiment` (if you have the images already).

To generate images, run:
```sh
py_image_generation
```

To run the experiment, run:
```sh
py_experiment
```
