from socket import socket
import pyaes
import rsa
from random import randint


    

class Client:
    def __init__(self):
        nombres = [randint(0, 255) for _ in range(32)]
        self.clef = bytes(nombres)
        self.sock = socket()
        host = "10.69.225.145"
        port = 2013
        self.sock.connect((host, port))
        print(f"connecté à {host} sur le port {port}")
        rep = self.sock.recv(2048)
        print("reçu ",rep)
        e = int(rep.decode('utf-8'))
        rep = self.sock.recv(2048)
        print("reçu ",rep)
        n = int(rep.decode('utf-8'))
        print(e)
        print(n)
        pub = rsa.PublicKey(n, e)
        clef_codee = rsa.encrypt(self.clef, pub)
        self.sock.sendall(clef_codee)
        print(self.clef)
        message = self.reception()
        print(message)   #reception du serveur 'bonjour du serveur'
        self.serv()

    def serv(self):    
        while True:
            message = input()
            self.envoi(message)
            reponse = self.reception()
            print(reponse)
    
    def clef_aes(self):
        "generation d'une clef aes de 32 octets"
        self.nombres = [randint(0, 255) for _ in range(32)]
        self.clef = bytes(nombres)
        print(self.clef)
        reponse = self.reception()
        print(reponse)
    
    def envoi(self, mess):
        aes = pyaes.AESModeOfOperationCTR(self.clef)
        code = aes.encrypt(mess.encode('utf-8'))
        self.sock.sendall(code)
        
    
    def reception(self):
        aes = pyaes.AESModeOfOperationCTR(self.clef)
        code = self.sock.recv(2048)
        message = aes.decrypt(code)
        print(message)
        return message.decode()
client = Client()
