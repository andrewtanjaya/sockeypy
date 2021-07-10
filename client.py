import socket
from threading import Thread

def main():
    print('Client Started')
    con = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        con.connect(('127.0.0.1',8000))
    except:
        print('Connection Failed')
        return
    
    print('Client Connected')

    recv_thread = Thread(target=receive_message, args=(con,))
    send_thread = Thread(target=send_message, args=(con,))

    recv_thread.start()
    send_thread.start()

    recv_thread.join()
    send_thread.join()
    
    print('Connection stopped')

def receive_message(con):
    while True:
        # max 4kb aja trs decode karena ngubah dari byte ke string
        try:
            message = con.recv(4096).decode()
        except:
            con.close()
            break

        if message == '':
            con.close()
            break
        
        print(message)

def send_message(con):
    while True:
        message = raw_input()
        try:
            con.send(message.encode())
        except:
            con.close()
            break


if __name__ == "__main__":
    main()