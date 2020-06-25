import json
import random
from typing import Optional, List

from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer
)

from .block import Block
from .config import BLOCKS, RANDOMIZE_BLOCKS

author = 'Michael Rose <michael_rose@gmx.de>'

doc = """
otime provides an easy way of creating time-preference based experiments by configuration
"""


class Constants(BaseConstants):
    name_in_url = 'otime'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    block_order = models.StringField(initial="")

    def creating_session(self) -> None:
        """Initializes the session and creates the order in which the Blocks should be run through
        """
        block_order = [i for i in range(len(BLOCKS))]
        if RANDOMIZE_BLOCKS:
            random.shuffle(block_order)

        self.block_order = json.dumps(block_order)

    def get_block_order(self) -> List[int]:
        """Get the order in which blocks should be run through

        The elements of the list represent the 0-based index in the `config.BLOCKS` list.

        :return: List of Block indexes
        """
        return json.loads(self.block_order)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    current_step = models.IntegerField(initial=0)
    """Current step the user is in
    """

    block_answers = models.StringField(initial="")
    """Serialized JSON array representing the players answers
    
    The JSON array is two dimensional - the elements of the array represent
    the selected choices per block where the element index matches the index
    of the block in config.BLOCKS (0-based). The elements itself are also arrays where
    each number inside the element represents the index of the choice the
    player made in the respective question - starting from 1.
    """

    def goto_next_step(self) -> None:
        """Advances the player to the next step
        """
        self.current_step = self.current_step + 1

    def get_current_step(self) -> int:
        """The player's current step

        :return: Current step
        """
        return self.current_step

    def get_current_block_index(self) -> int:
        """Get the index of the block to be currently displayed

        This function returns the 0-based index of the block in `config.BLOCKS`
        to be displayed to the player taking into account the potentially
        randomized order.
        This method will return `-1` if `self.current_step` exceed the number
        of configured blocks.

        :return: Index of block to display or `-1`
        """
        if self.current_step < len(BLOCKS):
            block_order = self.subsession.get_block_order()
            return block_order[self.current_step]
        else:
            return -1

    def get_current_block(self) -> Optional[Block]:
        """Get the current Block to display

        This function returns `None` if there is nothing left to display.

        :return: Block to display or `None`
        """
        block_index = self.get_current_block_index()
        if 0 <= block_index < len(BLOCKS):
            return BLOCKS[block_index]
        else:
            return None
