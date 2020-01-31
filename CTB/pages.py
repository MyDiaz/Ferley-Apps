from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Bienvenido(Page):
    pass

class primeraPregunta(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == self.participant.vars['task_rounds']['1']


class segundaPregunta(Page):
    form_model = 'player'
    form_fields = ['rta_2']

    def is_displayed(self):
        return self.round_number == self.participant.vars['task_rounds']['2']

class Gracias(Page):
    pass

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


page_sequence = [
    Bienvenido,
    primeraPregunta,
    segundaPregunta,
    Gracias
]
