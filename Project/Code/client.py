import pickle
import random
import socket
import ast
from multiprocessing import Process


host = '127.0.0.1'
ServerIP = ('127.0.0.1', 9999)
port = random.randint(10000, 11000)
Client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Client.bind((host, port))
ID=input("Enter ID:")
Client.sendto(f"ID {ID}".encode("utf-8"), ServerIP)

def List():
    while True:
        Messege, IP = Client.recvfrom(1024)
        if Messege.decode("utf-8").startswith("List "):
            print(str(Messege.decode("utf-8")))
            command= input("Do you want to send massege? (y:yes/n:no/q:quit)")
            if command.upper()=="Y":
                while True:
                    peer=input("Enter Peer ID: ")
                    if peer!=ID:
                        Client.sendto(f"Peer {peer}".encode("utf-8"),ServerIP)
                        ClientWork()
                        break
                    else:
                        continue
            elif command.upper()=="N":
                continue
            elif command.upper()=="Q":
                Client.sendto(f"Quit {ID}".encode("utf-8"),ServerIP)
                exit(1)
            else:
                print("invalid input ")
                continue
        if Messege.decode("utf-8").startswith("Message "):
            Split=Messege.decode("utf-8").split(" ",1)
            print(Split[1])

def ClientWork():
    while True:
        Messege, IP = Client.recvfrom(1024)
        if Messege.decode("utf-8").startswith("Peer "):
            Split=Messege.decode("utf-8").split(" ",1)
            msg=input("Enter Message to send\n>")
            Client.sendto(f"Message {msg}".encode("utf-8"),ast.literal_eval(Split[1]))
            Client.sendto(f"ID2 ".encode("utf-8"), ServerIP)
        if Messege.decode("utf-8").startswith("NoPeer"):
            print("There is no such client")
        break

#if __name__ == '__main__':
p1=Process(target=List())
p1.start()