import random
from multiprocessing import Process, Value, Array


"""class Card:

    def __init__(self, numCol):

        self.numCol=numCol

    def __str__(self):
        return "La carte est:" + str(self.num) + " " + self.color
"""

# class Player(Process, ID):
#   def __init__(self, Pile):


class Board:
    def __init__(self, card, numPlayers):
        self.card = card
        processes = []
        for i in range(0, numPlayers):
            p = Player()
            processes.append(p)


def is_valid(board_card, player_card):
    if ((player_card == board_card + 1)
        or (player_card == board_card - 1)
            or (abs(player_card) == abs(board_card))):
        return True
    return False


if __name__ == "__main__":

    # Initialisation Pile
    pile = Array('i', range(-11, 11))
    print(pile[:])
    for i in range(-10, 11):  # les numéros négatifs représenteront les bleus tandis que les numéros négatifs seront les rouges
        if(i != 0):
            pile[i] = i
    random.shuffle(pile)
    print(pile)
