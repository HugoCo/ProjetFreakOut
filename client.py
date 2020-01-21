import sysv_ipc
import time
import os
import threading
import sys
from multiprocessing import Queue

key = 6666
keyBP = 6667
player_ID = os.getpid()
user_input = 0
timer = 0
state = "init"
start = 0
timer = 0
end = 0
actual_hand = []
msg = ""
get_printed = True
first_card = ""


# effacer console : https://python.developpez.com/faq/?page=Console#GenClearDos
# ajouter fin de la partie avec condition (perd ou gagne)


def sending_card(input_queue):
    while True:
        input_queue.put(input())


def print_hand(hand):
    print("Votre main est : ")
    hand_list = hand.strip('][').split(', ')
    for i in range(len(hand_list)):
        if int(hand_list[i]) < 0:
            print("Blue : " + str((-int(hand_list[i]))) + " | ", end=' ')

        else:
            print("Red : " + hand_list[i] + " | ", end=' ')


def receive_hand():
    hand = mq.receive(
        type=player_ID + 1000)[0].decode()
    hand = hand.strip('][').split(', ')
    actual_hand = list(map(int, hand))
    return actual_hand


if __name__ == "__main__":
    print(player_ID)
    mq = sysv_ipc.MessageQueue(key)
    input_queue = Queue()
    input_thread = threading.Thread(target=sending_card, args=(input_queue,))
    input_thread.start()
    start = time.time()
    while user_input != "quit":

        if state == "init":
            msg_CtoB = (str(player_ID)).encode()
            mq.send(msg_CtoB, type=2)
            hand = mq.receive(type=player_ID + 1000)[0].decode()
            hand = hand.strip('][').split(', ')
            actual_hand = list(map(int, hand))
            state = "Ready, set..."
            print("")
            print(state)

        if state == "Ready, set...":
            msg = mq.receive(type=player_ID + 1000)[0].decode()
            if msg == "Go !":
                state = msg
            print(state)
            print(msg)

        if state == "Go !" or state == "Someone was faster !":
            if(get_printed == True):
                os.system('clear')
                print_hand(str(actual_hand))  # print la main du joueur
                print("")
                print("Enter O ou o to play:")
                print(msg)
            try:
                state = mq.receive(
                    block=False, type=player_ID + 1000)[0].decode()
                get_printed = True
            except sysv_ipc.BusyError:
                pass

            if not input_queue.empty():
                input_to_play = str(input_queue.get())
                if input_to_play == "O" or "o":
                    msg_CtoB = str(player_ID).encode()
                    mq.send(msg_CtoB, type=1)
                    state = mq.receive(type=player_ID + 1000)[0].decode()
                    print(state)
                    if(state == "Someone was faster !"):
                        print("Enter O ou o to play:")
                    start = time.time()
            get_printed = False

        if state == "Play a card":
            end = time.time()
            timer = end - start
            if timer < 10:
                end = time.time()
                timer = end - start
            elif timer >= 10:
                print("Pick a card")
                mq.send("Timeout", type=player_ID)
                actual_hand = receive_hand()
                state = "Go !"
                get_printed = True

            if not input_queue.empty():
                msg_CtoB = str(input_queue.get())

                # Check bleu
                if msg_CtoB[0] == "B":
                    msg_CtoB = msg_CtoB.replace("B", "-")
                    print(msg_CtoB)
                    msg_CtoB = int(msg_CtoB)

                    if -11 < msg_CtoB < 11 and msg_CtoB in actual_hand:
                        mq.send(str(msg_CtoB).encode(), type=player_ID)
                        actual_hand = receive_hand()
                        state = "Go !"
                        get_printed = True
                    else:
                        print("Saisie non valide, recommencez:")
                # Check Rouge
                elif msg_CtoB[0] == "R":
                    msg_CtoB = msg_CtoB.replace("R", "")
                    msg_CtoB = int(msg_CtoB)

                    if -11 < msg_CtoB < 11 and msg_CtoB in actual_hand:
                        mq.send(str(msg_CtoB).encode(), type=player_ID)
                        actual_hand = receive_hand()
                        state = "Go !"
                        get_printed = True
                    else:
                        print("Saisie non valide, recommencez:")

                else:
                    print("Saisie non valide, recommencez:")

                print(state)
        if state == "Fin de la partie ":
            user_input = "quit"

    mq.remove()
    print("Partie Finie")
