import sysv_ipc
import os
player_ID = os.getpid()

key_BtoP = 128
key_PtoB = 129

mq_BtoP = sysv_ipc.MessageQueue(key_BtoP)
mq_PtoB = sysv_ipc.MessageQueue(key_PtoB, sysv_ipc.IPC_CREAT)

if __name__ == "__main__":
    # Creating Message Queue Player to Board (server)
    value_PtoB = 1
    while value_PtoB:
        try:
            value_PtoB = int(input())
        except:
            print("Input error, try again!")
        message_PtoB = str(value_PtoB).encode()
        mq_PtoB.send(message_PtoB)

    mq_PtoB.remove()

    # Creating Message Queue Board to Player (client)
    while True:
        message_BtoP, t = mq_BtoP.receive()
        value_BtoP = message_BtoP.decode()
        value_BtoP = int(value_BtoP)
        if value_BtoP:
            print("received:", value_BtoP)
        else:
            print("exiting.")
            break
