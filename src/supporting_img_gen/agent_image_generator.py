from tqdm import tqdm
import os
import numpy as np
import random
import scipy.stats as stats
import pandas as pd

from supporting_img_gen.block_params_img_gen import BlockParamsImgGen
from supporting_img_gen.elements_generator import ElementsGenerator
from supporting_img_gen.type_img_generator import TypeImgGenerator
from utils.globals import *


class ImageGenerator:
    """
    The ImageGenerator class is responsible for generating the images for the experiment.
    """

    def generate(self):
        """
        Generates all the images for the experiment.
        """

        self._make_dir()

        elements_generator = ElementsGenerator()
        fix_mat = elements_generator.make_fixation()
        ann_mat = elements_generator.make_annulus()

        params = BlockParamsImgGen()
        type_img_gen = TypeImgGenerator(elements_generator=elements_generator)

        with tqdm(total=config.n_blocks * config.n_trials) as pbar:
            for block in range(config.n_blocks):

                # Generate parameters for all trials using multi_trial.py
                self._multi_trial(block_dir=f'{config.stim_dir}/block_{block}')

                # Read parameters
                params.update(block=block)

                for trial in range(config.n_trials):

                    snr = params.snr_vec[trial]
                    noise_ratio = 1 / (snr + 1)
                    signal_ratio = 1 - noise_ratio

                    fixation_values = fix_mat * signal_ratio * 2
                    annulus_values = ann_mat * signal_ratio * 2

                    type_img_gen.update(
                        params=params,
                        trial=trial,
                        block=block,
                        noise_ratio=noise_ratio,
                        signal_ratio=signal_ratio,
                        fixation_values=fixation_values,
                        annulus_values=annulus_values
                    )

                    # Generate images without annulus
                    noise_values_list = type_img_gen.make_noise_img()
                    gabor_values = type_img_gen.make_gabor_img(noise_values_list=noise_values_list)

                    # Generate images with annulus
                    if params.correct_answer[trial] == 'miss':
                        type_img_gen.make_annulus_img(noise_values_list)
                        type_img_gen.make_gabor_annulus_img(noise_values_list, gabor_values)

                    pbar.update(1)

    def _multi_trial(self, block_dir, stop_trial_prob=1 / 3):
        """
        Generates parameters for all trials in a block.

        :param block_dir: the directory of the block
        :param stop_trial_prob: the probability of a stop trial (default is 1/3)
        """

        # binomial distribution; the probability of stop_trial is stop_trial_prop; draw n_trials numbers
        stop_trials = stats.bernoulli.rvs(p=stop_trial_prob, size=config.n_trials)
        # transform the generated random numbers into Boolean values
        stop_trials = [bool(i) for i in stop_trials]

        # set the probability of high and low spatial frequency conditions
        gabor_freq_set = stats.bernoulli.rvs(p=config_gen.gabor_freq_prob, size=config.n_trials)
        gabor_freq = np.where(gabor_freq_set == 0, 3.5, 4)

        # randomly draw the length of cue intervals and response intervals from a uniform distribution
        snr_vec = np.random.gamma(10, 1 / 60, config.n_trials)
        only_noise_ms_vec = [random.uniform(500, 1000) for _ in range(config.n_trials)]
        only_gabor_ms_vec = [np.random.exponential(scale=500) for _ in range(config.n_trials)] # Added by Michael 14-Oct-2024
        trial_length_ms_vec = [random.uniform(1200, 2000) for _ in range(config.n_trials)]

        frame_length_use = []
        noise_frames_use = []
        gabor_frames_use = []
        annulus_frames_use = []
        correct_answer = []

        for i in range(config.n_trials):
            frame_lengths_arr, noise_frames, only_gabor_frames, gabor_ann_frames = self._single_trial(
                stop_trial=stop_trials[i],
                only_noise_ms=only_noise_ms_vec[i],
                only_gabor_ms=only_gabor_ms_vec[i],
                trial_length_ms=trial_length_ms_vec[i]
            )

            # generate correct answers trial by trial
            if stop_trials[i]:
                correct_answer.append("miss")
            else:
                answer = "j" if gabor_freq[i] == 3.5 else "f"
                correct_answer.append(answer)

            frame_length_use.append(frame_lengths_arr)
            noise_frames_use.append(noise_frames)
            gabor_frames_use.append(only_gabor_frames)
            annulus_frames_use.append(gabor_ann_frames)

        parameters = pd.DataFrame({
            'trial': list(range(config.n_trials)),
            'correct_answer': correct_answer,
            'gabor_freq': gabor_freq,
            'snr': snr_vec,
            'only_noise_frames': noise_frames_use,
            'only_gabor_frames': gabor_frames_use,
            'gabor_annulus_frames': annulus_frames_use,
            'frame_length': frame_length_use
        })
        parameters.to_csv(block_dir + "/parameters.csv", index=False)

        # return frame_length_use

    def _single_trial(
            self,
            stop_trial=True,
            only_noise_ms=500.0,
            only_gabor_ms=500.0,
            trial_length_ms=2000.0
    ):
        """
        Generates the frame lengths for a single trial.

        :param stop_trial: whether the trial is a stop trial
        :param only_noise_ms: the duration of the noise only period in ms
        :param only_gabor_ms: the duration of the gabor period in ms
        :param trial_length_ms: the duration of the trial in ms
        :return: the frame lengths for the trial
        """

        noise_frames = int(only_noise_ms / 1000 * config.refresh_rate)
        if stop_trial:
            only_gabor_frames = int(only_gabor_ms / 1000 * config.refresh_rate)
            trial_frames = int(trial_length_ms / 1000 * config.refresh_rate)
            if only_gabor_frames < trial_frames: # Added by Michael 14-Oct-2024
                gabor_ann_frames = trial_frames - only_gabor_frames
            else:
                gabor_ann_frames = 0
        else:
            only_gabor_frames = int(trial_length_ms / 1000 * config.refresh_rate)
            gabor_ann_frames = 0

        noise_counter = gabor_counter = ann_counter = 0
        img_counter = 0
        gabor_on = ann_on = False
        new_image = False

        frame_lengths_arr = np.empty(1)
        frame_length = 0

        def update_image(noise=False, gabor=False, ann=False):
            nonlocal gabor_on, ann_on, new_image
            if noise and noise_counter == 0:
                new_image = True
            if gabor and gabor_counter == 0:
                gabor_on = not gabor_on
                new_image = True
            if ann and ann_counter == 0:
                ann_on = not ann_on
                new_image = True

        def handle_new_image(only_noise=False):
            nonlocal new_image, img_counter, frame_lengths_arr, frame_length
            if new_image:
                if only_noise:
                    img_counter += 1
                frame_lengths_arr = np.append(frame_lengths_arr, frame_length)
                frame_length = 1
                new_image = False
            else:
                frame_length += 1

        def update_counters(noise=False, gabor=False, ann=False):
            nonlocal noise_counter, gabor_counter, ann_counter
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

        # only noise
        for i in range(noise_frames):
            update_image(noise=True)
            handle_new_image(only_noise=True)
            update_counters(noise=True)

        # add gabor
        for i in range(only_gabor_frames):
            update_image(noise=True, gabor=True)
            handle_new_image()
            update_counters(noise=True, gabor=True)

        # add annulus
        for i in range(gabor_ann_frames):
            update_image(noise=True, gabor=True, ann=True)
            handle_new_image()
            update_counters(noise=True, gabor=True, ann=True)

        frame_lengths_arr = np.append(frame_lengths_arr, frame_length)[2:]
        frame_lengths_arr = [int(i) for i in frame_lengths_arr]

        return frame_lengths_arr, noise_frames, only_gabor_frames, gabor_ann_frames


    @staticmethod
    def _make_dir():
        """
        Makes the directories for the images.
        """

        stim_dirs_block = [config.stim_dir + "/block_" + str(i) for i in range(config.n_blocks)]

        for block in range(config.n_blocks):
            try:
                os.mkdir(stim_dirs_block[block])
            except OSError:
                print(f'Directory block_{block} alredy exists. Files overwritten.')

            for trial in range(config.n_trials):
                stim_dirs_trial = stim_dirs_block[block] + f"/trial_{trial}"
                try:
                    os.mkdir(stim_dirs_trial)
                except OSError:
                    print(f'Directory trial_{trial} alredy exists. Files overwritten.')
