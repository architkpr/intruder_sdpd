import socket
import threading
# import sys
import copy
import time
import datetime
import numpy as np
from firebase import firebase


# Lists to store data received by ESP32s
# Declare more lists if more ESP32s used
esp32a_data_list = []
esp32b_data_list = []
# Flags to set when in Detection Period
begin_system = 0
first_time = 1

# firebase counter
count = 0
# intruder_firebase


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
            # print("Began System on Server")
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


def pollFirebase(intruder_firebase):
    global begin_system
    global first_time

    # # Connect to database at Firebase
    # intruder_firebase = firebase.FirebaseApplication('https://intruder-291bc.firebaseio.com/')
    # print("Connected to Firebase")

    # Poll Firebase continuously for trigger from user
    while True:
        # Read value from 'Start', 'new'
        result = intruder_firebase.get('Start', 'new')
        if int(result) == 1:
            # Detection Period begins
            begin_system = 1

            if first_time:
                print("Beginning Detection Period")
                # Clear all data lists
                esp32a_data_list.clear()
                esp32b_data_list.clear()
                first_time = 0

        else:
            # Detection Period ends
            # print("Ending Detection Period")
            begin_system = 0


def setup():
    global begin_system

    server_ip = input("Enter my IP address: ")
    server_port_1 = int(input("Enter port number for server A: "))
    server_port_2 = int(input("Enter port number for server B: "))

    # Connect to database at Firebase
    intruder_firebase = firebase.FirebaseApplication('https://intruder-291bc.firebaseio.com/')
    print("Connected to Firebase")
    firebase_thread = threading.Thread(target=pollFirebase, args=(intruder_firebase, ))
    firebase_thread.start()

    # Start the servers
    server_A = threading.Thread(target=runServer, args=(server_ip, server_port_1, 1, ))
    server_A.start()

    server_B = threading.Thread(target=runServer, args=(server_ip, server_port_2, 2, ))
    server_B.start()

    time.sleep(1)
    # begin_system = 1
    # Send data lists in windows of 1000 elements
    while True:
        # print("Size: {}".format(len(esp32a_data_list)))
        if len(esp32a_data_list) == 100:
            # print("I am inside")
            # print("Size: {}".format(len(esp32a_data_list)))
            data_list = copy.deepcopy(esp32a_data_list)
            esp32a_data_list.clear()
            sig_prog_A = threading.Thread(target=displayList, args=(data_list, 1, intruder_firebase, ))
            sig_prog_A.start()
            # print("Thread started")
            # print("Size: {}".format(len(esp32a_data_list)))

        if len(esp32b_data_list) == 100:
            data_list = copy.deepcopy(esp32b_data_list)
            esp32b_data_list.clear()
            sig_prog_B = threading.Thread(target=displayList, args=(data_list, 2, intruder_firebase, ))
            sig_prog_B.start()


def displayList(data_list, server_no, intruder_firebase):
    """
    Signal Processing Function
    """
    global count

    count = count + 1
    print("\n Values obtained from ESP {} : \n {}".format(server_no, data_list))

    num = len(data_list)
    alert_sum = 0

    variance1 = [0 for x in range(num)]
    variance2 = [0 for x in range(num)]
    variance3 = [0 for x in range(num)]
    alert = [0 for x in range(num)]

    # print(np.mean(data_list))
    # print('variance', np.var(data_list))

    for i in range(num - 10):
        # print(np.var(data_list[i:i + 10]))
        variance1[i] = np.var(data_list[i:i + 10])

    for i in range(num - 20):
        variance2[i] = np.var(data_list[i:i + 20])

    for i in range(num - 5):
        variance3[i] = np.var(data_list[i:i + 5])

    for i in range(num - 20):
        if variance1[i]:
            if (variance3[i] / (2 * variance2[i]) > 1):
                alert[i] = 5
                alert_sum += alert[i]

        else:
            alert[i] = 0

    if (alert_sum / 5 > 3):
        current_time_hour = time.strftime("%H")
        current_time_min = time.strftime("%M")
        current_time_sec = time.strftime("%S")
        current_date = time.strftime("%D")
        # intruder_firebase.put('timelog', 'time for ' + str(count), 'intruder detected on ESP : ' + str(server_no) + 'at time ' + current_time_1)

        intruder_firebase.put('timelog', current_date + ' at ' + current_time_hour + ':' + current_time_min + ':' + current_time_sec, 'intruder detected on ESP : ' + str(server_no))

    # plt.plot(data_list)
    # plt.plot(variance1, color='red')
    # plt.plot(alert,  color='green')
    # plt.plot(variance3, color='blue')
    # plt.plot(variance2, color='yellow')
    # plt.show()


if __name__ == "__main__":
    setup()
