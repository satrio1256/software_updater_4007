import socket
from _thread import *
import pickle


serverIP ='192.168.1.3'
serverPort = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((serverIP, serverPort))
except socket.error as e:
    str(e)

sock.listen(5)

def SendVersion(conn):
    fileServer = open('LatestVersion.txt', "rb",)
    try:
        byte = fileServer.read(1024)
        while byte != b'':
            conn.send(byte)

            byte = fileServer.read(1024)

            if byte ==b'':
                #print(byte)
                conn.send(byte)
                break
    finally:
        print("selesai kirim")
    fileServer.close()
    conn.close()

def clientProcess(conn):
    conn.send(pickle.dumps("Terhubung dengan server"))

    data= ""
    while True:
        try:
            data = conn.recv(1024)
            data = pickle.loads(data)
            print("Data dari client:", data)
            if data == "download":
                print("kirim file")
                SendVersion(conn)
            else:
                conn.send(pickle.dumps("Data diterima"))
        except:
            break
    conn.close()
    print("Client disconnect")

while True:
    conn, addr = sock.accept()
    print("Terhubung dengan:" ,addr)

    start_new_thread(clientProcess, (conn, ))
