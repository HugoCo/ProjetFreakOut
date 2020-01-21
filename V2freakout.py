import sysv_ipc
import random
import ast
from multiprocessing import Process, Lock, Queue

#debugger, timer, communication dans le main,

key = 128
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)


def is_finished(pile, lock):
    with lock:
        if len(pile) == 0:
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
        self.queue_list = queue_list
        self.player_list = player_list
        cleanmq()
        self.run(pile, lock)

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
        if self.card < 0:
            top_of_pile = "La première carte est : Bleu " + str(-self.card)
        else:
            top_of_pile = "La première carte est : Rouge " + str(self.card)
        print(len(player_list))
        self.broadcast(top_of_pile)
        self.broadcast("go")

        while not is_finished(pile, lock):
            # premier message : ID du player
            #
            player_ID = int((mq.receive(type=1)[0]).decode())
            mq.send("Play a card".encode(), type=player_ID + 1000)
            received_message = mq.receive(type=player_ID)[0].decode()
            print("received_message" + str(received_message))
            if self.card<0:
                print("card on top: B" + str(-self.card))
            else:
                print("card on top: R" + str(self.card))

            # client failed to send a card
            if received_message == "Timeout":
                new_card = 404
                for i, player in enumerate(self.player_list):
                    if player.player_ID == player_ID:
                        self.queue_list[i].put(new_card)

            # card is valid
            elif is_valid(self.card, int(received_message)):
                received_card = int(received_message)
                print("is valid")
                for i, player in enumerate(self.player_list):
                    if player.player_ID == player_ID:
                        self.queue_list[i].put(received_card)
                        print("HERE")
                self.card = received_card

            # card is not valid
            # Si mauvais on renvoie le numéro de la carte + 200
            else:
                print("is not valid")
                received_message = int(received_message)
                for i, player in enumerate(self.player_list):
                    if player.player_ID == player_ID:
                        self.queue_list[i].put(received_message + 200)
                    # mq.send("go".encode(), type=player_ID + 1000)

            """while mq.current_messages != 0:
                not_accepted_ID = int(mq.receive(type=1).decode())
                mq.send("Someone was faster !".encode(),
                        type=not_accepted_ID + 1000)"""
            cleanmq()

        print("exiting.")
        mq.remove()


class Player(Process):
    def __init__(self, pile, lock, player_ID, q):
        super(Player, self).__init__()
        self.hand = []
        self.player_ID = int(player_ID)
        self.q = q
        self.pile = pile
        self.lock = lock
        print(player_ID)
        for i in range(5):
            self.hand.append(pioche(self.pile, self.lock))
        mq.send((str(self.hand)).encode(), type=self.player_ID+1000)
        print("main sent " + str(self.hand))

    def run(self):
        while len(self.hand) != 0:
            # s'il y a encore des cartes dans la main
            if not self.q.empty():
                print("Q not empty")
                msg_BtoP = self.q.get()
                print("msg_BtoP : ", msg_BtoP)

                for card in self.hand:
                    print("check cards")
                    if msg_BtoP == card:
                        self.hand.remove(card)
                        print("is valid = " + str(self.hand))
                        mq.send((str(self.hand)).encode(),
                                type=self.player_ID + 1000)
                        break
                    elif msg_BtoP == (200 + card) or msg_BtoP == 404:
                        print("ERREUR 404")
                        self.hand.append(pioche(self.pile, self.lock))
                        mq.send(str(self.hand).encode(),
                                type=self.player_ID + 1000)
                        break


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
    # Waiting for all process Player to be connected before
    print("Waiting for player")
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
