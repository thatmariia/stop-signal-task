from utils.globals import *

from PIL import Image
from psychopy import visual
import random
import numpy as np


class Images:
    """
    The Images class is responsible for loading and showing the images.
    """

    def __init__(self):
        self._noise_img = []
        self._noise_gabor_img = []
        self._noise_annulus_img = []
        self._noise_gabor_annulus_img = []

    def reset(self):
        """
        Resets the images.
        """

        self._noise_img = []
        self._noise_gabor_img = []
        self._noise_annulus_img = []
        self._noise_gabor_annulus_img = []

    def load(self, trial, block, correct_answer):
        """
        Loads the images for the given trial and block.

        :param trial: the trial
        :param block: the block
        :param correct_answer: the correct answer for the trial
        """

        self.reset()
        path = lambda img_type, x: f'{config.stim_dir}/block_{block}/trial_{trial}/{img_type}_{x}.png'

        def load_img(img_type, img_list):
            for i in range(config.number):
                with Image.open(path(img_type, i)) as file:
                    img = visual.ImageStim(win=config_exp.win, image=file, colorSpace='rgb1', size=(1500, 1500),
                                           units='pix')
                    img_list.append(img)

            return img_list

        # Load noise images
        self._noise_img = load_img("noise", self._noise_img)

        # Load noise_gabor images
        self._noise_gabor_img = load_img("gabor", self._noise_gabor_img)

        # Load noise_annulus images
        if correct_answer[trial] == "miss":
            self._noise_annulus_img = load_img("annulus", self._noise_annulus_img)
        else:
            self._noise_annulus_img.append(0)

        # Load noise_gabor_annulus images
        if correct_answer[trial] == "miss":
            self._noise_gabor_annulus_img = load_img("gabor_ann", self._noise_gabor_annulus_img)
        else:
            self._noise_gabor_annulus_img.append(0)

    def _between_trial_interval(self, loading_time=0):
        """
        The interval between trials.

        :param loading_time: the image loading time to subtract from the interval time
        """

        min_time = config.refresh_rate * max(0.0, 1.5 - loading_time)
        max_time = config.refresh_rate * max(0.0, 2 - loading_time)
        trial_interval = int(np.random.uniform(min_time, max_time))

        for _ in range(trial_interval):
            config_exp.win.flip()
            config_exp.win.mouseVisible = False

    def show(self, trial, params, img_order, loading_time=0):
        """
        Shows the images for the given trial.

        :param trial: the trial
        :param params: the block parameters
        :param img_order: the image order of the trial
        :param loading_time: the image loading time
        """

        noise_counter = gabor_counter = ann_counter = 0
        img_counter = noise_img_counter = 0
        gabor_on = ann_on = False
        img_index = img_order[0]
        new_image = False

        if parallel_ports.use:
            parallel_ports.port_write.setData(1)

        config_exp.win.flip()
        self._between_trial_interval(loading_time=loading_time)

        if parallel_ports.use:
            parallel_ports.port_write.setData(2)

        config_exp.timer.reset()

        def update_image(noise=False, gabor=False, ann=False):
            nonlocal img_index, noise_img_counter, new_image, gabor_on, ann_on
            if noise and noise_counter == 0:
                # img_index is used to locate the corresponding noise image
                # All images in the same trial with the same img_index has the same noise background
                img_index = img_order[noise_img_counter]
                noise_img_counter += 1
                new_image = True
            if gabor and gabor_counter == 0:
                # If the previous gabor_on is 1, change it into 0, vice versa
                # This is used to control on and off of gabors
                gabor_on = not gabor_on
                new_image = True
            if ann and ann_counter == 0:
                ann_on = not ann_on
                new_image = True

        def show(list_name):
            stim = list_name[img_index]
            for _ in range(params.frame_length_use[trial][img_counter]):
                stim.draw()
                config_exp.win.flip()
                config_exp.win.mouseVisible = False

        def show_new_image(local_gabor_on=False, local_ann_on=False):
            nonlocal new_image, img_counter
            if new_image:
                match local_gabor_on, local_ann_on:
                    case (False, False):
                        show(self._noise_img)
                    case (True, False):
                        show(self._noise_gabor_img)
                    case (True, True):
                        show(self._noise_gabor_annulus_img)
                    case (False, True):
                        show(self._noise_annulus_img)

                img_counter += 1
                new_image = False

        def update_counters(noise=False, gabor=False, ann=False):
            nonlocal noise_counter, gabor_counter, ann_counter
            # If the number of frames of the currect image is equal to the component length
            # It is time to start a new image
            if noise:
                noise_counter += 1
                if noise_counter == config.noise_frame_length:
                    noise_counter = 0
            if gabor:
                gabor_counter += 1
                if gabor_counter == config.gabor_frame_length:
                    gabor_counter = 0
            if ann:
                ann_counter += 1
                if ann_counter == config.ann_frame_length:
                    ann_counter = 0

        # Only noise
        for frame in range(params.only_noise_frames[trial]):
            update_image(noise=True)
            show_new_image()
            update_counters(noise=True)

        if parallel_ports.use:
            parallel_ports.port_write.setData(3 if params.gabor_freq[trial] == 3.5 else 4)

        # Add gabor
        for frame in range(params.only_gabor_frames[trial]):
            update_image(noise=True, gabor=True)
            show_new_image(gabor_on)
            update_counters(noise=True, gabor=True)

        # Add annulus
        if (params.correct_answer[trial] == "miss") and parallel_ports.use:
            parallel_ports.port_write.setData(5)

        for frame in range(params.gabor_annulus_frames[trial]):
            update_image(noise=True, gabor=True, ann=True)
            show_new_image(gabor_on, ann_on)
            update_counters(noise=True, gabor=True, ann=True)

        config_exp.win.flip()

    @staticmethod
    def create_random_order():
        """
        Creates a random image order for the experiment.
        """

        img_order = []
        for i in range(config.n_trials):
            img_order_part = []
            first_part = list(range(config.number))
            random.shuffle(first_part)
            img_order_part.extend(first_part)
            # 5 is used here because the number of img_index in each trial is always below 20*(5+1)=120
            # Img_index is changed every 3 frames (because the noise_img is changed every 3 frames)
            for _ in range(5):
                part = list(range(config.number))
                random.shuffle(part)
                # In case two images with the same noise background are drawn together
                while img_order_part[-1] == part[0]:
                    random.shuffle(part)
                img_order_part.extend(part)
            img_order.append(img_order_part)

        return img_order
