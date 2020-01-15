import sysv_ipc
import time
import ast
key = 128

mq = sysv_ipc.MessageQueue(key)

i = True
timer = 0
while True:
    start = time.time()
    end = time.time()
    timer = end-start
    print(timer)
    if timer < 10:
        print("DANS LA BOUCLE TIMER")
        message_r, t = mq.receive(type=4)
        value_r = message_r.decode()
        print("msg recu")
        print("received:", value_r)
        print(t)
