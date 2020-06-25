from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


# Expose variables for all templates. Attempted to create this as prettier function, but was not able.
def vars_for_all_templates(self):
    return {
        'lottery_a_hi': c(self.session.vars['payoffs']['A'][0]),
        'lottery_a_lo': c(self.session.vars['payoffs']['A'][1]),
        'lottery_b_hi': c(self.session.vars['payoffs']['B'][0]),
        'lottery_b_lo': c(self.session.vars['payoffs']['B'][1]),
        'num_choices': Constants.num_choices
    }


# Class for the IntroPage. Inherits attributes from Page Class
class IntroPage(Page):
    # Get forms to be displayed on IntroPage
    form_model = 'player'
    form_fields = ['name', 'risk']


# Class for the DecisionPage. Inherits attributes from Page Class
class DecisionPage(Page):
    form_model = 'player'

    # Unzip the list of choices, in order to create form fields corresponding to the number of choices
    def get_form_fields(self):
        form_fields = [list(t) for t in zip(*self.session.vars['choices'])][1]
        print(form_fields)
        return form_fields

    # Expose variables that will only be available on this page.
    def vars_for_template(self):
        return {
            "choices": self.session.vars['choices'],
        }

    # Triggers the function that set draws the payoff of the user before the user is taken to the result page. This
    # should be changed if we were to make a game with several rounds.
    def before_next_page(self):
        self.player.set_payoffs()


# Class for the ResultsPage. Inherits attributes from Page Class
class ResultsPage(Page):

    # Expose variables that will only be available on this page.
    def vars_for_template(self):
        return {
            "index_to_pay": self.participant.vars['index_to_pay'],
        }


# The sequence the app will order the pages.
page_sequence = [IntroPage, DecisionPage, ResultsPage]
