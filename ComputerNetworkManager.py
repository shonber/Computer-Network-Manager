# ___Modules__
from socket import *
import threading
from functions import main, get_clients, commands, ip_grab, scanner, close_client, unicast_msg, shutdown


# ___Server class___
class ComputerNetworkManager(object):
    def __init__(self, HOST, PORT):
        # ___Server creation___
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen(50)

        # ___Lists___
        self.clients = []
        self.Threads = []

    # ___A function for accepting clients__
    def accept_client(self, server):
        while True:
            try:
                self.client, addr = server.accept()
                self.clients.append([self.client, addr])
            except:
                pass

    # ___infinite function loop for options___
    def __call__(self, *args, **kwargs):
        while True:

            # ___Threads, so more than 1 user can connect to the server___
            t = threading.Thread(target=self.accept_client, args=(self.server,))
            t.start()

            main()
            try:
                option = int(input("[+] Insert an option > "))
            except:
                print("\n[-] Numbers only")

            # ___Showing all connected clients___
            if option == 1:
                get_clients(self.clients)

            # ___Client command execute___
            elif option == 2:
                try:
                    commands(self.clients)
                except OSError as f:
                    print(f)

            elif option == 3:
                unicast_msg(self.clients)  # start with 'private: <message>'

            # ___Network scanner___
            elif option == 4:
                while True:
                    my_ip = ip_grab(self.clients)

                    if my_ip == 's' or my_ip == 'S':
                        break
                    # Network = my_ip[:my_ip.rfind('.')+1]

                    netList = []
                    lock = threading.Lock()

                    for i in range(255):
                        test = str(my_ip)+str(i)
                        t2 = threading.Thread(target=scanner, args=(test, netList, lock, ))
                        t2.start()
                        self.Threads.append(t2)

                    for thread in self.Threads:
                        thread.join()

                    print("\nThese are the IP Address's: {0}".format(netList))
            # ___Client remover___
            elif option == 5:
                close_client(self.clients)

            # ___Server shutdown___
            elif option == 6:
                shutdown(self.clients, self.server)

            # ___Only 6 options no more___
            elif option >= 7:
                print("\n[-] No such an option")


server = ComputerNetworkManager("", 3434)
server()
