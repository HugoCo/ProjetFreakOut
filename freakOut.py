import sysv_ipc
from queue import Queue
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
    def __init__(self, numCard, numPlayers):
        self.card = numCard
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

def pioche(pile):
    pile_content=pile[0]
    pile.pop(0)
    return pile_content





if __name__ == "__main__":
    # Initialisation Pile
    # les numéros négatifs représenteront les bleus tandis que les numéros négatifs seront les rouges
    pile = Array('i', range(-10, 10))
    random.shuffle(pile)
    numJoueur = input("Entrez le nb de joueur :")
    theBoard = Board(1, 2)
    
