import socket
import sys

#
def send_cmds(s, conn):
    print("[Ctrl]+[C] for interrupte the connection") 
    print("$: ", end="")
    while True:
        try:
            cmd = input()
            if len(cmd) > 0:
                conn.sendall(cmd.encode())
                data = conn.recv(4096)
                print(data.decode("utf-8"), end="")
        except KeyboardInterrupt:
            print("something went wrong")
            print(KeyboardInterrupt.__cause__)
            conn.close()
            s.close()
            sys.exit()


def server(address):
    try:
        s = socket.socket()
        s.bind(address)
        s.listen()
        print("server started")
        print("waiting for a connection...")
    except Exception as e:
        print("something went wrong: ")
        print(e.__cause__)
        result = input("do you want to restart the connection? [Y/n]")
        if result == 'y' or result == 'Y':
            print(f"connection restarted: {address}")
            server(address)
        else:
            print("connection terminated")
            sys.exit()
    conn, client_addr = s.accept()
    print(f"connected on {address}")
    send_cmds(s, conn)
    
    
if __name__ == "__main__":
    try:
        host = "192.168.1.7"
        port = 4444
    except socket.error as e:
        if socket.error.errno == 98:
            host = "127.0.0.1"
            port = 1234
    server((host, port))             