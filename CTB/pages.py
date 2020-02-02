import random

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Bienvenido(Page):
    pass

class primeraPregunta(Page):
    form_model = 'player'
    form_fields = ['rta_1']


class segundaPregunta(Page):
    form_model = 'player'
    form_fields = ['rta_2']


class Gracias(Page):
    pass


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

page_sequence = [Bienvenido]

preguntas = [
    primeraPregunta,
    segundaPregunta
]

random.shuffle(preguntas)

for p in preguntas:
    page_sequence.append(p)

page_sequence.append(Gracias)
