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
    num_rounds = 1
    semanas = 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    rta_1 = models.StringField()
    rta_2 = models.StringField()
    rta_3 = models.StringField()
    rta_4 = models.StringField()
    rta_5 = models.StringField()
    rta_6 = models.StringField()
    rta_7 = models.StringField()
    rta_8 = models.StringField()
    rta_9 = models.StringField()
    rta_10 = models.StringField()
    rta_11 = models.StringField()
    rta_12 = models.StringField()
    rta_13 = models.StringField()
    rta_14 = models.StringField()
    rta_15 = models.StringField()
    rta_16 = models.StringField()
    rta_17 = models.StringField()
    rta_18 = models.StringField()
    rta_19 = models.StringField()
    rta_20 = models.StringField()
    rta_21 = models.StringField()
    rta_22 = models.StringField()
    rta_23 = models.StringField()
    rta_24 = models.StringField()


