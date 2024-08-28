from kafka import KafkaConsumer, consumer
from time import sleep
import json
from bson import json_util

import pymongo
from pymongo import MongoClient

import configparser
config = configparser.ConfigParser()
config.read('consumer.ini')

mongodbUri  = config['DEFAULT']['mongodbUri']
database  = config['DEFAULT']['database']
broker  = config['DEFAULT']['broker']
topicName  = config['DEFAULT']['topicName']


class MessageConsumer:
    broker = broker
    topic = topicName
    logger = None

    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic

    def activate_listener(self):
        consumer = KafkaConsumer(bootstrap_servers=self.broker,
                                     auto_offset_reset='latest',
                                     value_deserializer=lambda m: json.loads(m.decode('utf-8')))

        consumer.subscribe(self.topic)
        print("consumer is listening....")
        try:
            for message in consumer:
                print(message.value)
                myCollection = dbConnections('DeviceData')
                doc = json.loads(message.value)
                print(type(doc))
                jsn = {"Battery_Level": doc['Battery_Level'],
                        "Device_Id":doc['Device_Id'],
                        "First_Sensor_temperature":doc['First_Sensor_temperature'] ,
                        "Route_From":doc['Route_From'],
                        "Route_To":doc['Route_To']
                      }                      
                myCollection.insert_one(jsn)
                #consumer.commit()
        except KeyboardInterrupt:
            print("Aborted by user...")
        finally:
            consumer.close()
    
    
def dbConnections(colName : str):
    CONNECTION_STRING = mongodbUri
    client = MongoClient(CONNECTION_STRING)
    myDatabase = client[database]
    myCollection = myDatabase[colName]
    return myCollection


#Running multiple consumers
broker = broker
topic = topicName

consumer1 = MessageConsumer(broker,topic)
consumer1.activate_listener()

