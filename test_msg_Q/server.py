import sysv_ipc
import os

key = 128

mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
print(os.getpid())

value_r = 1
while value_r:
    value_s = int(input("ENVOIE SERVER VERS CLIENT"))
    message_s = str(value_s).encode()
    mq.send(message_s)
    print("HERE")
    message_r, t = mq.receive()
    value_r = message_r.decode()
    print(value_r)

mq.remove()
