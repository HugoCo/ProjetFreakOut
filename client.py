import sysv_ipc
import time
import os
import threading
from multiprocessing import Queue
key = 128
player_ID = os.getpid()
cards_in_hand = list()
user_input = 0
timer = 0
state = "init"
start = 0
timer = 0
end = 0
# effacer console : https://python.developpez.com/faq/?page=Console#GenClearDos
# ajouter fin de la partie avec condition (pert ou gagne)


def sending_card(input_queue):
    while True:
        input_queue.put(input())


if __name__ == "__main__":
    print(player_ID)
    mq = sysv_ipc.MessageQueue(key)
    input_queue = Queue()
    input_thread = threading.Thread(
        target=sending_card, args=(input_queue,))
    input_thread.start()
    start = time.time()
    while user_input != "quit":

        if state == "init":
            msg_CtoB = (str(player_ID)).encode()
            mq.send(msg_CtoB, type=2)
            print("Voici les cartes piochées:")
            hand = mq.receive(type=player_ID + 1000)[0].decode()
            print(hand)
            state = "ready, set..."
            print(state)

        if state == "ready, set...":
            msg = mq.receive(type=player_ID+1000)[0].decode()
            if msg == "go":
                state = msg
            print(msg)

        if state == "go" or state == "not accepted":
            print("Quelle carte voulez-vous jouer?:")
            msg_CtoB = (str(player_ID) + ", "
                        + str(input_queue.get())).encode()
            mq.send(msg_CtoB, type=1)
            state = mq.receive(type=player_ID+1000)[0].decode()
            print(state)
            start = time.time()
            print(start)

        if state == "Play a card":
            end = time.time()
            timer = end - start
            if timer < 10:
                end = time.time()
                timer = end - start

            elif timer >= 10:
                print(timer)
                print("Pick a card")
                state = "go"
                mq.send("100", type=player_ID)

            if not input_queue.empty():
                msg_CtoB = (str(input_queue.get())).encode()
                mq.send(msg_CtoB, type=player_ID)
                state = mq.receive(type=player_ID+1000)[0].decode()
                print(state)

        if state == "Fin de la partie ":
            user_input = "quit"

    mq.remove()
    print("Partie Finie")
