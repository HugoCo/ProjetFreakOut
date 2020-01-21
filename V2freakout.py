import sysv_ipc
import random
import ast
from multiprocessing import Process, Lock, Queue, Manager

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
        pile.pop(0)
    return card_from_pile


def cleanmq(t=None):
    while mq.current_messages != 0:
        if isinstance(t, int):
            mq.receive(type=t)
        else:
            mq.receive()
        print("cleaning mq")


class Board:
    def __init__(self, num_players, player_list, pile, lock, queue_list):
        self.num_players = num_players
        # self.player_list = []
        self.queue_list = queue_list
        self.player_list = player_list
        cleanmq()
        """for i in range(num_players):
            player_ID = int(mq.receive(type=2)[0].decode())
            q = Queue()
            self.queue_list.append(q)
            p = Player(pile, lock, player_ID, q)
            print("Player ", i, "initialized")
            self.player_list.append(p)
            p.start()
            print("started")"""
        self.run(pile, lock)

        # il faut start les processes

    def broadcast(self, msg, not_this_player=None):
        if isinstance(not_this_player, Player):
            for client in self.player_list:
                if client != not_this_player:
                    mq.send(msg.encode(), type=client.player_ID+1000)
        else:
            for client in self.player_list:
                mq.send(msg.encode(), type=client.player_ID+1000)

    def run(self, pile, lock):
        print("arrived to run board")
        self.card = pioche(pile, lock)
        top_of_pile = ("La première carte est : " + str(self.card))
        print(len(player_list))
        self.broadcast(top_of_pile)
        self.broadcast("go")

        while not is_finished(pile, lock):
            # Message Queue Player to Board
            player_ID = int((mq.receive(type=1)[0]).decode())
            mq.send("Play a card".encode(), type=player_ID + 1000)
            received_card = mq.receive(type=player_ID)[0].decode()
            print("received_card" + str(received_card))
            if received_card == "Timeout":
                # ajouter un message vers le player
                cleanmq()
                self.broadcast("go")
            print("card on top:" + str(self.card))
            if is_valid(self.card, int(received_card)):
                received_card = int(received_card)
                print("is valid")
                self.card = received_card
                msg_BtoP = (str(received_card)).encode()
                mq.send(msg_BtoP, type=player_ID+10000)
                for i, player in enumerate(self.player_list):
                    print("enumarate for here")
                    if player.player_ID == player_ID:
                        self.queue_list[i].put(received_card)
            else:
                print("is not valid")
                # Si mauvais on renvoie le numéro de la carte + 200
                # msg_BtoP = (str(received_card+200)).encode()
                # mq.send(msg_BtoP, type=player_ID+1)
                for i, player in enumerate(self.player_list):
                    if player.player_ID == player_ID:
                        self.queue_list[i].put(received_card + 200)
            while mq.current_messages != 0:
                mq.receive()
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
            self.hand.append(pioche(pile, lock))
        mq.send(("Votre main est" + str(self.hand)).encode(),
                type=self.player_ID+1000)
        print("main sent " + str(self.hand))

    def run(self):
        print("LA")
        while len(self.hand) != 0:
            """msg_PtoC = mq.receive(type=self.player_ID + 500)[0].decode()
            if(msg_PtoC == "Can I have my hand?"):
                mq.send(("Votre main est" + str(self.hand)).encode(),
                        type=self.player_ID+1000)"""
            if not self.q.empty():
                print("HERE")
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
    lock = Lock()

    random.shuffle(pile)
    pile.remove(0)
    numJoueur = int(input("Entrez le nb de joueur :"))
    queue_list = []
    player_list = []
    # pioche(pile, lock)

    print("waiting for player")
    # initialisation players
    for i in range(numJoueur):
        player_ID = int(mq.receive(type=2)[0].decode())
        q = Queue()
        queue_list.append(q)
        p = Player(pile, lock, player_ID, q)
        print("Player ", i, "initialized")
        player_list.append(p)
        print(len(player_list))
        p.start()
        print("started")

    theBoard = Board(numJoueur, player_list, pile, lock, queue_list)
    theBoard.start()