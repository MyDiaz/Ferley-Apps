from otree.api import Currency as c
from otree.constants import BaseConstants


class Constants(BaseConstants):
    name_in_url = 'risk_lottery'
    players_per_group = None
    num_rounds = 1
    num_choices = 8
    # Defining Lottery Payoffs in a dict
    payoffs = {"A": [20, 16], "B": [38, 1]}
