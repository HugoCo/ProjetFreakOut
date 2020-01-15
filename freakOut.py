import sysv_ipc
import random
import time
import ast
from multiprocessing import Process, Value, Array, Lock

key = 128
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)


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


class Player(Process):
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
            if msg_BtoP[3] < 100:  # faire + 200 parce que -10+100 = 90 <100
                top_of_pile = msg_BtoP[3]

            for card in self.hand:
                if msg_BtoP[3] == card:
                    self.hand.remove(card)
                elif msg_BtoP[3] == (100 + card):
                    self.hand.append(pioche())

            print("received:", msg_BtoP[3])
            time_to_play = random.random()*10
            card_to_play = self.hand[int(random.random(len(self.hand)))]
            time.sleep(time_to_play)
            # Pourquoi on renvoie ici ?
            # message_PtoB = str(value_PtoB).encode()
            # mq_PtoB.send(message_PtoB)


class Board:
    def __init__(self, numCard, numPlayers, pile, lock):
        self.card = numCard
        processes = []
        for i in range(0, numPlayers):
            p = Player(pile, lock, "ID")
            processes.append(p)
            p.start()

        # il faut start les processes

    def run(self, pile, lock):
        first_card = pioche(pile, lock)
        mq.send(str(first_card).encode())
        message = 0
        timer = 0
        start = time.time()
        end = time.time()
        while not is_finished():
            while timer < 10:  # mettre le client dans la partie process?
                timer = end - start
                """
                # Message queue Board to Player
                while message:
                    message_BtoP = str(value_BtoP).encode()
                    mq_BtoP.send(message_BtoP)
                """
                msg_PtoB, t = mq.receive()
                msg_PtoB = msg_PtoB.decode()
                msg_PtoB = ast.literal_eval(msg_PtoB)

                # msg_PtoB est un tuple avec 3 valeurs :
                # (destinataire, source, valeur de la carte)
                if msg_PtoB[0] == "board":
                    print("received:", msg_PtoB)
                    if is_valid(self.card, msg_PtoB[2]):
                        self.card = msg_PtoB[2]
                        received_card = int(msg_PtoB[2])
                    else:
                        # Si mauvais on renvoie le numéro de la carte + 100
                        received_card = int(100+msg_PtoB[2])
                    mq.remove()
                    msg_BtoP = msg_PtoB[1] + ", " + msg_PtoB[0]
                    + ", " + str(received_card)
                    mq.send(msg_BtoP.encode())
                    is_finished(pile, lock)
                    end = time.time()
        mq.remove()


if __name__ == "__main__":

    # Initialisation Pile
    # les numéros négatifs représentent les cartes bleus
    # et les numéros positifs les rouges

    # faire une fonction d'initialisation ou on construit une liste
    # avec tous les process ID
    pile = Array('i', range(-10, 10))
    lock = Lock()
    random.shuffle(pile)
    numJoueur = input("Entrez le nb de joueur :")
    theBoard = Board(1, 2, pile, lock)
