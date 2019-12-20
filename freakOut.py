# ce qu'il reste à faire : - message queue, protection des données


import sysv_ipc
from queue import Queue
import random
from multiprocessing import Process, Value, Array, Lock

# class Player(Process, ID):
#   def __init__(self, Pile):
key_BtoP = 128
key_PtoB = 129
mq_BtoP = sysv_ipc.MessageQueue(key_BtoP, sysv_ipc.IPC_CREAT)
mq_PtoB = sysv_ipc.MessageQueue(key_PtoB)


class Board:
    def __init__(self, numCard, numPlayers, lock):
        self.card = numCard
        processes = []
        for i in range(0, numPlayers):
            p = Player()
            processes.append(p)
            # il faut start les processes

    def run(self):
        message=0
        while(! is__finished()):
            #Message queue Board to Player
            while message:
                message_BtoP = str(value_BtoP).encode()
                mq_BtoP.send(message_BtoP)
                

            # Message Queue Player to Board
            while True:
                message_PtoB, t = mq_PtoB.receive()
                value_PtoB = message_PtoB.decode()
                value_PtoB = int(value_PtoB)
                if value_PtoB: #Value_PtoB sera un tableau avec 2 cases : la première est la valeur de la carte, la 2e, le numéro du joueur
                    print("received:", value_PtoB)
                    numJoueur=value_PtoB[1]
                    if is_valid(self.card,value_PtoB[0]):                        
                        self.card=value_PtoB[0]
                        message=1
                        value_BtoP=int(value_PtoB[0])
                    else:
                        value_BtoP=int(100+value_PtoB[0]) # Si mauvais on renvoie le numéro de la carte + 100
                    mq_PtoB.empty()

                else:
                    print("exiting.")
                    break
        mq_BtoP.remove()
        mq_PtoB.remove()
            
            

def is_finished(pile,lock):
    if (len(pile)==0):
        return True
    return False

def is_valid(board_card, player_card):
    if ((player_card == board_card + 1)
        or (player_card == board_card - 1)
            or (abs(player_card) == abs(board_card))):
        return True
    return False

def pioche(pile,lock):
    pile_content=pile[0]
    pile.pop(0)
    return pile_content






if __name__ == "__main__":
    # Creating Message Queue Board to Player


    # Initialisation Pile
    # les numéros négatifs représenteront les bleus tandis que les numéros négatifs seront les rouges
    pile = Array('i', range(-10, 10))
    lock=Lock()
    random.shuffle(pile)
    numJoueur = input("Entrez le nb de joueur :")
    theBoard = Board(1, 2, lock)
    
