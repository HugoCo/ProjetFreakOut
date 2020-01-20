import sysv_ipc
import random
import time
import ast
from multiprocessing import Process, Lock, Pipe

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


class Board:
    def __init__(self, num_card, num_players, pile, lock):
        self.card = num_card
        self.num_players = num_players
        self.player_list = []
        self.board_con_list = []

        for i in range(1):
            player_ID = int(mq.receive(type=2)[0].decode())
            player_conn, board_conn = Pipe()
            self.board_conn_list.append(board_conn)
            p = Player(pile, lock, player_ID, player_conn)
            print("Player ", i, "initialized")
            self.player_list.append(p)
            print(type(p))
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
            msg_PtoB, t = (mq.receive(type=1))[0].decode()
            msg_PtoB = ast.literal_eval(msg_PtoB)
            print("received:", msg_PtoB)
            player_ID = msg_PtoB[0]
            print(player_ID)
            received_card = int(msg_PtoB[1])
            if is_valid(self.card, received_card):
                self.card = received_card
                print(self.card)
                message = 1
                # msg_BtoP = (str(received_card)).encode()
                # mq.send(msg_BtoP, type=player_ID+1)
                for player, i in enumerate(self.player_list):
                    if player.player_ID == player_ID:
                        self.board_conn_list[i].send(received_card)
            else:
                # Si mauvais on renvoie le numéro de la carte + 200
                # msg_BtoP = (str(received_card+200)).encode()
                # mq.send(msg_BtoP, type=player_ID+1)
                for player, i in enumerate(self.player_list):
                    if player.player_ID == player_ID:
                        self.board_conn_list[i].send(received_card + 200)
            while mq.current_messages != 0:
                mq.receive(type=1)
                print(mq.current_messages)
                print("cleaning mq")

        print("exiting.")
        mq.remove()


class Player(Process):
    def __init__(self, pile, lock, player_ID, player_conn):
        super(Player, self).__init__()
        self.hand = []
        self.player_ID = player_ID
        print(player_ID)
        for i in range(5):
            print("pioche : i")
            self.hand.append(pioche(pile, lock))
        mq.send(("Votre main est" + str(self.hand)).encode(),
                type=self.player_ID+1000)
        print("main sent")

    def run_random(self):
        while(len(self.hand) != 0):
            msg_BtoP = self.player_con.recv
            print(msg_BtoP)
            # msg_BtoP, t = mq.receive(type=self.player_ID + 1)
            # msg_BtoP = msg_BtoP.decode()
            # msg_BtoP = int(msg_BtoP)

            if msg_BtoP < 100:
                top_of_pile = msg_BtoP

            for card in self.hand:
                if msg_BtoP == card:
                    self.hand.remove(card)
                elif msg_BtoP == (100 + card):
                    self.hand.append(pioche())
            message_PtoC = str(msg_BtoP).encode()
            mq.send(message_PtoC, type=self.player_ID + 1000)

            print("received:", msg_BtoP)
            time_to_play = random.random()*10
            card_to_play = self.hand[int(random.random(len(self.hand)))]
            time.sleep(time_to_play)


if __name__ == "__main__":

    # Initialisation Pile
    # les numéros négatifs représentent les cartes bleus
    # et les numéros positifs les rouges

    # faire une fonction d'initialisation ou on construit une liste
    # avec tous les process ID

    pile = list(range(-10, 10))
    lock = Lock()
    random.shuffle(pile)
    numJoueur = int(input("Entrez le nb de joueur :"))
    pioche(pile, lock)
    theBoard = Board(pile[0], numJoueur, pile, lock)
