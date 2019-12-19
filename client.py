import sysv_ipc
 
key = 128
 
mq = sysv_ipc.MessageQueue(key)
 
while True:
    message, t = mq.receive()
    value = message.decode()
    value = int(value)
    if value:
        print("received:", value)
    else:
        print("exiting.")
        break