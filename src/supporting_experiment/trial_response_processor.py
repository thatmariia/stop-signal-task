from utils.globals import *
from psychopy import event

from supporting_experiment.sounds import Sounds


class TrialResponseProcessor:
    """
    The TrialResponseProcessor class is responsible for processing the responses of the participant in each trial.
    """

    def __init__(self):
        self.accu = 0
        self.response_list = []

    def reset(self):
        """
        Resets the accuracy counter.
        """

        self.accu = 0

    def process(self, trial, trial_i, correct_answer):
        """
        Processes the response of the participant in a trial.

        :param trial: the trial number
        :param trial_i: the trial index
        :param correct_answer: the correct answer for each trial
        """

        if parallel_ports.use:
            parallel_ports.port_write.setData(6)

        if parallel_ports.use:
            # TODO: read from parallel_ports.port_read instead of keyboard
            # response = event.getKeys(keyList=['f', 'j'])
            response = parallel_ports.port_read.readData()
            match response:
                case 109:
                    response = 'f'
                case 253:
                    response = 'j'
                case _:
                    response = []
            # left = 109, right = 253
        else:
            response = event.getKeys(keyList=['f', 'j'])

        self.response_list.append(response)

        # Record RT & keyboard responses
        timeee = config_exp.timer.getTime()

        if len(self.response_list[trial_i]) == 0:
            self.response_list[trial_i].append("miss")

        sounds = Sounds()

        # Auditory feedback on trial accuracy
        if self.response_list[trial_i][0] == correct_answer[trial]:
            if parallel_ports.use:
                parallel_ports.port_write.setData(6)
            sounds.correct_sound.play()
            self.accu += 1
        elif (self.response_list[trial_i][0] != correct_answer[trial]) and (correct_answer[trial] == "miss"):
            if parallel_ports.use:
                parallel_ports.port_write.setData(7)
            sounds.fail_to_stop_sound.play()
        else:
            if parallel_ports.use:
                parallel_ports.port_write.setData(8)
            sounds.incorrect_sound.play()
