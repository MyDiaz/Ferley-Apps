from otree.api import (
    BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    models
)

author = 'Michael Rose <michael_rose@gmx.de>'

doc = """
otdm provides an easy way of creating experiments to measure the temporal discounting of money
using the Direct Method (DM) [Attema et al., 2016]
"""


class Constants(BaseConstants):
    name_in_url = 'otdm'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    current_step = models.IntegerField(initial=1)
    """Current step the player is in
    
    Equals the elicitation round, i.e. ranges from 1 (for c12) to 5 (c78).
    """

    # IMPORTANT: DO NOT CHANGE THE VARIABLE NAMES FOR THE c values!

    c12 = models.IntegerField(initial=-1)
    """Represents the measured value of c_(1/2)"""

    c14 = models.IntegerField(initial=-1)
    """Represents the measured value of c_(1/4)"""

    c34 = models.IntegerField(initial=-1)
    """Represents the measured value of c_(3/4)"""

    c18 = models.IntegerField(initial=-1)
    """Represents the measured value of c_(1/8)"""

    c78 = models.IntegerField(initial=-1)
    """Represents the measured value of c_(7/8)"""

    def goto_next_step(self) -> None:
        """Advances the player to the next step

        Should be called after each `ChoiceListPage`
        """
        self.current_step = self.current_step + 1

    def cancel_game(self) -> None:
        """Sets the indicator that an invalid choice occurred"""
        self.current_step = -1

    def get_current_step(self) -> int:
        """Get the current step the player is in
        :return: current step (1-based)
        """
        return self.current_step
