import sysv_ipc
import random
import time
import ast
from multiprocessing import Process, Array, Lock

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
        print(pile[0])
        pile.pop(0)
    return card_from_pile


class Board:
    def __init__(self, num_card, num_players, pile, lock):
        self.card = num_card
        self.num_players = num_players
        for i in range(0, num_players):
            player_ID = mq.receive(type=2)
            p = Player(pile, lock, player_ID)
            self.player_list.append(p)
            p.start()

        start = time.time()
        # il faut start les processes

    def run(self, lock):
        first_card = pioche(pile, lock)
        for player in self.player_list:
            first_card = first_card.encode()
            mq.send(first_card, type=player.player_ID + 10000)
        message = 0
        while(not is_finished(pile, lock)):
            # Message Queue Player to Board
            msg_PtoB, t = (mq.receive(type=1)).decode()
            msg_PtoB = ast.literal_eval(msg_PtoB)
            print("received:", msg_PtoB)
            player_ID = msg_PtoB[0]
            received_card = msg_PtoB[1]
            if is_valid(self.card, received_card):
                self.card = received_card
                message = 1
                msg_BtoP = (str(received_card)).encode()
                mq.send(msg_BtoP, type=player_ID+1)
            else:
                # Si mauvais on renvoie le numéro de la carte + 200
                msg_BtoP = (str(received_card+200)).encode()
                mq.send(msg_BtoP, type=player_ID+1)
            mq.empty()
        print("exiting.")
        mq.remove()


class Player(Process):
    def __init__(self, pile, lock, player_ID):
        self.hand = []
        self.player_ID = player_ID
        for i in range(6):
            self.hand.append(pioche(pile, lock))

    def run_random(self):
        while(len(self.hand) != 0):
            msg_BtoP, t = mq.receive(type=self.player_ID + 1)
            msg_BtoP = msg_BtoP.decode()
            msg_BtoP = int(msg_BtoP)
            # msg_BtoP est un tuple avec 3 valeurs :
            # (destinataire, source, valeur de la carte)
            if msg_BtoP[3] < 100:
                top_of_pile = msg_BtoP

            for card in self.hand:
                if msg_BtoP == card:
                    self.hand.remove(card)
                elif msg_BtoP == (100 + card):
                    self.hand.append(pioche())

            print("received:", msg_BtoP)
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

    # faire une fonction d'initialisation ou on construit une liste
    # avec tous les process ID
    pile = Array('i', range(-10, 10))
    lock = Lock()
    random.shuffle(pile)
    numJoueur = int(input("Entrez le nb de joueur :"))
    pioche(pile, lock)
    #theBoard = Board(pile[0], numJoueur, pile, lock)
