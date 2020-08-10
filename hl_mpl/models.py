from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

from django.conf import settings

# Moved index function to separate file to keep this file cleaner
from . import utils
#from hl_mpl.config import *

import random
import numpy as np

author = 'Olaf Ghanizadeh'

doc = """
A crude and simple implementation of the Holt/Laury(2002) lottery.
"""


class Subsession(BaseSubsession):
    """Creating the lottery subsessions"""

    def creating_session(self):
        """Method to initiate a session"""
        # Set Constant num.choices to n for easier reuse
        n = self.session.config['num_choices']
        # Multiplier to test for incentive effects
        multiplier = self.session.config['multiplier']

        # Multiply payoffs by session.config.multiplier
        payoffs = {key: [i * multiplier for i in value] for (key, value) in BaseConstants.payoffs.items()}
        # Store in session variables
        self.session.vars['payoffs'] = payoffs

        index = utils.create_index(n)
        self.session.vars['index'] = index

        probs = [
            i / n
            for i in index
        ]

        inverse_p = [1 - p for p in probs]

        self.session.vars['probs'] = probs
        self.session.vars['inverse_probs'] = inverse_p

        formatted_p = ["{0:.0f}".format(p * 100) + "%" for p in probs]
        formatted_inverse_p = ["{0:.0f}".format(p * 100) + "%" for p in inverse_p]

        form_fields = ['choice_' + str(k) for k in index]

        choices = list(zip(index, form_fields, formatted_p, formatted_inverse_p))
        self.session.vars['choices'] = choices

        # Create lottery for each player
        for p in self.get_players():
            # Randomly pick which choice to pay at the end of lottery, and assign to a participant variable
            p.participant.vars['index_to_pay'] = random.randrange(0, len(index))

            # NEEDS COMMENT
            p.participant.vars['choice_to_pay'] = 'choice_' + str(p.participant.vars['index_to_pay'])


# Unused class in this project
class Group(BaseGroup):
    pass


class Player(BasePlayer):
    """The oTree class that generates the info PER PLAYER"""

    n = settings.SESSION_CONFIGS[0].get('num_choices')

    # Name Field
    name = models.StringField(
        label="What is your name? Please enter your first name and last name."
    )
    # Select field where user fills out their perceived attitude towards risks
    risk = models.IntegerField(
        choices=[
            [1, 'I prefer to avoid risks'],
            [2, 'I am neutral towards risks'],
            [3, 'I like taking risks if I can gain from it'],
        ],
        label="How is your attitude towards risk?",
    )

    # Generates the fields for the form fields. Necessary to call locals() to access correct scope. This should be
    # put in a function to improve code quality.
    for j in range(1, n + 1):
        locals()['choice_' + str(j)] = models.IntegerField(
            choices=[0, 1],
            widget=widgets.RadioSelectHorizontal
        )
    # Delete intermediate variables
    del j
    del n

    # Initiate fields to be populated by app
    choice_to_pay = models.StringField()
    option_chosen = models.IntegerField()
    option_chosen_letter = models.StringField()

    # Function to set payoffs for each player
    def set_payoffs(self):
        """When 'set_payoffs' is called, the player's payoff is set"""

        # Call the payoff dictionary, which contains updated values with multiplier
        payoffs = self.session.vars['payoffs']
        # Call the number of choices to create the probability distribution to draw from
        n = self.session.config['num_choices']

        # get the choice that was randomly drawn in 'creating_session'
        self.choice_to_pay = self.participant.vars['choice_to_pay']

        # Check which option the user selected in the Choice that was selected by app
        self.option_chosen = getattr(self, self.choice_to_pay)

        # Get the index of the Choice that was drawn to create the corresponding probability
        index = self.participant.vars['index_to_pay']

        # Create lists of probability and inverse probability, this could be improved with better code
        i = self.session.vars['probs'][index - 1]
        j = self.session.vars['inverse_probs'][index - 1]

        # store in list for numpy to draw from
        p = [i, j]

        # delete intermediate variables
        del i
        del j

        # Assign the outcomes to lists
        a = [c(payoffs['A'][0]), c(payoffs['A'][1])]
        b = [c(payoffs['B'][0]), c(payoffs['B'][1])]

        # If the player chose 'A'
        if self.option_chosen == 0:
            # Numpy function that picks an element in a list according to probability distribution, first argument is
            # the list to pick from, second argument is the number of times to run the draw, third argument is list
            # of probabilities
            drawn = np.random.choice(a, 1, p)
            # Run the draw once, numpy creates a list with 1 element, and we access it by getting the 0-index.
            self.payoff = drawn[0]
            self.option_chosen_letter = 'A'

        # If the player chose 'B'
        elif self.option_chosen == 1:
            drawn = np.random.choice(b, 1, p)
            self.payoff = drawn[0]
            self.option_chosen_letter = 'B'
