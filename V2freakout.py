import sysv_ipc
import random
from multiprocessing import Process, Lock

key = 6666
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
keyBP = 6667
mqBP = sysv_ipc.MessageQueue(keyBP, sysv_ipc.IPC_CREAT)

pile = list(range(-10, 10))
lock = Lock()


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


def cardtodisplay(card):
    if card < 0:
        return("The first card is: Blue" + str(-card))
    else:
        return("The first card is: Red" + str(card))


class Board:
    def __init__(self, num_players, player_list, pile, lock):
        self.num_players = num_players
        self.player_list = player_list
        cleanmq()
        self.run(pile, lock)

    def broadcast(self, msg, not_this_player=None):
        if isinstance(not_this_player, int):
            for client in self.player_list:
                if client.player_ID != not_this_player:
                    mq.send(msg.encode(), type=client.player_ID+1000)
        else:
            for client in self.player_list:
                mq.send(msg.encode(), type=client.player_ID+1000)

    def run(self, pile, lock):
        self.card = pioche(pile, lock)
        toppile = cardtodisplay(self.card)
        print(toppile)
        self.broadcast(toppile)
        self.broadcast("Go !")

        while not is_finished(pile, lock):
            # premier message : ID du player
            #
            player_ID = int((mq.receive(type=1)[0]).decode())
            mq.send("Play a card".encode(), type=player_ID + 1000)
            received_message = mq.receive(type=player_ID)[0].decode()
            print(cardtodisplay(self.card))

            # client failed to send a card
            if received_message == "Timeout":
                pick_card = 404
                mqBP.send(str(pick_card).encode(), type=player_ID + 500)

            # card is valid
            elif is_valid(self.card, int(received_message)):
                print("is valid")
                mqBP.send(str(received_message).encode(), type=player_ID + 500)
                self.card = int(received_message)

            # card is not valid
            # Si mauvais on renvoie le numéro de la carte + 200
            else:
                print("is not valid")
                received_message = int(received_message) + 200
                mqBP.send(str(received_message).encode(), type=player_ID + 500)

            cleanmq()
            self.broadcast("Someone was faster !", player_ID)
        print("exiting.")
        mq.remove()


class Player(Process):
    def __init__(self, player_ID):
        super(Player, self).__init__()
        self.hand = []
        self.player_ID = int(player_ID)
        print(player_ID)
        for i in range(5):
            self.hand.append(pioche(pile, lock))
        mq.send((str(self.hand)).encode(), type=self.player_ID+1000)
        print("main sent " + str(self.hand))

    def run(self):
        while len(self.hand) != 0:
            # s'il y a encore des cartes dans la main
            if mq.current_messages != 0:
                print("Q not empty")
                msg = int(mqBP.receive(type=self.player_ID + 500)[0].decode())

                for card in self.hand:
                    print("check cards")
                    if msg == card:
                        self.hand.remove(card)
                        print("is valid = " + str(self.hand))
                        mq.send((str(self.hand)).encode(),
                                type=self.player_ID + 1000)
                        break
                    elif msg == (200 + card) or msg == 404:
                        print("ERREUR 404")
                        self.hand.append(pioche(pile, lock))
                        mq.send(str(self.hand).encode(),
                                type=self.player_ID + 1000)
                        break


if __name__ == "__main__":

    # Initialisation Pile
    # les numéros négatifs représentent les cartes bleus
    # et les numéros positifs les rouges

    # faire une fonction d'initialisation ou on construit une liste
    # avec tous les process ID
    cleanmq()
    random.shuffle(pile)
    pile.remove(0)
    numJoueur = int(input("Entrez le nb de joueur :"))
    player_list = []
    # Waiting for all process Player to be connected before
    print("Waiting for player...")
    # initialisation players
    for i in range(numJoueur):
        player_ID = int(mq.receive(type=2)[0].decode())
        p = Player(player_ID)
        print("Player ", i, "initialized")
        player_list.append(p)
        p.start()

    theBoard = Board(numJoueur, player_list, pile, lock)
    theBoard.start()
