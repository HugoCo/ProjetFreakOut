import sysv_ipc
from queue import Queue
import random
import time
from multiprocessing import Process, Value, Array, Lock

key_BtoP = 128
key_PtoB = 129
mq_BtoP = sysv_ipc.MessageQueue(key_BtoP, sysv_ipc.IPC_CREAT)
mq_PtoB = sysv_ipc.MessageQueue(key_PtoB)


class Player(Process, ID):
    def __init__(self, Pile,lock):
        self.hand=[]
        for i in range (6):
            self.hand.append(pioche(Pile,lock))

    def run_random(self):
        message=0
        while(len(self.hand) != 0):
            message_BtoP, t = mq_BtoP.receive()
            value_BtoP = message_BtoP.decode()
            value_BtoP = int(value_BtoP)
            if value_BtoP: #Value_PtoB sera un tableau avec 2 cases : la première est la valeur de la carte, la 2e, le numéro du joueur
                if value_BtoP<100:
                    card_on_top_of_pile=value_BtoP

                for card in self.hand:
                        if value_BtoP == card:
                            self.hand.remove(card)
                        elif value_BtoP == (100 + card):
                            self.hand.append(pioche())
                            
                print("received:", value_PtoB)
                time_to_play=random.random()*10
                card_to_play=self.hand[int(random.random(len(self.hand)))]
                time.sleep(time_to_play)
                message_PtoB = str(value_PtoB).encode()
                mq_PtoB.send(message_PtoB)

            else:
                print("exiting.")
                break

class Board:
    def __init__(self, numCard, numPlayers, pile, lock):
        self.card = numCard
        processes = []
        for i in range(0, numPlayers):
            p = Player(Pile, )
            processes.append(p)
            p.start()

        start = time.time()
        # il faut start les processes

    def run(self,pile,lock):
        first_card=pioche(pile,lock)
        mq_BtoP.send(str(first_card).encode())
        message=0
        while(not is_finished(pile,lock)):
            #Message queue Board to Player
            while message:
                message_BtoP = str(value_BtoP).encode()
                mq_BtoP.send(message_BtoP)
                

                # Message Queue Player to Board
                while True:
                    message_PtoB, t = mq_PtoB.receive()
                    value_PtoB = message_PtoB.decode()
                    value_PtoB = int(value_PtoB)
                    if value_PtoB:
                        # Value_PtoB sera un tableau avec 2 cases :
                        # la première est la valeur de la carte, la 2e,
                        # le numéro du joueur
                        print("received:", value_PtoB)
                        numJoueur = value_PtoB[1]
                        if is_valid(self.card, value_PtoB[0]):
                            self.card = value_PtoB[0]
                            message = 1
                            value_BtoP = int(value_PtoB[0])
                        else:
                            # Si mauvais on renvoie le numéro de la carte + 100
                            value_BtoP = int(100+value_PtoB[0])
                        mq_PtoB.empty()

<<<<<<< HEAD
=======
                else:
                    print("exiting.")
                    break
        mq_BtoP.remove()
        mq_PtoB.remove()


def is_finished(pile, lock):
    with lock:
        if (len(pile) == 0):
            return True
        return False


def is_valid(board_card, player_card):
    if ((player_card == board_card + 1)
        or (player_card == board_card - 1)
            or (abs(player_card) == abs(board_card))):
        return True
    return False


def pioche(pile, lock):
    with lock:
        pile_content = pile[0]
        pile.pop(0)
    return pile_content


if __name__ == "__main__":
    # Creating Message Queue Board to Player

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
    # les numéros négatifs représenteront les bleus tandis que les numéros
    # négatifs seront les rouges
    pile = Array('i', range(-10, 10))
    lock = Lock()
    random.shuffle(pile)
    numJoueur = input("Entrez le nb de joueur :")
    theBoard = Board(1, 2, pile, lock)
