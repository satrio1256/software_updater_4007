import socket
from _thread import *
import pickle


serverIP ='127.0.0.1'
serverPort = 7000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((serverIP, serverPort))
except socket.error as e:
    str(e)

sock.listen(5)

def SendVersion(conn):
    fileServer = open('ServerFiles/LatestVersion.csv', "rb",)
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
        print("File sent")
    fileServer.close()
    conn.close()

def SendExecutables(conn, package_name):
    fileServer = open('ServerFiles/Executables/'+package_name, "rb",)
    try:
        byte = fileServer.read(1024)
        while byte != b'':
            conn.send(byte)
            byte = fileServer.read(1024)
            if byte == b'':
                conn.send(byte)
                break
    finally:
        print(package_name, "sent")
    fileServer.close()
    conn.close()

def clientProcess(conn):
    conn.send(pickle.dumps("Connected to Server"))

    data= ""
    while True:
        try:
            data = conn.recv(1024)
            data = pickle.loads(data)
            print("Request from Client:", data)
            if data == "download_app_definition":
                print("Sending Files")
                SendVersion(conn)
            elif "Request" in data:
                print("Sending Executables")
                package_name = data.split("_", 1)[-1]
                SendExecutables(conn, package_name)
            else:
                conn.send(pickle.dumps("Data Received"))
        except:
            break
    conn.close()
    print("Client disconnected")
    print("---")

while True:
    conn, addr = sock.accept()
    print("Connected with:", addr)

    start_new_thread(clientProcess, (conn, ))
