import socket
import threading
import copy

# Lists to store data received by ESP32s
# Declare more lists if more ESP32s used
esp32a_data_list = []
esp32b_data_list = []


def runServer(server_ip, server_port, server_no):
    """
    Start a server to receive data from the ESP32 modules
    :param server_ip: IP address of Raspberry PI
    :param server_port: Port number to which the ESP32 must connect
    :param server_no: Identifier for which ESP32 is connected
    """

    # Create a socket at given IP and port and make the server bind to it
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = socket.getaddrinfo(server_ip, server_port)
    server.bind(address[0][4])
    server.listen(5)

    print("\nServer Started at {}:{}\n".format(server_ip, server_port))

    conn, addr = server.accept()
    print("\nConnection Established at {}:{}\n".format(server_ip, server_port))

    while True:
        rssi_value = (conn.recv(1024)).decode()

        # Data received is a string of the form - '-25\x00\x00\...'
        # Split data to store only RSSI information
        if server_no is 1:
            esp32a_data_list.append(int(rssi_value.rstrip('\x00')))
            # print(esp32a_data_list)
        else:
            esp32b_data_list.append(int(rssi_value.rstrip('\x00')))

        # Reply acknowledgement to ESP32
        conn.send(b'1')

    # No more data left to send
    print("\nClosing Connection at {}:{}\n".format(server_ip, server_port))
    conn.close()

    server.close()
    print("\nServer Closed at {}:{}\n".format(server_ip, server_port))


def setup():

    server_ip = input("Enter my IP address: ")
    server_port_1 = int(input("Enter port number for server A: "))
    server_port_2 = int(input("Enter port number for server B: "))

    # Start the servers
    server_A = threading.Thread(target=runServer, args=(server_ip, server_port_1, 1, ))
    server_A.start()

    server_B = threading.Thread(target=runServer, args=(server_ip, server_port_2, 2, ))
    server_B.start()

    while True:
        if len(esp32a_data_list) == 30:
            data_list = copy.deepcopy(esp32a_data_list)
            sig_prog_A = threading.Thread(target=displayList, args=(data_list, 1, ))
            sig_prog_A.start()
            esp32a_data_list.clear()
        if len(esp32b_data_list) == 30:
            data_list = copy.deepcopy(esp32b_data_list)
            sig_prog_B = threading.Thread(target=displayList, args=(data_list, 2, ))
            sig_prog_B.start()
            esp32b_data_list.clear()


def displayList(data_list, server_no):
    """
    Signal Processing Function
    """
    print("\nSignal Processing Function begins here\n")
    print("Data received from {}: {}".format(server_no, data_list))


if __name__ == "__main__":
    setup()
