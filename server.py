import socket
from threading import Thread

connections = []

def main():
    print('Server Started')
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # harus tuple
    sock.bind(('',8000))
    sock.listen(10)

    while True:
        con,addrs = sock.accept()
        connections.append(con)

        print('Connection Established on' + str(addrs[0]) + ':' + str(addrs[1]))

        # args terima tuple, kalau tuple isinya cuma 1 blkgnya harus kasi , klo nnt jadi list
        recv_thread = Thread(target=receive_message, args=(con,))

        recv_thread.start()
    
    for con in connections:
        con.join()

    sock.close()


def receive_message(con):
    while True:
        # max 4kb aja trs decode karena ngubah dari byte ke string
        try:
            message = con.recv(4096).decode()
        except:
            con.close()
            connections.remove(con)
            break

        if message == '':
            con.close()
            connections.remove(con)
            break
        
        print(message)

        other_connections = list(filter(lambda c: c!=con,connections))
        for connection in other_connections :
            connection.send(message.encode())


if __name__ == "__main__":
    main()