import socket
import time
import json
import requests
from random import randint

import configparser
config = configparser.ConfigParser()
config.read('server.ini')

serverHostName  = config['DEFAULT']['serverHostName']
serverPort  = config['DEFAULT']['serverPort']


def server_program():
    host = socket.gethostbyname(serverHostName) #'0.0.0.0' #socket.gethostname()
    port = int(serverPort)  

    server_socket = socket.socket() 
    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept()      
    print("Connection from: " + str(address))
    
    while True:
        time.sleep(5)
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user: " + str(data))
        data = makeData()
        conn.send(data)  
        
    conn.close()

def makeData():
    datas= {
        "Battery_Level": randint(1.00, 5.00),
        "Device_Id": randint(1000000000 , 1999999999),
        "First_Sensor_temperature": randint(1.00, 30.00) ,
        "Route_From": "Hyderabad, India",
        "Route_To": "Louisville, USA"
    }
    userdata = (json.dumps(datas)+"\n").encode('utf-8')
    return userdata


if __name__ == '__main__':
    server_program()