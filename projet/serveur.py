import rsa
import pyaes
from socket import socket
from threading import Thread
import random

class Serveur_Perroquet_Threaded:
    def __init__(self):
        self.pub, self.priv = rsa.newkeys(2048)
        host = "localhost"
        port = 8000

    def serve(client):
        