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
state = 0
start = 0
timer = 0
end = 0
# state = 1 : Envoie un message
# state = 2 : Attend la réponse
# state = 3 : envoie la carte ou recois un msg si
#             c'est trop tard ou le résultat


def sending_card(input_queue):
    while True:
        input_queue.put(input())


if __name__ == "__main__":
    input_queue = Queue()
    input_thread = threading.Thread(
        target=sending_card, args=(input_queue,))
    input_thread.start()
    start = time.time()
    while user_input != "quit":
        if state == "init":
            msg_CtoB = (str(player_ID)).encode()
            mq.send(msg_CtoB, type=1)
            state = "ready, set..."

            print(state)
        if state == "ready, set...":
            state = mq.receive(type=player_ID+1000).decode()
            print(state)

        if state == "go":
            msg_CtoB = (str(player_ID) + ", "
                        + str(input_queue.get())).encode()
            mq.send(msg_CtoB, type=1)
            state = "Play a card"
            print(state)

        if state == "play a card":
            if timer < 10:
                end = time-time()
                timer = end - start
                print(timer)

            elif timer >= 10:
                print("Pick a card")
                state = "go"

            if not input_queue.empty():
                msg_CtoB = (str(player_ID) + ", "
                            + str(input_queue.get())).encode()
                mq.send(msg_CtoB, type=1)

    mq.remove()
