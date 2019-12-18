import random
from queue import Queue


class Card:

    def __init__(self, num, color):

        self.num = num
        self.color = color

    def __str__(self):
        return "La carte est:" + str(self.num) + " " + self.color


class Player(Process):
    def __init__(self, Pile):
        for i in range(5):


class Board:
    def __init__(self, card, numPlayers):
        self.card = card
        processes = []
        for in range(0, numPlayers):
            p = Player()
            processes.append(p)


"""
class Pile:
    def __init__(self):
        self.cardList = []
        for i in range(2):
            for j in range(1, 11):
                if i == 0:
                    self.cardList.append(Card(j, "blue"))
                else:
                    self.cardList.append(Card(j, "red"))

        random.shuffle(self.cardList)
"""

if __name__ == "__main__":

    # Initialisation Pile
    cardPile = []
    for i in range(2):
        for j in range(1, 11):
            if i == 0:
                cardPile.append(Card(j, "blue"))
            else:
                cardPile.append(Card(j, "red"))
    random.shuffle(cardPile)
