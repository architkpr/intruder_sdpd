import socket
import time


def testingRSSI():
    server_ip = input("Enter server IP address: ")
    server_port = int(input("Enter port number for server: "))

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = socket.getaddrinfo(server_ip, server_port)
    client.connect(address[0][4])

    print("connected. \n")
    while True:
        # Wait for 10ms
        time.sleep(0.01)
        client.send(b'-50\x00\x00\x00')
        print((client.recv(1024)).decode())


if __name__ == '__main__':
    testingRSSI()
