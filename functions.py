import os


# ___main menu___
def main():
    print("""\nSERVER MANAGER
    1) Show all clients
    2) Execute a command
    3) Send a unicast message
    4) Scan a network
    5) Remove a client
    6) Close the server
    """)


# ___Showing all connected clients___
def get_clients(clients):
    counter = 0
    if clients:
        print("\nUSERS:")
        print("---------------------------")
        for client in clients:
            print("{0} = {1}".format(counter, client[1]))
            counter += 1
        print("---------------------------")
    else:
        print("\n[-] No clients")


# ___Executing commands on connected clients___
def commands(clients):
    if clients:
        get_clients(clients)
        while True:
            client_id = input("\n[+] What client | [B] to go back >>> ")
            if client_id == 'b' or client_id == 'B':
                break
            client_id = int(client_id)
            client_socket = clients[client_id][0]

            while True:
                exe = input("[+] Insert a command | [B] to go back >>> ")
                if exe == 'b' or exe == 'B':
                    get_clients(clients)
                    break
                client_socket.sendall(exe.encode())

                result = client_socket.recv(2048).decode()
                print(result)

    else:
        print("\n[-] No clients")


# ___Sending a private message___
def unicast_msg(clients):
    if clients:
        get_clients(clients)
        while True:
            client_id = input("\n[+] What client | [B] to go back >>> ")
            if client_id == 'b' or client_id == 'B':
                break
            client_id = int(client_id)
            client_socket = clients[client_id][0]
            while True:
                data = input("UNICAST: | [S] to stop >>> ")  # start with 'private: <message>'
                if data == 's' or data == 'S':
                    get_clients(clients)
                    break

                client_socket.sendall(data.encode())

    else:
        print("\n[-] No clients")


# ___Finding the ipv4 address___
def ip_grab(clients):
    while True:
        ip = input("\nInsert Your FULL IPv4 Address | [C] for a client scan & [S] to close >>> ")
        if ip == 's' or ip == 'S':
            return ip
        elif ip == 'c' or ip == 'C':
            if clients:
                get_clients(clients)
                while True:
                    client_id = input("\n[+] What client | [B] to go back >>> ")
                    if client_id == 'b' or client_id == 'B':
                        break

                    client_id = int(client_id)
                    client_ip = clients[client_id][1][0]
                    # return client_ip
                    result2 = client_ip[:client_ip.rfind('.') + 1]
                    return result2
            else:
                print("\n[-] No clients")

        else:
            result = ip[:ip.rfind('.') + 1]
            return result


# ___Scanner for the Network scan (arp -a)
def scanner(ipv4, netList, lock):
    result = os.popen("ping {0} -n 1".format(ipv4)).read()
    with lock:
        if "TTL" in result:
            print(ipv4)
            netList.append(ipv4)


# ___Closing a client on the server___
def close_client(clients):
    if clients:
        get_clients(clients)
        while clients:
            client_id = input("\n[+] What client? | [B] to go back >>> ")
            if client_id == 'b' or client_id == 'B':
                break

            client_id = int(client_id)
            client_socket = clients[client_id][0]
            client_ip = clients[client_id][1]

            leave = input("\n[+] Are you sure? [Y] | [N] >>> ")
            if leave == 'n' or leave == 'N':
                get_clients(clients)


            elif leave == 'y' or leave == 'Y':
                client_socket.sendall(leave.encode())
                clients.remove([client_socket, client_ip])
                get_clients(clients)


    else:
        print("\n[-] No clients")


# ___Server shutdown___
def shutdown(clients, server):
    if clients:
        print("\n[-] You need to remove all clients before closing the server")

    else:
        server.close()
        print("\n_________________________SERVER_SOCKET_CLOSED_________________________")
        exit(0)
