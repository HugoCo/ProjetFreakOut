import sysv_ipc
import time
import os
import pygame
key = 128
player_ID = os.getpid()
mq = sysv_ipc.MessageQueue(key)
cards_in_hand = list()
user_input = 0
timer = 0
state = 0
# state = 0 : Initialisation
# state = 1 : Envoie un message
# state = 2 : Attend la réponse
# state = 3 : envoie la carte ou recois un msg si
#c'est trop tard ou le résultat

if __name__ == "__main__":

    while user_input != "quit":
        if state == 0:
            user_input = int(input())
            msg_CtoB = (str(player_ID)).encode()
            mq.send(msg_CtoB, type=1)
            state = 1

        if state == 1:
            user_input = int(input())
            msg_CtoB = (str(player_ID) + ", " + str(user_input)).encode()
            mq.send(msg_CtoB, type=1)

    mq.remove()
