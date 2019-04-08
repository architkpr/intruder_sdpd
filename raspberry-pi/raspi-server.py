import socket
import threading
import sys
import copy
import time
from firebase import firebase

# Lists to store data received by ESP32s
# Declare more lists if more ESP32s used
esp32a_data_list = []
esp32b_data_list = []
# Flag to set when in Detection Period
begin_system = 0


def runServer(server_ip, server_port, server_no):
    global begin_system
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

        # Check if in Detection Period
        if begin_system is 1:
            print("Began System on Server")
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


def pollFirebase():
    global begin_system

    # Connect to database at Firebase
    intruder_firebase = firebase.FirebaseApplication('https://intruder-291bc.firebaseio.com/')
    print("Connected to Firebase")

    # Poll Firebase continuously for trigger from user
    while True:
        # Read value from 'Start', 'new'
        result = intruder_firebase.get('Start', 'new')
        if int(result) == 1:
            # Detection Period begins
            begin_system = 1
            # print("Beginning Detection Period")
            # Clear all data lists
            esp32a_data_list.clear()
            esp32b_data_list.clear()

        else:
            # Detection Period ends
            # print("Ending Detection Period")
            begin_system = 0


def setup():
    global begin_system

    server_ip = input("Enter my IP address: ")
    server_port_1 = int(input("Enter port number for server A: "))
    server_port_2 = int(input("Enter port number for server B: "))

    # Connect to Firebase and poll for triggers
    firebase_thread = threading.Thread(target=pollFirebase)
    firebase_thread.start()

    # Start the servers
    server_A = threading.Thread(target=runServer, args=(server_ip, server_port_1, 1, ))
    server_A.start()

    server_B = threading.Thread(target=runServer, args=(server_ip, server_port_2, 2, ))
    server_B.start()

    time.sleep(1)
    # begin_system = 1
    # Send data lists in windows of 100 elements
    while True:
        # print("Size: {}".format(len(esp32a_data_list)))
        if len(esp32a_data_list) == 100:
            print("I am inside")
            print("Size: {}".format(len(esp32a_data_list)))
            data_list = copy.deepcopy(esp32a_data_list)
            esp32a_data_list.clear()
            sig_prog_A = threading.Thread(target=displayList, args=(data_list, 1, ))
            sig_prog_A.start()
            print("Thread started")

        if len(esp32b_data_list) == 100:
            data_list = copy.deepcopy(esp32b_data_list)
            esp32b_data_list.clear()
            sig_prog_B = threading.Thread(target=displayList, args=(data_list, 2, ))
            sig_prog_B.start()


def displayList(data_list, server_no):
    """
    Signal Processing Function
    """
    print("\nSignal Processing Function begins here\n")
    print("Data received from {}: {}".format(server_no, data_list))
    # sys.exit()
    # print("THREAD NOT AVAILABLE")

    # # connect to firebase

    # # write value to timelog
    # resultPut = myfirebase.put('timelog', '10:40', 'no intruderrrrr')

    # print(result)


if __name__ == "__main__":
    setup()
