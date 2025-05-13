import rsa
import pyaes
from socket import socket
from threading import Thread
import random
from mysql.connector import connect
from hashlib import sha256
import base64

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
            print(client.recv(1024).decode('utf-8'))
            client.sendall(n)
            print("n envoyé")
            clef_codee = client.recv(2048)
            print(clef_codee)
            clef = rsa.decrypt(clef_codee, self.priv)
            return clef

        def connection(client):
            cnx = connect(user='coulomb', password='coulomb', host='localhost', database='projet')
            cursor = cnx.cursor()
            self.envoi('Nouvel utilisateur?', client, clef)
            reponse = self.reception(client, clef)
            print(reponse)
            if reponse == 'Oui': 
                self.envoi("Entrer votre nom", client, clef)
                nom = self.reception(client, clef)
                print(nom)
                self.envoi("Entrer votre prénom", client, clef)
                prenom = self.reception(client, clef)
                print(prenom)
                self.envoi("Créer un mot de passe", client, clef)
                mdp = self.reception(client, clef)
                print(mdp)
                hash1 = sha256(mdp.encode('utf-8'))
                print(hash1)
                print(hash1.digest())
                sha = base64.standard_b64encode(hash1.digest()).decode('utf-8')
                requete = f'INSERT INTO Utilisateurs (NOM, PRENOM, MOT_DE_PASSE) VALUES("{nom}", "{prenom}", {hash1.digest()})'
                print(requete)
                cursor.execute(requete)
                cnx.commit()
                resultat = cursor.fetchall()
                print(resultat)
                requete = "select * from Utilisateurs"
                cursor.execute(requete)
                resulat = cursor.fetchall()
                cnx.commit()
                print(resulat)

        clef = echange(client)
        print(clef)
        self.envoi('Bonjour du serveur', client, clef)
        print(self.reception(client, clef))
        connection(client)
        
            
        
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
        return message.decode('utf-8')




serveur = Serveur_Perroquet_Threaded()
serveur.serve_forever()
