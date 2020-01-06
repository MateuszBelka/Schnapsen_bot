"""
MyBot -- chooses suit to follow and plays highest value card of said suit.
"""

# Import the API objects
from api import State, Deck, util
import random


class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # type: (State) -> tuple[int, int]


        # var declarations
        moves = state.moves() # type: list(tuple[int, int])
        opponent_card = state.get_opponents_played_card() # type: int or None
        trump_suit = state.get_trump_suit() # type: string or None
        best_move_of_trump_suit = self.get_best_move_of_trump_suit(moves, trump_suit) # type: tuple[int, int]

        if best_move_of_trump_suit != (None, None):
            return best_move_of_trump_suit
        if opponent_card == None:
            return self.get_highest_move_from_moves(moves)
        else:
            moves_of_opponent_suit = self.get_moves_of_opponent_suit(moves, opponent_card)
            if moves_of_opponent_suit != []:
                return self.get_highest_move_from_moves(moves_of_opponent_suit)
            else:
                return self.get_highest_move_from_moves(moves)

    def get_best_move_of_trump_suit(self, moves, trump_suit):
        # type: list(tuple[int, int]), string -> tuple[int, int]

        if trump_suit is None:
            return (None, None)

        local_trump_moves = []
        for move in moves:
            if move[0] is not None and Deck.get_suit(move[0]) == trump_suit:
                local_trump_moves.append(move)

        return self.get_highest_move_from_moves(local_trump_moves)

    def get_highest_move_from_moves(self, moves):
        # type: list(tuple[int, int]) -> tuple[int, int]
        if moves == []:
            return (None, None)

        output = moves[0]
        for move in moves:
            if util.get_rank(move[0]) < util.get_rank(output[0]):
                output = move
        return output

    def get_moves_of_opponent_suit(self, moves, opponent_card):
        # type: list(tuple[int, int]), int -> list(tuple[int, int])
        output = []
        for move in moves:
            if util.get_suit(opponent_card) == util.get_suit(move[0]):
                output.append(move)
        return output
