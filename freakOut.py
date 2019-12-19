import sysv_ipc
from queue import Queue
import random
from multiprocessing import Process, Value, Array

# class Player(Process, ID):
#   def __init__(self, Pile):
key_BtoP = 128
key_PtoB = 129
mq_BtoP = sysv_ipc.MessageQueue(key_BtoP, sysv_ipc.IPC_CREAT)
mq_PtoB = sysv_ipc.MessageQueue(key_PtoB)


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
    #Creating Message Queue Board to Player
    value_BtoP = 1
    while value_BtoP:
        try:
            value_BtoP = int(input())
        except:
            print("Input error, try again!")
        message_BtoP = str(value_BtoP).encode()
        mq_BtoP.send(message_BtoP)
    mq_BtoP.remove()

    #Creating Message Queue Player to Board
    while True:
        message_PtoB, t = mq_PtoB.receive()
        value_PtoB = message_PtoB.decode()
        value_PtoB = int(value_PtoB)
        if value_PtoB:
            print("received:", value_PtoB)
        else:
            print("exiting.")
            break

    # Initialisation Pile
    # les numéros négatifs représenteront les bleus tandis que les numéros négatifs seront les rouges
    pile = Array('i', range(-10, 10))
    random.shuffle(pile)
    numJoueur = input("Entrez le nb de joueur :")
    theBoard = Board(1, 2)
    
