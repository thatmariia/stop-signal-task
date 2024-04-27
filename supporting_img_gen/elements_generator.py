import numpy as np
import matplotlib.pyplot as plt

from globals import *


class ElementsGenerator:
    """
    The ElementsGenerator class is responsible for generating the elements of the visual stimuli.
    Based on:
    Michael Nunez's makefixation.m, makenoise.m, makegabor.m, makeannulus.m (2016);
    Konrad Mikalauskas (2022)
    """

    @staticmethod
    def make_gabor(radius_cm=10, gabor_size_cm=6, rotation_deg=45, gabor_freq_cm=5):
        """
        Generates a Gabor patch.
        """

        # pixelize
        radius = round(radius_cm * config_gen.ppcm)
        gabor_size = round(gabor_size_cm * config_gen.ppcm)
        gabor_freq = gabor_freq_cm / config_gen.ppcm

        half_gabor = np.floor(gabor_size / 2)

        image_px = 2 * radius
        x_grid = np.empty((image_px, image_px))
        y_grid = np.empty((image_px, image_px))

        index = 0
        for i in range(-radius + 1, radius + 1):
            x_grid[:, index] = i
            y_grid[index, :] = i
            index += 1

        # degrees to radians
        rand_phase_rad = np.random.uniform() * 2 * np.pi
        rotation_rad = rotation_deg * (np.pi / 180)

        # rand_place = np.random.randint(1, np.floor((2*radius-gabor_size)/3), 2) * np.array((np.sin(90.*np.random.uniform()), np.sin(90.*np.random.uniform())))
        # rand_dir = 3 - 2*np.random.randint(1, 3, 2)
        # shift = rand_place * rand_dir
        shift = np.array((0, 0))

        x_p = x_grid * np.cos(rotation_rad) + y_grid * np.sin(rotation_rad) + shift[0]
        y_p = y_grid * np.cos(rotation_rad) - x_grid * np.sin(rotation_rad) + shift[1]

        gabor_mat = np.exp(
            -((x_p / (half_gabor / 2)) ** 2) - (0.4 * (y_p / (half_gabor / 2)) ** 2)
        ) * np.sin(2 * np.pi * gabor_freq * (x_p) + rand_phase_rad)

        # standardize matrix values to [-1, 1]
        gabor_mat = ((gabor_mat - gabor_mat.min()) / (gabor_mat.max() - gabor_mat.min()) - 0.5) * 0.5

        # make gabor matrix circular
        xc = np.empty((image_px, image_px))
        yc = np.empty((image_px, image_px))
        for i in range(0, image_px):
            xc[:, i] = i + 1
            yc[i, :] = i + 1
        z = np.sqrt((xc - radius) ** 2 + (yc - radius) ** 2)
        gabor_mat[z > radius] = np.nan

        # plot
        if config_gen.plot:
            plt.figure()
            plt.imshow(gabor_mat, cmap='gray')
            # plt.show()

        return gabor_mat

    @staticmethod
    def make_noise(radius_cm=10, num_bands=2, sd_pass_cm=20, freq_bands_cm=None):
        """
        Generates noise.
        """

        if freq_bands_cm is None:
            freq_bands_cm = [1, 5]  # default value

        # pixelize
        radius = round(radius_cm * config_gen.ppcm)
        sd_pass = sd_pass_cm / config_gen.ppcm
        freq_bands = freq_bands_cm / config_gen.ppcm

        # x and y coords in cm
        image_px = 2 * radius
        x_grid = np.empty((image_px, image_px))
        y_grid = np.empty((image_px, image_px))

        index = 0
        for i in np.linspace(-1, 1, image_px + 1)[1:]:
            x_grid[:, index] = i
            y_grid[index, :] = i
            index += 1

        # distance of points to center
        radii = np.sqrt(x_grid ** 2 + y_grid ** 2)

        # magic
        unfilt_noise = np.random.normal(size=(image_px, image_px))
        fourier_mat = np.fft.fftshift(np.fft.fft2(unfilt_noise - np.mean(unfilt_noise)))

        bandpass = np.zeros((image_px, image_px))
        for i in range(0, num_bands):
            bandpass += np.exp(-((radii - 2 * freq_bands[i]) ** 2) / 2 / sd_pass ** 2)

        spec_mat = fourier_mat * bandpass
        noise_mat = np.fft.ifft2(np.fft.fftshift(spec_mat) + np.mean(unfilt_noise)).real

        # standardize matrix values to [0.25, 0.75]
        noise_mat = ((noise_mat - noise_mat.min()) / (noise_mat.max() - noise_mat.min())) / 2 + 0.25
        # noise_mat[666,666] = 1
        # noise_mat[666,-666] = 0

        # make the noise matrix circular
        xc = np.empty((image_px, image_px))
        yc = np.empty((image_px, image_px))
        for i in range(0, image_px):
            xc[:, i] = i + 1
            yc[i, :] = i + 1
        z = np.sqrt((xc - radius) ** 2 + (yc - radius) ** 2)
        noise_mat[z > radius] = np.nan

        # plot
        if config_gen.plot:
            plt.figure()
            plt.imshow(noise_mat, cmap='gray')
            # plt.show()

        return noise_mat

    @staticmethod
    def make_annulus(radius_cm=10, ann_dist_cm=7, ann_width_cm=1, alpha=0.5):
        """
        Generates an annulus.
        """

        # pixelize
        radius = round(radius_cm * config_gen.ppcm)
        ann_dist = round(ann_dist_cm * config_gen.ppcm)
        ann_width = round(ann_width_cm * config_gen.ppcm)

        image_px = 2 * radius
        ann_mat = np.zeros((image_px, image_px))

        # make annulus
        xc = np.empty((image_px, image_px))
        yc = np.empty((image_px, image_px))
        for i in range(0, image_px):
            xc[:, i] = i + 1
            yc[i, :] = i + 1
        z = np.sqrt((xc - radius) ** 2 + (yc - radius) ** 2)
        r_half = np.sqrt((2 * ann_dist ** 2 + ann_width ** 2 / 2) / 2)

        ann_mat[z > (ann_dist - ann_width / 2)] = 0.25
        ann_mat[z > r_half] = -0.25
        ann_mat[z > (ann_dist + ann_width / 2)] = 0
        ann_mat[z > radius] = np.nan

        # plot
        if config_gen.plot:
            plt.figure()
            plt.imshow(ann_mat, cmap='gray', alpha=alpha)
            # plt.show()

        return ann_mat

    @staticmethod
    def make_fixation(radius_cm=10, fixation_cm=0.2):
        """
        Generates a fixation point.
        """

        # pixelize
        radius = round(radius_cm * config_gen.ppcm)
        fix = round(fixation_cm * config_gen.ppcm)

        image_px = 2 * radius
        fix_mat = np.zeros((image_px, image_px))

        # make fixation matrix circular
        xc = np.empty((image_px, image_px))
        yc = np.empty((image_px, image_px))
        for i in range(0, image_px):
            xc[:, i] = i + 1
            yc[i, :] = i + 1
        z = np.sqrt((xc - radius) ** 2 + (yc - radius) ** 2)
        fix_mat[z > radius] = np.nan

        # make fixation point
        fix_mat[z < fix] = -10

        # plot
        if config_gen.plot:
            plt.figure()
            plt.imshow(fix_mat, cmap='gray')
            # plt.show()

        return fix_mat
