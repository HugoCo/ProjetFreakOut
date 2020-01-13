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
        message_r, t = mq.receive()
        value_r = message_r.decode()
        value_r = value_r
        """if value:
            print("msg recu")
            print("received:", value)
            if i:
                premier_process = (mq.last_send_pid)
                print(premier_process)
        else:
            print("exiting.")
            break"""
        print("msg recu")
        print("received:", value_r)
    message_s = "timer restart".encode()
    mq.send(message_s)
