import random
from multiprocessing import Process, Value, Array
from queue import Queue


"""class Card:

    def __init__(self, numCol):

        self.numCol=numCol

    def __str__(self):
        return "La carte est:" + str(self.num) + " " + self.color
"""

#class Player(Process, ID):
 #   def __init__(self, Pile):


class Board:
    def __init__(self, card, numPlayers):
        self.card = card
        processes = []
        for i in range(0, numPlayers):
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
    pile=Array('i',range(20))
    for i in range (-10,11): #les numéros négatifs représenteront les bleus tandis que les numéros négatifs seront les rouges    
        if(i!=0):
            pile[i]=i
    
    """for i in range(2):
        for j in range(1, 11):
            if i == 0:
                cardPile.append(Card(j, "blue"))
            else:
                cardPile.append(Card(j, "red"))
    """
    random.shuffle(pile)
    print(pile)
