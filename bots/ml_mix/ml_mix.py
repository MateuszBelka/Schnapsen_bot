#!/usr/bin/env python
"""
A basic adaptive bot. This is part of the third worksheet.

"""

from api import State, util, Deck
import random, os
from itertools import chain

from sklearn.externals import joblib

# Path of the model we will use. If you make a model
# with a different name, point this line to its path.
DEFAULT_MODEL = '/home/matt/github/schnapsen_bot/bots/ml_mix/model.pkl'

class Bot:

    __randomize = True

    __model = None

    def __init__(self, randomize=True, model_file=DEFAULT_MODEL):

        print(model_file)
        self.__randomize = randomize

        # Load the model
        self.__model = joblib.load(model_file)

    def get_move(self, state):

        val, move = self.value(state)

        return move

    def value(self, state):
        """
        Return the value of this state and the associated move
        :param state:
        :return: val, move: the value of the state, and the best move.
        """

        best_value = float('-inf') if maximizing(state) else float('inf')
        best_move = None

        moves = state.moves()

        if self.__randomize:
            random.shuffle(moves)

        for move in moves:

            next_state = state.next(move)

            # IMPLEMENT: Add a function call so that 'value' will
            # contain the predicted value of 'next_state'
            # NOTE: This is different from the line in the minimax/alphabeta bot
            value = self.heuristic(next_state)

            if maximizing(state):
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move

        return best_value, best_move

    def heuristic(self, state):

        # Convert the state to a feature vector
        feature_vector = [features(state)]

        # These are the classes: ('won', 'lost')
        classes = list(self.__model.classes_)

        # Ask the model for a prediction
        # This returns a probability for each class
        prob = self.__model.predict_proba(feature_vector)[0]

        # Weigh the win/loss outcomes (-1 and 1) by their probabilities
        res = -1.0 * prob[classes.index('lost')] + 1.0 * prob[classes.index('won')]

        return res

def maximizing(state):
    """
    Whether we're the maximizing player (1) or the minimizing player (2).
    :param state:
    :return:
    """
    return state.whose_turn() == 1


def features(state):
    # type: (State) -> tuple[float, ...]
    """
    Extract features from this state. Remember that every feature vector returned should have the same length.

    :param state: A state to be converted to a feature vector
    :return: A tuple of floats: a feature vector representing this state.
    """

    feature_set = []

    # Add player 1's points to feature set
    p1_points = state.get_points(1)

    # Add player 2's points to feature set
    p2_points = state.get_points(2)

    # Add player 1's pending points to feature set
    p1_pending_points = state.get_pending_points(1)

    # Add plauer 2's pending points to feature set
    p2_pending_points = state.get_pending_points(2)

    # Get trump suit
    trump_suit = state.get_trump_suit()

    # Add phase to feature set
    phase = state.get_phase()

    # Add stock size to feature set
    stock_size = state.get_stock_size()

    # Add leader to feature set
    leader = state.leader()

    # Add whose turn it is to feature set
    whose_turn = state.whose_turn()

    # Add opponent's played card to feature set
    opponents_played_card = state.get_opponents_played_card()

    player_hand = state.hand()

    opponent_hand = state.hand_opponent()

    cards_in_hand = 5 # there are 5 cards in a hand at all times
    
    max_hand_points = cards_in_hand * 11 # ace is worth 11 points


    ################## You do not need to do anything below this line ########################

    perspective = state.get_perspective()

    # Perform one-hot encoding on the perspective.
    # Learn more about one-hot here: https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/
    perspective = [card if card != 'U'   else [1, 0, 0, 0, 0, 0] for card in perspective]
    perspective = [card if card != 'S'   else [0, 1, 0, 0, 0, 0] for card in perspective]
    perspective = [card if card != 'P1H' else [0, 0, 1, 0, 0, 0] for card in perspective]
    perspective = [card if card != 'P2H' else [0, 0, 0, 1, 0, 0] for card in perspective]
    perspective = [card if card != 'P1W' else [0, 0, 0, 0, 1, 0] for card in perspective]
    perspective = [card if card != 'P2W' else [0, 0, 0, 0, 0, 1] for card in perspective]

    # Append one-hot encoded perspective to feature_set
    feature_set += list(chain(*perspective))

    # Append normalized points to feature_set
    total_points = p1_points + p2_points
    feature_set.append(p1_points/total_points if total_points > 0 else 0.)
    feature_set.append(p2_points/total_points if total_points > 0 else 0.)

    # Append normalized pending points to feature_set
    total_pending_points = p1_pending_points + p2_pending_points
    feature_set.append(p1_pending_points/total_pending_points if total_pending_points > 0 else 0.)
    feature_set.append(p2_pending_points/total_pending_points if total_pending_points > 0 else 0.)

    # Append lowest card value in player hand && ace count && hand strength
    hand_points = 0.0
    ace_count = 0.0
    current_lowest = 0.0
    for card in player_hand:
        if Deck.get_rank(card) == "A":
            if current_lowest < 1.0:
                current_lowest = 1.0
            ace_count += 0.2
            hand_points += 11
        elif Deck.get_rank(card) == "10":
            if current_lowest < 0.75:
                current_lowest = 0.75
            hand_points += 10
        elif Deck.get_rank(card) == "K":
            if current_lowest < 0.5:
                current_lowest = 0.5
            hand_points += 4
        elif Deck.get_rank(card) == "Q":
            if current_lowest < 0.25:
                current_lowest = 0.25
            hand_points += 3
        elif Deck.get_rank(card) == "J":
            if current_lowest < 0.0:
                current_lowest = 0.0
            hand_points += 2

    feature_set.append(current_lowest)
    feature_set.append(ace_count)
    feature_set.append(hand_points/max_hand_points)

    # Append lowest card value in opponent's hand && ace count && opponent hand strength
    hand_points_opp = 0.0
    ace_count_opp = 0.0
    current_lowest_opp = 0.0
    if (phase == 2):
        for card in opponent_hand:
            if Deck.get_rank(card) == "A":
                if current_lowest_opp < 1.0:
                    current_lowest_opp = 1.0
                ace_count_opp += 0.2
                hand_points_opp += 11
            elif Deck.get_rank(card) == "10":
                if current_lowest_opp < 0.75:
                    current_lowest_opp = 0.75
                hand_points_opp += 10
            elif Deck.get_rank(card) == "K":
                if current_lowest_opp < 0.5:
                    current_lowest_opp = 0.5
                hand_points_opp += 4
            elif Deck.get_rank(card) == "Q":
                if current_lowest_opp < 0.25:
                    current_lowest_opp = 0.25
                hand_points_opp += 3
            elif Deck.get_rank(card) == "J":
                if current_lowest_opp < 0.0:
                    current_lowest_opp = 0.0
                hand_points_opp += 2
    feature_set.append(current_lowest_opp)
    feature_set.append(ace_count_opp)
    feature_set.append(hand_points_opp/max_hand_points)

    # Append how many cards of opponent's suit do you have
    same_suit_cards = 0.0

    for card in player_hand:
        if opponents_played_card is not None:
            if Deck.get_suit(card) == Deck.get_suit(opponents_played_card):
                same_suit_cards += 1
    feature_set.append(same_suit_cards/cards_in_hand)

    # Append one-hot encoded points difference
    p_diff = p1_points - p2_points
    feature_set += [p_diff, 0] if p_diff > 0 else [0, -1 * p_diff]

    # Append one-hot encoded pending points difference
    pp_diff = p1_pending_points - p2_pending_points
    feature_set += [pp_diff, 0] if pp_diff > 0 else [0, -1 * pp_diff]

    # Return feature set
    return feature_set
