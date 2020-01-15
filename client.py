import sysv_ipc
import os
player_ID = os.getpid()

key = 128

mq = sysv_ipc.MessageQueue(key)
user_input = 0

if __name__ == "__main__":

    print("Starting")
    pid_init = str(player_ID)
    mq.send(pid_init.encode())
    # Creating Message Queue Player to Board (server)
    while user_input != "quit":
        try:
            user_input = int(input())
        except:
            print("Input error, try again!")
        # msg_BtoP est un tuple avec 3 valeurs :
        # (destinataire, source, valeur de la carte)
        msg_PtoB = ("board" + ", " + str(player_ID)
                    + ", " + str(user_input)).encode()
        mq.send(msg_PtoB)
    m                                                                                                                                                                                                                           q.remove()
