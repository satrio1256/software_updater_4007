import socket
import pickle
import os

class Client_Network:
    def __init__(self, serverIP, serverPort):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverIP = '127.0.0.1'
        self.serverPort = 7000
        self.addr = (self.serverIP, self.serverPort)
        self.replay = self.connect()

    def getReplay(self):
        return self.replay

    def connect(self):
        try:
            self.client.connect(self.addr)
            replay = self.client.recv(1024)
            replay = pickle.loads(replay)
            print(replay)
            return replay
        except:
            pass

    def send(self,data):
        try:
            data = pickle.dumps(data)
            self.client.send(data)
            return pickle.loads(self.client.recv(1024))
        except socket.error as e:
            print(e)

    def download_latest_app_definition(self):
        data = pickle.dumps("download_app_definition")
        self.client.send(data)
        if (not os.path.exists("ClientFiles/Executables")):
            os.makedirs("ClientFiles/Executables")
        downFile = open("ClientFiles/LatestVersion_on_server.csv", "wb")
        recv=True
        data = self.client.recv(1024)
        while data != b'':
            downFile.write(data)
            data = self.client.recv(1024)

        print("Latest Apps Definition Downloaded")
        downFile.close()

    def request_package(self, package_name):
        data = pickle.dumps("Request_"+package_name)
        self.client.send(data)
        if (not os.path.exists("ClientFiles/Executables")):
            os.makedirs("ClientFiles/Executables")
        downFile = open("ClientFiles/Executables/"+package_name, "wb")
        recv=True
        print("Downloading", package_name)
        data = self.client.recv(1024)
        while data != b'':
            downFile.write(data)
            data = self.client.recv(1024)
        print("Package Downloaded")
        downFile.close()


