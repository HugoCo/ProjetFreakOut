import sysv_ipc
import time
import os
import threading
from multiprocessing import Queue

key = 128  # clé
player_ID = os.getpid()
user_input = 0
timer = 0
state = "init"
start = 0
timer = 0
end = 0
actual_hand = []
msg = ""


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
            print("Bleu : " + str((-int(hand_list[i]))) + " | ", end='')

        else:
            print("Rouge : " + hand_list[i] + " | ", end='')


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
            state = "ready, set..."
            print("")
            print(state)

        if state == "ready, set...":
            msg = mq.receive(type=player_ID + 1000)[0].decode()
            if msg == "go":
                state = msg
            print(msg)

        if state == "go" or state == "Someone was faster !":
            print_hand(str(actual_hand))  # print la main du joueur
            print("")
            print("Entrez O ou o pour jouer:")
            input_to_play = input_queue.get()
            if input_to_play == "O" or "o":
                msg_CtoB = str(player_ID).encode()
                mq.send(msg_CtoB, type=1)
                state = mq.receive(type=player_ID + 1000)[0].decode()
            print(state)
            start = time.time()

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
                state = "go"

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
                        state = "go"
                        print("Dans PICK A CARD" + state)
                    else:
                        print("Saisie non valide, recommencez:")
                # Check Rouge
                elif msg_CtoB[0] == "R":
                    msg_CtoB = msg_CtoB.replace("R", "")
                    msg_CtoB = int(msg_CtoB)

                    if -11 < msg_CtoB < 11 and msg_CtoB in actual_hand:
                        mq.send(str(msg_CtoB).encode(), type=player_ID)
                        actual_hand = receive_hand()
                        state = "go"
                        print(state)
                    else:
                        print("Saisie non valide, recommencez:")

                else:
                    print("Saisie non valide, recommencez:")

                print(state)

        if state == "Fin de la partie ":
            user_input = "quit"

    mq.remove()
    print("Partie Finie")
