import rsa
import pyaes
from socket import socket
from threading import Thread
import random

class Serveur_Perroquet_Threaded:
    def __init__(self):
        self.pub, self.priv = rsa.newkeys(1024)
        self.host = "localhost"
        


    def serve(self, client):
        def echange(client):
            e = str(self.pub.e).encode('utf-8')
            n = str(self.pub.n).encode('utf-8')
            client.sendall(e)
            print("e envoyé")
            client.sendall(n)
            print("n envoyé")
            clef_codee = client.recv(2048)
            clef = rsa.decrypt(clef_codee, self.priv)
            return clef     
        clef = echange(client)
        print(clef)
        self.envoi('Bonjour du serveur', client, clef)
        while True:
            message = self.reception(client, clef)
            print(message)
            self.envoi(message, client, clef)
            
        
    def serve_forever(self):
        sock = socket()
        host = "10.69.225.145"
        port = 2013
        sock.bind((host, port))
        sock.listen()
        while True:
            client, adresse = sock.accept()
            print(f"connecté à {adresse[0]} sur le port {adresse[1]}")
            Thread(target=self.serve, args=[client]).start()


    def envoi(self, mess, client, clef):
        aes = pyaes.AESModeOfOperationCTR(clef)
        code = aes.encrypt(mess.encode('utf-8'))
        client.sendall(code)

    def reception(self, client, clef):
        aes = pyaes.AESModeOfOperationCTR(clef)
        code = client.recv(2048)
        message = aes.decrypt(code)
        print(message)
        return message.decode('utf-8')




serveur = Serveur_Perroquet_Threaded()
serveur.serve_forever()
