import sysv_ipc
import random
from multiprocessing import Process, Manager
import time

key = 6666
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
keyBP = 6667
mqBP = sysv_ipc.MessageQueue(keyBP, sysv_ipc.IPC_CREAT)


def is_finished(pile):
    if len(pile) == 0:
        return True
    return False


def is_valid(board_card, player_card):
    if ((player_card == board_card + 1)
        or (player_card == board_card - 1)
            or (abs(player_card) == abs(board_card))):
        return True
    return False


def pioche(pile):
    if not is_finished(pile):
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
        return("The card on the board is: Blue " + str(-card))
    else:
        return("The card on the board is: Red " + str(card))


class Board():
    def __init__(self, num_players, player_list, pile):
        self.num_players = num_players
        self.player_list = player_list
        self.pile = pile
        cleanmq()
        self.run()

    def broadcast(self, msg, typenum, not_this_player=None):
        if isinstance(not_this_player, int):
            if typenum == 1000:
                for client in self.player_list:
                    if client.player_ID != not_this_player:
                        mq.send(msg.encode(), type=client.player_ID+typenum)
            else :
                for client in self.player_list:
                    if client.player_ID != not_this_player:
                        mqBP.send(msg.encode(), type=client.player_ID+typenum)
        else:
            if typenum == 1000:
                for client in self.player_list:
                    mq.send(msg.encode(), type=client.player_ID+typenum)
            else:
                for client in self.player_list:
                    mqBP.send(msg.encode(), type=client.player_ID+typenum)

    def run(self):
        self.card = pioche(self.pile)
        print(cardtodisplay(self.card))
        self.broadcast("Go !", 1000)
        #print("taille de la pile", len(self.pile))
        finished = is_finished(self.pile)
        while True:
            if finished == True:
                break
            else:
                finished = is_finished(self.pile)
                #print(finished)
                # premier message : ID du player
                player_ID = int((mq.receive(type=1)[0]).decode())
                #print(player_ID)
                mq.send("Play a card".encode(), type=player_ID + 1000)
                received_message = mq.receive(type=player_ID)[0].decode()
                #print("received message", received_message)
                print(cardtodisplay(self.card))

                # client failed to send a card
                if received_message == "Timeout":
                    pick_card = 404
                    mqBP.send(str(pick_card).encode(), type=player_ID + 500)

                # card is valid
                elif is_valid(self.card, int(received_message)):
                    #print("is valid")
                    mqBP.send(str(received_message).encode(),
                              type=player_ID + 500)
                    self.card = int(received_message)

                # card is not valid
                # Si mauvais on renvoie le numéro de la carte + 200
                elif not is_valid(self.card, int(received_message)):
                    #print("is not valid")
                    received_message = int(received_message) + 200
                    mqBP.send(str(received_message).encode(),
                              type=player_ID + 500)

                cleanmq()
                print(cardtodisplay(self.card))
                self.broadcast("Someone was faster !", 1000, player_ID)
        print("PERDU")
        self.broadcast("Fin", 1000)
        self.broadcast("666", 500)


class Player(Process):
    def __init__(self, player_ID, pile):
        super(Player, self).__init__()
        self.hand = []
        self.player_ID = int(player_ID)
        #print(player_ID)
        self.pile = pile
        for i in range(5):
            self.hand.append(pioche(self.pile))
        mq.send((str(self.hand)).encode(), type=self.player_ID+1000)
        #print("main sent " + str(self.hand))

    def run(self):
        hand_size = len(self.hand)
        while hand_size > 0:
            # s'il y a encore des cartes dans la main
            if mqBP.current_messages != 0:
                msg = mqBP.receive(
                    type=self.player_ID + 500)[0].decode()
                #print(msg)
                msg = int(msg)
                for card in self.hand:
                    if msg == card:
                        self.hand.remove(card)
                        #print("is valid = " + str(self.hand))
                        mq.send((str(self.hand)).encode(),
                                type=self.player_ID + 1000)
                        break
                    elif msg == (200 + card) or msg == 404:
                        #print("ERREUR 404")
                        self.hand.append(pioche(self.pile))
                        #print(self.hand)
                        mq.send(str(self.hand).encode(),
                                type=self.player_ID + 1000)
                        break
                #print("main sent " + str(self.hand))
                if msg == 666:
                    #print("666")
                    hand_size = -1
        print("CLOSING")


if __name__ == "__main__":

    # Initialisation Pile
    # les numéros négatifs représentent les cartes bleus
    # et les numéros positifs les rouges

    # faire une fonction d'initialisation ou on construit une liste
    # avec tous les process ID
    manager = Manager()
    pile = manager.list(range(-10, 10))
    random.shuffle(pile)
    pile.remove(0)
    numJoueur = 1
    while True:
        try:
            numJoueur = int(input("Entrez le nb de joueur :"))
            if numJoueur <= 0:
                raise ValueError
            break
        except ValueError:
            print("Veuillez entrer un nombre entier plus grand que  0")

    cleanmq()
    player_list = []
    # Waiting for all process Player to be connected before
    print("Waiting for player...")
    # initialisation players
    for i in range(numJoueur):
        player_ID = int(mq.receive(type=2)[0].decode())
        p = Player(player_ID, pile)
        print("Player ", i, "initialized")
        player_list.append(p)
        p.start()
    theBoard = Board(numJoueur, player_list, pile)
    print("PARTIE FINIE")
    for p in player_list:
        p.terminate()
    if mqBP.current_messages == 0 and mqBP.current_messages == 0:
        mq.remove()
        mqBP.remove()
