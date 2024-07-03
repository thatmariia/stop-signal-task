import time
from psychopy import visual, event
import pandas as pd
import random
from psychopy import core
import gc

from utils.globals import *
from supporting_experiment.visuals import Visuals
from supporting_experiment.block_params_experiment import BlockParamsExperiment
from supporting_experiment.images import Images
from supporting_experiment.trial_response_processor import TrialResponseProcessor


class FormalExperiment:
    """
    The FormalExperiment class is responsible for running the experiment.
    """

    def run(self):
        """
        Runs the entire experiment with instructions and block, trials.
        """

        visuals = Visuals()

        # Instructions
        visuals.show_instructions()
        keys = event.waitKeys(keyList=['space'])

        # Practice trials
        # self._practice_trials()

        # Formal experiment
        for block in range(config.n_blocks):
            accuracy_rate = self._experiment(block=block)
            # This is the ending text for the last block
            if block == config.n_blocks - 1:
                visuals.show_after_experiment_screen(accuracy_rate=accuracy_rate)
                config_exp.win.flip()
                time.sleep(10)
            else:
                visuals.show_after_block_screen(block=block, accuracy_rate=accuracy_rate)
                config_exp.win.flip()
                time.sleep(10)


    def _experiment(self, block):
        """
        Runs the experiment for a given block.

        :param block: the block number
        :return: the accuracy rate after the block
        """

        # Load parameters from a pre-generated csv
        params = BlockParamsExperiment(block)

        # Generate a random trial order
        trial_order = list(range(config.n_trials))
        random.shuffle(trial_order)

        text = visual.TextStim(config_exp.win, text="Press 'space' to start when ready.", height=45)
        text.draw()
        config_exp.win.flip()
        keys = event.waitKeys(keyList=['space'])
        config_exp.win.flip()

        # Show images
        images = Images()
        img_order = images.create_random_order()

        response_processor = TrialResponseProcessor()

        # Timer to record the loading time of the first trial
        loading_timer = core.Clock()

        for i, trial in enumerate(trial_order):

            loading_timer.reset()

            images.reset()
            gc.collect()

            images.load(
                trial=trial,
                block=block,
                correct_answer=params.correct_answer
            )

            loading_time = loading_timer.getTime()

            images.show(
                trial=trial,
                params=params,
                img_order=img_order[i],
                loading_time=loading_time
            )

            response_processor.process(
                trial=trial,
                trial_i=i,
                correct_answer=params.correct_answer
            )

        # Output the accuracy rate and a csv file
        accuracy_rate = response_processor.accu / config.n_trials
        re_correct_answer = [params.correct_answer[i] for i in trial_order]
        output = pd.DataFrame({
            'trial': trial_order,
            'correct_answer': re_correct_answer,
            'response': response_processor.response_list
        })
        output.to_csv(f"data/block_{block}.csv", index=False)

        return accuracy_rate


    def _practice_trials(self):
        """
        Runs the practice trials.
        TODO: implement this method
        """

        raise NotImplementedError("This method is not implemented yet.")
        # Practice trials
        # text = visual.TextStim(win, text="Loading images ...", height=45)
        # text.draw()
        # win.flip()
        # accuracy_rate = experiment(n_trials=0, block=-1)
        # text = visual.TextStim(win, text=f"Practice ends. Good job! Your accuracy rate is {accuracy_rate*100}%.", height=35)
        # text.draw()
        # text = visual.TextStim(win, text="Press 'space' to start the formal experiment.", pos=(0, -200), height=35)
        # text.draw()
        # win.flip()
        # keys = event.waitKeys(keyList=['space'])

