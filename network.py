import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverIP = '192.168.1.3'
        self.serverPort = 5555
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
    def download(self):
        data = pickle.dumps("download")
        self.client.send(data)

        downFile = open("LatestVersionnDownload.txt", "wb")
        recv =True
        data = self.client.recv(1024)
        while data != b'':
            downFile.write(data)
            data = self.client.recv(1024)

        print("data berhasil di didonload")
        downFile.close()

n=Network()
n.download()


