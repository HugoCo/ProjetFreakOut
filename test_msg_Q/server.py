import sysv_ipc
key = 128
player_ID = 0
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

value_r = 1
if __name__ == "__main__":
    player_ID, t = mq.receive(type=2)
    player_ID = int(player_ID.decode())
    print("process iD = "+str(player_ID))
    mq.send("go", type=player_ID+1000)
while True:
    value_s = input("ENVOIE SERVER VERS CLIENT")
    message_s = value_s.encode()
    mq.send(message_s, type=player_ID+1000)
    print(mq.receive(type=1)[0].decode())
mq.remove()
