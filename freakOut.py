import sysv_ipc
from queue import Queue
import random
import time
import ast
from multiprocessing import Process, Value, Array, Lock

key = 128
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

# Dans la message queue on a des tuples de 3 valeurs
# (destinataire, source, valeur de la carte)
# destinataire et source: 0=tout le monde, 1=le board, 2=les process players, 3=le client
# valeur de la carte de -10 à 10

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
        mq_BtoP.send(("2,1,"+str(first_card)).encode())
        message=0
        while(not is_finished(pile,lock)):
            #Message queue Board to Player
            while message:
                message_BtoP = str(message_BtoP).encode()
                mq_BtoP.send(message_BtoP)
                

            # Message Queue Player to Board
            message_PtoB=ast.literal_eval(mq_PtoB.receive())
            if(message_PtoB[0]==1):
                value_PtoB = message_PtoB[2]
                print("received:", value_PtoB[2])
                numJoueur = value_PtoB[1]
                if is_valid(self.card, value_PtoB[2]):
                    self.card = value_PtoB[2]
                    message = 1
                    message_BtoP = "2,1,"+int(value_PtoB[2])
                else:
                    # Si mauvais on renvoie le numéro de la carte + 200
                    message_BtoP = "2,1,"+int(200+value_PtoB[0])
                    mq_PtoB.empty()
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
        card_from_pile = pile[0]
        pile.pop(0)
    return card_from_pile


class Player(Process, ID):
    def __init__(self, Pile, lock):
        self.hand = []
        for i in range(6):
            self.hand.append(pioche(Pile, lock))

    def run_random(self):
        while(len(self.hand) != 0):
            msg_BtoP, t = mq.receive()
            msg_BtoP = msg_BtoP.decode()
            msg_BtoP = ast.literal_eval(msg_BtoP)
            # msg_BtoP est un tuple avec 3 valeurs :
            # (destinataire, source, valeur de la carte)
            if msg_BtoP[3] < 200:  # faire + 200 parce que -10+100 = 90 <100
                top_of_pile = msg_BtoP[3]

            for card in self.hand:
                if msg_BtoP[3] == card:
                    self.hand.remove(card)
                elif msg_BtoP[3] == (200 + card):
                    self.hand.append(pioche())

            print("received:", msg_BtoP[3])
            time_to_play = random.random()*10
            card_to_play = self.hand[int(random.random(len(self.hand)))]
            time.sleep(time_to_play)
            # Pourquoi on renvoie ici ?
            # message_PtoB = str(value_PtoB).encode()
            # mq_PtoB.send(message_PtoB)

if __name__ == "__main__":

    # Initialisation Pile
    # les numéros négatifs représentent les cartes bleus
    # et les numéros positifs les rouges
    pile = Array('i', range(-10, 10))
    lock = Lock()
    random.shuffle(pile)
    numJoueur = input("Entrez le nb de joueur :")
    theBoard = Board(1, 2, pile, lock)
