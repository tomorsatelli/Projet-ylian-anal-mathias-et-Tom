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
        port = 2014
        self.sock.connect((host, port))
        print(f"connecté à {host} sur le port {port}")
        rep = self.sock.recv(2048)
        print("reçu ",rep)
        self.sock.sendall("ok".encode('utf-8'))
        e = int(rep.decode('utf-8'))
        rep = self.sock.recv(2048)
        print("reçu ",rep)
        n = int(rep.decode('utf-8'))
        print(e)
        print(n)
        pub = rsa.PublicKey(n, e)
        clef_codee = rsa.encrypt(self.clef, pub)
        print(clef_codee)
        self.sock.sendall(clef_codee)
        print(self.clef)
        message = self.reception()
        print(message)   #reception du serveur 'bonjour du serveur'
        self.envoi('ok')
        self.connection()

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
        return message.decode()

    def connection(self):
        reponse = self.reception()
        print(reponse)
        self.envoi('Oui')
        print(self.reception())
        nom = input('nouveau Nom ?')
        self.envoi(nom)
        print(self.reception())
        prenom = input('Quel est votre prénom ?')
        self.envoi(prenom)
        print(self.reception())
        mot_de_passe = input('Choissiez un mot de passe.')
        self.envoi(mot_de_passe)
        montant = (input('Choisissez un montant'))
        self.envoi(str(montant))
    

client = Client()




