"""
MyBot --
"""

# Import the API objects
from api import State
import random


class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # type: (State) -> tuple[int, int]

        
        # All legal moves
        moves = state.moves()


        # Return a random choice
        return random.choice(moves)
