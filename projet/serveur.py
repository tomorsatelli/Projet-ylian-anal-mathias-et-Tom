import rsa
import pyaes
from socket import socket
from threading import Thread
import random

class Serveur_Perroquet_Threaded:
    def __init__(self):
        self.pub, self.priv = rsa.newkeys(1024)
        self.host = "localhost"
        self.port = 8000
    


    def serve(self, client):
        e = str(self.pub.e).encode('utf-8')
        n = str(self.pub.n).encode('utf-8')
        client.sendall(e)
        client.sendall(n)

        
    def serve_forever(self):
        sock = socket()
        host = "10.69.225.145"
        port = 1996 
        sock.bind((host, port))
        sock.listen()
        while True:
            client, adresse = sock.accept()
            print(f"connecté à {adresse[0]} sur le port {adresse[1]}")
            self.serve(client)


def envoi(mess, client, clef):
    pass

serveur = Serveur_Perroquet_Threaded()
print(serveur.pub)
print(serveur.pub.e)
print(serveur.pub.n)
serveur.serve_forever()
