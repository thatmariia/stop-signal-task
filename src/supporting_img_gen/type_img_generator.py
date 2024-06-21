import random
import matplotlib.pyplot as plt

from utils.globals import *


class TypeImgGenerator:
    """
    The TypeImgGenerator class is responsible for generating the images of the visual stimuli.
    """

    def __init__(self, elements_generator):
        self._elements_generator = elements_generator

        self._params = None
        self._trial = None
        self._block = None
        self._noise_ratio = None
        self._signal_ratio = None
        self._fixation_values = None
        self._annulus_values = None

    def update(
            self,
            params,
            trial,
            block,
            noise_ratio,
            signal_ratio,
            fixation_values,
            annulus_values
    ):
        """
        Updates the parameters of the TypeImgGenerator.

        :param params: block parameters
        :param trial: trial number
        :param block: block number
        :param noise_ratio: noise ratio
        :param signal_ratio: signal ratio
        :param fixation_values: fixation values
        :param annulus_values: annulus values
        """

        self._params = params
        self._trial = trial
        self._block = block
        self._noise_ratio = noise_ratio
        self._signal_ratio = signal_ratio
        self._fixation_values = fixation_values
        self._annulus_values = annulus_values

    def make_gabor_annulus_img(self, noise_values_list, gabor_values):
        """
        Generates the images of the visual stimuli with Gabor and annulus.
        """

        for i in range(config.number):
            filename = f"{config.stim_dir}/block_{self._block}/trial_{self._trial}/gabor_ann_{i}.png"
            self._plotter(noise_values_list[i] + gabor_values + self._annulus_values + self._fixation_values, filename)

    def make_annulus_img(self, noise_values_list):
        """
        Generates the images of the visual stimuli with annulus.
        """

        for i in range(config.number):
            filename = f"{config.stim_dir}/block_{self._block}/trial_{self._trial}/annulus_{i}.png"
            self._plotter(noise_values_list[i] + self._annulus_values + self._fixation_values, filename)

    def make_gabor_img(self, noise_values_list):
        """
        Generates the images of the visual stimuli with Gabor.

        :return: the Gabor values
        """

        gabor_rotation = random.randint(0, 180)

        gabor_freq_cm = 4 if self._params.gabor_freq[self._trial] == 4 else 3.5
        gabor = self._elements_generator.make_gabor(
            gabor_freq_cm=gabor_freq_cm,
            rotation_deg=gabor_rotation
        )
        gabor_values = gabor * self._signal_ratio * 2

        for i in range(config.number):
            filename = f"{config.stim_dir}/block_{self._block}/trial_{self._trial}/gabor_{i}.png"
            self._plotter(noise_values_list[i] + gabor_values + self._fixation_values, filename)

        return gabor_values

    def make_noise_img(self):
        """
        Generates the images of the visual stimuli with noise.

        :return: the noise values
        """

        noise_values_list = []

        for i in range(config.number):
            noise = self._elements_generator.make_noise()
            noise_values = (noise - 0.25) * 2 * self._noise_ratio + 0.5 * self._signal_ratio
            noise_values_list.append(noise_values)

            filename = f"{config.stim_dir}/block_{self._block}/trial_{self._trial}/noise_{i}.png"
            self._plotter(noise_values + self._fixation_values, filename)

        return noise_values_list

    @staticmethod
    def _plotter(value_matrix, image_name):
        """
        Makes and saves the image.
        """

        plt.figure(
            figsize=(
                config_gen.image_size / config_gen.my_dpi,
                config_gen.image_size / config_gen.my_dpi
            ),
            dpi=config_gen.my_dpi
        )
        plt.xticks([])
        plt.yticks([])
        plt.axis('off')
        plt.imshow(value_matrix, vmin=0, vmax=1, cmap='gray')
        plt.savefig(image_name, dpi=config_gen.my_dpi, transparent=True)
        plt.close('all')
        plt.clf()
        plt.cla()
