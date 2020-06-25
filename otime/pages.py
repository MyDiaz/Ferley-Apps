from ._builtin import Page, WaitPage
from .config import BLOCKS, VISUALIZE_CHOICES_AS_SLIDER


class BlockPage(Page):
    """Displays a `Block` to the player

    This page will automatically retrieve the current `Block` to be displayed
    to the player from the player's current block.
    """

    form_model = 'player'
    form_fields = ['block_answers']

    def is_displayed(self):
        """This page will only be displayed when there are blocks left"""
        return self.player.get_current_block() is not None

    def vars_for_template(self):
        step = self.player.get_current_step() + 1
        block_index = self.player.get_current_block_index() + 1
        current_block = self.player.get_current_block()
        num_blocks = len(BLOCKS)
        return {
            'step': step,
            'block_index': block_index,
            'num_blocks': num_blocks,
            'progress': round(step * 100 / num_blocks),
            'curr_block': current_block,
            'use_slider': VISUALIZE_CHOICES_AS_SLIDER,
            'num_choices': current_block.number_of_intermediate_choices + 2
        }

    def error_message(self, values):
        pass

    def before_next_page(self):
        self.player.goto_next_step()


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


def generate_page_sequence():
    return [BlockPage] * len(BLOCKS) + [ResultsWaitPage, Results]


page_sequence = generate_page_sequence()
