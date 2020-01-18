import sysv_ipc
import os
import time
key = 128

mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
print(os.getpid())

value_r = 1
if __name__ == "__main__":
    start = time.time()
    timer = end - start
while value_r:
    value_s = int(input("ENVOIE SERVER VERS CLIENT"))
    message_s = str(value_s).encode()
    mq.send(message_s, type=4)
    print("HERE")

mq.remove()
