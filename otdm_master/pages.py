from math import floor

from typing import List

from ._builtin import Page, WaitPage
from .choices import ChoiceManager
from .config import GAIN_PER_WEEK, NUM_WEEKS


class ChoiceListPage(Page):
    """
    Displays a list of choices to the player to elicitate a certain c value.
    """

    form_model = 'player'
    #form_fields = ['c12','c14','c34','c18','c78']

    def is_displayed(self):
        return self.player.get_current_step() != -1

    def get_form_fields(self) -> List[str]:
        manager = ChoiceManager(self.player)
        return [manager.get_step().get_field()]

    def vars_for_template(self):
        manager = ChoiceManager(self.player)

        week_range = manager.get_week_range()
        week_start = week_range[0]
        week_end = week_range[-1]

        option_a_weeks = week_range[:]
        option_a_weeks.insert(0, week_start)
        option_a_gain_count = [i - week_start + 1 for i in option_a_weeks]

        option_b_weeks = week_range[:]
        option_b_weeks.append(week_end)
        option_b_gain_count = [week_end - i + 1 for i in option_b_weeks]

        week_gain = zip(option_a_weeks, option_a_gain_count,
                        option_b_weeks, option_b_gain_count)

        return {
            'gain': GAIN_PER_WEEK,
            'progress': self.player.get_current_step() / 5 * 100,
            'var_name': manager.get_step().get_field(),

            'week_start': week_start,
            'week_end': week_end,

            'week_gain': week_gain
        }

    def before_next_page(self):
        manager = ChoiceManager(self.player)

        # we fix the computed value as the client gives us just
        # the index of the selected option - which is not directly a week
        # the index is 1-based so we have subtract 1

        field_name = manager.get_step().get_field()
        index = getattr(self.player, field_name) - 1
        week_range = manager.get_week_range()

        # the number of selectable options is len(week_range) + 1
        if index == 0 or index == len(week_range):
            # selection is invalid - we cannot handle this case further
            # as it would lead to invalid ranges in the future
            setattr(self.player, field_name, index)
            self.player.cancel_game()
        else:
            switch_lower_bound = week_range[index]
            if switch_lower_bound > 1:
                if switch_lower_bound < floor(NUM_WEEKS / 2.0):
                    # values that are below half of the time frame get the "upper bound"
                    switch_lower_bound = switch_lower_bound + 1
                else:
                    # values that are above half of the time frame get the "lower bound"
                    pass
            setattr(self.player, field_name, switch_lower_bound)

            self.player.goto_next_step()


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    ChoiceListPage,  # elicit c12
    ChoiceListPage,  # elicit c14
    ChoiceListPage,  # elicit c34
    ChoiceListPage,  # elicit c18
    ChoiceListPage,  # elicit c78
    ResultsWaitPage,
    Results
]
