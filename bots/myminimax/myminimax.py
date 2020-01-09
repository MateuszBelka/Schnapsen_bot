#!/usr/bin/env python
"""


"""

from api import State, util
import random

class Bot:

    __max_depth = -1
    __randomize = True

    def __init__(self, randomize=True, depth=6):
        """
        :param randomize: Whether to select randomly from moves of equal value (or to select the first always)
        :param depth:
        """
        self.__randomize = randomize
        self.__max_depth = depth

    def get_move(self, state):
        # type: (State) -> tuple[int, int]

        val, move = self.value(state)

        return move

    def value(self, state, depth = 0):
        # type: (State, int) -> tuple[float, tuple[int, int]]
        """
        Return the value of this state and the associated move
        :param state:
        :param depth:
        :return: A tuple containing the value of this state, and the best move for the player currently to move
        """

        if state.finished():
            winner, points = state.winner()
            return (points, None) if winner == 1 else (-points, None)

        if depth == self.__max_depth:
            return heuristic(state)

        moves = state.moves()

        if self.__randomize:
            random.shuffle(moves)

        best_value = float('-inf') if maximizing(state) else float('inf')
        best_move = None

        for move in moves:

            next_state = state.next(move)

            # IMPLEMENT: Add a recursive function call so that 'value' will contain the
            # minimax value of 'next_state'
            value = self.value(next_state,depth + 1)[0]

            if maximizing(state):
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move

        return best_value, best_move

def maximizing(state):
    # type: (State) -> bool
    """
    Whether we're the maximizing player (1) or the minimizing player (2).

    :param state:
    :return:
    """
    return state.whose_turn() == 1

def heuristic(state):
    # type: (State) -> float
    """
    Estimate the value of this state: -1.0 is a certain win for player 2, 1.0 is a certain win for player 1

    :param state:
    :return: A heuristic evaluation for the given state (between -1.0 and 1.0)
    """


    if state.get_points(1) > 66:
        return 1.0, None
    elif state.get_points(2) > 66:
        return -1.0, None

    score_diff = state.get_points(1) - state.get_points(2)
    score_sum = state.get_points(1) + state.get_points(2)
    return score_diff / score_sum, None













""" Attempt at heuristic """

# ISSUE: How can I pass function as argument such that I can call this function later
#
#     Each has 33% influence on final eval
#     trump card or merriage played +/- 0.33
#     hand strength above average +/- 0.33
#     higher score than opponent +/- 0.33
#
#     heur_eval = 0.00
#     functions_to_eval = ["", "", "stronger_score"]
#     no_eval_funcs = len(func_to_eval)
#
#     for function in functions_to_eval:
#         heur_eval = update_heur_eval(state, function, heur_eval, no_eval_funcs)
#
#
#     return heur_eval, None
#
# def update_heur_eval(state, func, heur_eval, no_eval_funcs):
#
#     if func(state):
#         heur_eval += 1/no_eval_funcs
#     else:
#         heur_eval -= 1/no_eval_funcs
#
#     return heur_eval
#
# def played_trump_or_marriage(state):
#     # type: (State) -> boolean
#
#
# def hand_str_above_avg(state):
#     # type: (State) -> boolean
#     pass
#
# def stronger_score(state):
#     # type: (State) -> boolean
#     pass
