from enum import Enum
from typing import Callable, List

from .config import NUM_WEEKS
from .models import Player


class ChoiceStep(Enum):
    """
    Represents all the information required to produce a list of choices
    to elicit a certain c value.

    All enumeration values have four properties:
    - the round number in which the c value is elicited
    - the field name of the `player`
    - a function to get the starting week for the choice list
    - a function to get the ending week for the choice list
    """
    C_12 = 1, \
           'c12', \
           lambda p: 1, \
           lambda p: NUM_WEEKS
    C_14 = 2, \
           'c14', \
           lambda p: 1, \
           lambda p: p.c12
    C_34 = 3, \
           'c34', \
           lambda p: p.c12, \
           lambda p: NUM_WEEKS
    C_18 = 4, \
           'c18', \
           lambda p: 1, \
           lambda p: p.c14
    C_78 = 5, \
           'c78', \
           lambda p: p.c34, \
           lambda p: NUM_WEEKS

    def __new__(cls, keycode: int,
                field_name: str,
                range_start_extractor: Callable[[Player], int],
                range_end_extractor: Callable[[Player], int]):
        obj = object.__new__(cls)
        obj._value_ = keycode
        obj._player_field = field_name
        obj._range_start_extractor = range_start_extractor
        obj._range_end_extractor = range_end_extractor
        return obj

    def get_field(self) -> str:
        return self._player_field

    def get_range_start(self, player: Player) -> int:
        return self._range_start_extractor(player)

    def get_range_end(self, player: Player) -> int:
        return self._range_end_extractor(player)


class ChoiceManager:
    """
    Helper class to facilitate working with calculating week ranges
    for the current step a player is in.
    """

    def __init__(self, player: Player):
        self._player = player
        self._step = ChoiceStep(player.get_current_step())

    def get_step(self) -> ChoiceStep:
        return self._step

    def get_week_range(self) -> List[int]:
        start = self._step.get_range_start(self._player)
        end = self._step.get_range_end(self._player)
        return [i for i in range(start, end + 1)]
