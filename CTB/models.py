from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'CTB'
    players_per_group = None
    tasks = ['1', '2']
    num_rounds = len(tasks)


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                round_numbers = list(range(1, Constants.num_rounds+1))
                random.shuffle(round_numbers)
                p.participant.vars['task_rounds'] = dict(zip(Constants.tasks, round_numbers))



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    rta_1 = models.StringField()
    rta_2 = models.StringField()

