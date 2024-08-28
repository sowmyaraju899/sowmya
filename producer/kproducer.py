from kafka import KafkaProducer
import json

import socket

import configparser
config = configparser.ConfigParser()
config.read('producer.ini')

broker  = config['DEFAULT']['broker']
topicName  = config['DEFAULT']['topicName']
serverHostName  = config['DEFAULT']['serverHostName']
serverPort  = config['DEFAULT']['serverPort']

class MessageProducer:
    broker = ""
    topic = ""
    producer = None

    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.broker,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        acks='all',
        retries = 3)


    def send_msg(self, msg):
        print("sending message...")
        try:
            future = self.producer.send(self.topic,msg)
            self.producer.flush()
            future.get(timeout=60)
            print("message sent successfully...")
            return {'status_code':200, 'error':None}
        except Exception as ex:
            return ex


broker = broker #'localhost:9092'
topic = topicName
message_producer = MessageProducer(broker,topic)
 
host = socket.gethostbyname(serverHostName)  #"0.0.0.0" #socket.gethostname()  
print(host)
port = int(serverPort)   

client_socket = socket.socket()  
client_socket.connect((host, port))

message = "get Data" 
 
while message.lower().strip() != 'exit':
    client_socket.send(message.encode()) 
    data = client_socket.recv(1024).decode() 
    print('Received from server: ' + data)  
    resp = message_producer.send_msg(data)
    message = "get Data"  

client_socket.close()  # close the connection

