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
# state = 1 : Envoie un message
# state = 2 : Attend la réponse
# state = 3 : envoie la carte ou recois un msg si
#             c'est trop tard ou le résultat


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
            state = mq.receive()[0].decode()
            print(state)

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

    mq.remove()
