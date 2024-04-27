#from psychopy import sound
from psychopy.sound import Sound


class Sounds:
    """
    The Sounds class is responsible for loading and playing sounds in the experiment.
    """

    def __init__(self):
        # Load sound
        # Sound found on Freesound.org, made by "pan14"
        self.correct_sound = Sound('sounds/correct.wav', stereo=True)
        # Sound found on Freesound.org, made by "Autistic Lucario"
        self.incorrect_sound = Sound('sounds/incorrect.wav', stereo=True)
        # Sound found on Freesound.org, made by "kantouth"
        self.fail_to_stop_sound = Sound('sounds/fail_to_stop.wav', stereo=True)


