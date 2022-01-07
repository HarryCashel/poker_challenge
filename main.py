import sys


card_values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14
}


def format_hand(hand):
    """Takes a list of strings representing a hand and formats it to be used by score_hand function"""
    new_hand = []
    for card in hand:
        new_card = (card_values[card[0]], card[1])
        new_hand.append(new_card)
    return new_hand


def score_hand(hand) -> tuple:
    """Function that takes a string - a five-card poker hand and scores the hand.
    Returns a tuple of score, high card and a list of values in the hand.
    Returning the whole hand is only needed for a tie with pairs, however I felt it better to be consistent"""

    # get the numerical value of each card
    values = sorted([card[0] for card in hand], reverse=True)

    # get suit of each card
    suits = [card[1] for card in hand]

    # check for straight and flush
    straight = (values == list(range(values[0], values[-1] - 1, -1)))
    flush = all(suit == suits[0] for suit in suits)

    # straight flush check

    if straight and flush:
        if values[0] == 14:
            return 9, 14
        return 8, max(values), values

    # empty list to represent pair (two of a kind) or pair of pairs
    # and empty list to represent trips (three of a kind)

    pairs = []
    triples = []

    # iterate over the hand to check for 2, 3 and 4 of a kind
    for card in values:

        if values.count(card) == 4:
            return 7, max(values), values
        elif values.count(card) == 3:
            triples.append(card)
        elif values.count(card) == 2:
            pairs.append(card)

    # check hand for other possibilities

    if triples and pairs:
        return 6, max(triples), values
    if triples:
        return 3, max(triples), values
    if flush:
        return 5, max(values), values
    if straight:
        return 4, max(values), values
    if len(pairs) == 4:
        return 2, max(pairs[0], pairs[1]), values
    if len(pairs) == 2:
        return 1, max(pairs), values
    return 0, max(values), values


def find_next_largest(hand1, hand2, tie_value):
    """Function to find the next biggest value in the result of a tie"""
    hand1_max = (list(filter(lambda a: a != tie_value, hand1)))
    hand2_max = (list(filter(lambda a: a != tie_value, hand2)))

    if max(hand1_max) > max(hand2_max):
        return "player1"
    elif max(hand1_max) < max(hand2_max):
        return "player2"
    else:
        return find_next_largest(hand1_max, hand2_max, max(hand1_max))


def run():
    """Wraps the logic into a function"""
    player1_score = 0
    player2_score = 0

    for line in sys.stdin:
        hand = line.split()
        player1_hand = format_hand(hand[:5])
        player2_hand = format_hand(hand[5:])

        player1_result = score_hand(player1_hand)
        player2_result = score_hand(player2_hand)

        if player1_result[0] > player2_result[0]:
            player1_score += 1
        elif player1_result[0] < player2_result[0]:
            player2_score += 1
        elif player1_result[0] == player2_result[0]:
            if player1_result[1] > player2_result[1]:
                player1_score += 1
            elif player1_result[1] < player2_result[1]:
                player2_score += 1
            elif player1_result[1] == player2_result[1]:
                if find_next_largest(player1_result[2], player2_result[2], player1_result[1]) == "player1":
                    player1_score += 1
                elif find_next_largest(player1_result[2], player2_result[2], player1_result[1]) == "player2":
                    player2_score += 1

    sys.stdout.write(f"Player 1: {player1_score}\nPlayer 2: {player2_score}\n")


run()
