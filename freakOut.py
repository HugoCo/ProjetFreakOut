import sysv_ipc
import random
import time
import ast
from multiprocessing import Process, Lock, Queue

#debugger, timer, communication dans le main,

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


def cleanmq():
    while mq.current_messages != 0:
        mq.receive()
        print(mq.current_messages)
        print("cleaning mq")


class Board:
    def __init__(self, num_card, num_players, pile, lock):
        self.card = num_card
        self.num_players = num_players
        self.player_list = []
        self.queue_list = []
        cleanmq()
        for i in range(num_players):
            player_ID = int(mq.receive(type=2)[0].decode())
            q = Queue()
            self.queue_list.append(q)
            p = Player(pile, lock, player_ID, q)
            print("Player ", i, "initialized")
            self.player_list.append(p)
            p.start()
            print("started")
        self.run(pile, lock)

        # il faut start les processes

    def broadcast(self, msg, player=None):
        if isinstance(player, Player):
            for client in self.player_list:
                if client != player:
                    mq.send(msg.encode(), type=client.player_ID+1000)
        else:
            for client in self.player_list:
                mq.send(msg.encode(), type=client.player_ID+1000)

    def run(self, pile, lock):
        print("arrived to run board")
        first_card = pioche(pile, lock)
        first_card = ("La première carte est : " + str(first_card))
        self.broadcast(first_card)
        self.broadcast("go")

        message = 0
        while not is_finished(pile, lock):
            # Message Queue Player to Board
            msg_PtoB = (mq.receive(type=1)[0]).decode()
            print(msg_PtoB)
            print("received:", msg_PtoB)
            player_ID = msg_PtoB
            mq.send("Play a card".encode(), type=player_ID + 1000)
            print(type(player_ID))
            received_card = (mq.receive(type=player_ID)[0])
            if received_card == "Timeout":
                #ajouter un message vers le player
                cleanmq()
                self.broadcast("go")

            if is_valid(self.card, received_card):
                self.card = received_card
                print(self.card)
                message = 1
                msg_BtoP = (str(received_card)).encode()
                mq.send(msg_BtoP, type=player_ID+10000)
                for i, player in enumerate(self.player_list):
                    if player.player_ID == player_ID:
                        self.queue_list[i].put(received_card)
            else:
                # Si mauvais on renvoie le numéro de la carte + 200
                # msg_BtoP = (str(received_card+200)).encode()
                # mq.send(msg_BtoP, type=player_ID+1)
                for i, player in enumerate(self.player_list):
                    if player.player_ID == player_ID:
                        print(type(self.queue_list[i]))
                        self.queue_list[i].put(received_card + 200)
            while mq.current_messages != 0:
                mq.receive()
                print(mq.current_messages)
                print("cleaning mq")
            cleanmq()

        print("exiting.")
        mq.remove()


class Player(Process):
    def __init__(self, pile, lock, player_ID, q):
        super(Player, self).__init__()
        self.hand = []
        self.player_ID = player_ID
        self.q = q
        print(player_ID)
        for i in range(5):
            print("pioche : i")
            self.hand.append(pioche(pile, lock))
        mq.send((str(self.hand)).encode(),
                type=self.player_ID+1000)
        print("main sent")
        #self.run()

    def run(self):
        while len(self.hand) != 0:
            if self.q.empty() == False:
                msg_BtoP = self.q.get()
                print("msg_BtoP", msg_BtoP)

                # if msg_BtoP < 100:
                # top_of_pile = msg_BtoP

                for card in self.hand:
                    if msg_BtoP == card:
                        self.hand.remove(card)
                        mq.send("Coup correct, voici votre nouvelle main : "
                                + str(self.hand).encode(), type=self.player_ID + 1000)
                    elif msg_BtoP == (200 + card):
                        self.hand.append(pioche())
                        mq.send("Coup incorrect, vous piochez. Voici votre nouvelle main : "
                                + str(self.hand).encode(), type=self.player_ID + 1000)

                print("received:", msg_BtoP)


if __name__ == "__main__":

    # Initialisation Pile
    # les numéros négatifs représentent les cartes bleus
    # et les numéros positifs les rouges

    # faire une fonction d'initialisation ou on construit une liste
    # avec tous les process ID

    pile = list(range(-10, 10))
    pile.pop(10)
    print(pile)
    lock = Lock()
    random.shuffle(pile)
    numJoueur = int(input("Entrez le nb de joueur :"))
    pioche(pile, lock)
    theBoard = Board(pile[0], numJoueur, pile, lock)
