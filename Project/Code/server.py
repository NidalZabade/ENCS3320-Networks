import socket
from multiprocessing import Process

host = '127.0.0.1'
port = 9999
Server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Server.bind((host, port))
Clients = {}
IDs=[]


def List():
    while True:
        Message, ClientIP = Server.recvfrom(1024)
        if Message.decode("utf-8").startswith("ID "):
            Split=Message.decode("utf-8").split(" ",1)
            Clients[Split[1]] = ClientIP
            IDs.append(Split[1])
            print(Clients)
            if Split[1] !=None:
                for ip in Clients:
                    Server.sendto(f"List {str(IDs)}".encode("utf-8"), Clients.get(ip))
        if Message.decode("utf-8").startswith("Peer "):
            Split = Message.decode("utf-8").split(" ", 1)
            if Split[1] in IDs:
                Server.sendto(f"Peer {Clients.get(Split[1])}".encode("utf-8"),ClientIP)
            else:
                Server.sendto(f"NoPeer".encode("utf-8"),ClientIP)
        if Message.decode("utf-8").startswith("Quit "):
            Split = Message.decode("utf-8").split(" ", 1)
            del Clients[Split[1]]
            IDs.remove(Split[1])
            for ip in Clients:
                Server.sendto(f"List {str(IDs)}".encode("utf-8"), Clients.get(ip))
        if Message.decode("utf-8").startswith("ID2 "):
            for ip in Clients:
                Server.sendto(f"List {str(IDs)}".encode("utf-8"), Clients.get(ip))

# if __name__ == '__main__':
p1=Process(target=List())
p1.start()
print(Clients)