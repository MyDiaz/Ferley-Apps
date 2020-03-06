import random

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Bienvenido(Page):
    pass

class Pregunta_1(Page):
    form_model = 'player'
    form_fields = ['rta_1']

class Pregunta_2(Page):
    form_model = 'player'
    form_fields = ['rta_2']

class Pregunta_3(Page):
    form_model = 'player'
    form_fields = ['rta_3']

class Pregunta_4(Page):
    form_model = 'player'
    form_fields = ['rta_4']

class Pregunta_5(Page):
    form_model = 'player'
    form_fields = ['rta_5']

class Pregunta_6(Page):
    form_model = 'player'
    form_fields = ['rta_6']

class Pregunta_7(Page):
    form_model = 'player'
    form_fields = ['rta_7']

class Pregunta_8(Page):
    form_model = 'player'
    form_fields = ['rta_8']

class Pregunta_9(Page):
    form_model = 'player'
    form_fields = ['rta_9']

class Pregunta_10(Page):
    form_model = 'player'
    form_fields = ['rta_10']

class Pregunta_11(Page):
    form_model = 'player'
    form_fields = ['rta_11']

class Pregunta_12(Page):
    form_model = 'player'
    form_fields = ['rta_12']

class Pregunta_13(Page):
    form_model = 'player'
    form_fields = ['rta_13']

class Pregunta_14(Page):
    form_model = 'player'
    form_fields = ['rta_14']

class Pregunta_15(Page):
    form_model = 'player'
    form_fields = ['rta_15']

class Pregunta_16(Page):
    form_model = 'player'
    form_fields = ['rta_16']

class Pregunta_17(Page):
    form_model = 'player'
    form_fields = ['rta_17']

class Pregunta_18(Page):
    form_model = 'player'
    form_fields = ['rta_18']

class Pregunta_19(Page):
    form_model = 'player'
    form_fields = ['rta_19']

class Pregunta_20(Page):
    form_model = 'player'
    form_fields = ['rta_20']

class Pregunta_21(Page):
    form_model = 'player'
    form_fields = ['rta_21']

class Pregunta_22(Page):
    form_model = 'player'
    form_fields = ['rta_22']

class Pregunta_23(Page):
    form_model = 'player'
    form_fields = ['rta_23']

class Pregunta_24(Page):
    form_model = 'player'
    form_fields = ['rta_24']

class Gracias(Page):
    pass


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

page_sequence = [Bienvenido]

preguntas = [
    Pregunta_1,
    Pregunta_2,
    Pregunta_3,
    Pregunta_4,
    Pregunta_5,
    Pregunta_6,
    Pregunta_7,
    Pregunta_8,
    Pregunta_9,
    Pregunta_10,
    Pregunta_11,
    Pregunta_12,
    Pregunta_13,
    Pregunta_14,
    Pregunta_15,
    Pregunta_16,
    Pregunta_17,
    Pregunta_18,
    Pregunta_19,
    Pregunta_20,
    Pregunta_21,
    Pregunta_22,
    Pregunta_23,
    Pregunta_24
]

random.shuffle(preguntas)

for p in preguntas:
    page_sequence.append(p)

page_sequence.append(Gracias)