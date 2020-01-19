import sysv_ipc
import time
import os
import threading
from multiprocessing import Queue
key = 128
player_ID = os.getpid()
mq = sysv_ipc.MessageQueue(key)
cards_in_hand = list()
user_input = 0
timer = 0
state = "init"
start = 0
timer = 0
end = 0

# ajouter fin de la partie avec condition (pert ou gagne)


def sending_card(input_queue):
    while True:
        input_queue.put(input())


if __name__ == "__main__":
    print(player_ID)
    input_queue = Queue()
    input_thread = threading.Thread(
        target=sending_card, args=(input_queue,))
    input_thread.start()
    start = time.time()
    while user_input != "quit":

        if state == "init":
            msg_CtoB = (str(player_ID)).encode()
            mq.send(msg_CtoB, type=2)
            state = "ready, set..."
            print(state)

        if state == "ready, set...":
            msg = mq.receive(type=player_ID+1000)[0].decode()
            if msg == "go":
                msg = state
            print(msg)

        if state == "go" or state == "not accepted":
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

            if not input_queue.empty():
                msg_CtoB = (str(player_ID) + ", "
                            + str(input_queue.get())).encode()
                mq.send(msg_CtoB, type=1)
                state = mq.receive(type=player_ID+1000)[0].decode()
                print(state)

        if state == "Fin de la partie ":
            user_input = "quit"

    mq.remove()
    print("Partie Finie")
