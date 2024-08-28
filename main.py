from codecs import charmap_encode
from fastapi import FastAPI, Request

import pymongo
from pymongo import MongoClient

from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import configparser
config = configparser.ConfigParser()
config.read('properties.ini')

corsOrigin = config['DEFAULT']['corsOrigin']
mongodbUri  = config['DEFAULT']['mongodbUri']
database  = config['DEFAULT']['database']
deviceDataCollection  = config['DEFAULT']['deviceDataCollection']
shipmentCollection  = config['DEFAULT']['shipmentCollection']
usersCollection  = config['DEFAULT']['usersCollection']


app = FastAPI()
app.mount("/static",StaticFiles(directory="static"), name="static")

templates =Jinja2Templates(directory="templates")
list_of_usernames=list()
origins = [ corsOrigin ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class user(BaseModel):
    fullname: str
    username: str
    email:str
    phone: int
    password: str
    
class userLogin(BaseModel):
    username: str
    password: str    

class shipment(BaseModel):
    shipmentNumber: str
    poNumber: str   
    containerNumber : str
    deliveryNumber: str
    expDelDate: str
    ndcNumber: str
    routerDetails: str
    batchIDNumber: str
    goodsType: str
    serialNumGoods: str
    device: str
    shipmentDescription : str


@app.get("/",response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("landingpage.html",{"request":request})


@app.get("/login",response_class=HTMLResponse)
async def flogin(request: Request):
    return templates.TemplateResponse("login.html",{"request":request})


@app.get("/register",response_class=HTMLResponse)
async def fregister(request: Request):
    return templates.TemplateResponse("registration.html",{"request":request})



@app.get("/dashboard",response_class=HTMLResponse)
async def fdashboard(request: Request):
    return templates.TemplateResponse("dashboard.html",{"request":request})



@app.get("/shipment",response_class=HTMLResponse)
async def fshipment(request: Request):
    return templates.TemplateResponse("shipment.html",{"request":request})



@app.get("/devicedata",response_class=HTMLResponse)
async def fdevicedata(request: Request):
    return templates.TemplateResponse("devicedatastream.html",{"request":request})


#login
@app.post("/login")
async def login(request: userLogin):
    userName = request.username
    password = request.password    
    myCollection = dbConnections(usersCollection)
    data = myCollection.find({"username": userName })
    results = list(data)
    if len(results)==0:
        return "User not found"
    else:
        userData = myCollection.find({"username": userName , "password" : password})
        userResults = list(userData)
        if len(userResults)==0:
            print("no records")
            return "false"
        else: 
            print("record found")
            return "true"
    
    

# register
@app.post("/register")
async def register(request: user):

    myCollection = dbConnections(usersCollection)
    doc = {"fullname" : request.fullname, 
            "username" : request.username, 
            "email" : request.email, 
            "phone" : request.phone, 
            "password" : request.password
        }
    myCollection.insert_one(doc)
    
    return "success"


# saveShipment
@app.post("/saveShipment")
async def saveShipment(request: shipment):

    myCollection = dbConnections(shipmentCollection)
    doc = {
            "shipmentNumber": request.shipmentNumber,
            "poNumber": request.poNumber,  
            "containerNumber" : request.containerNumber,
            "deliveryNumber": request.deliveryNumber,
            "expDelDate": request.expDelDate,
            "ndcNumber": request.ndcNumber,
            "routerDetails": request.routerDetails,
            "batchIDNumber": request.batchIDNumber,
            "goodsType": request.goodsType,
            "serialNumGoods": request.serialNumGoods,
            "device": request.device,
            "shipmentDescription" : request.shipmentDescription
          }
    myCollection.insert_one(doc)
    
    return "success"




#Device Data Stream
@app.get("/DeviceDataStream")
async def deviceDatastream():    
    myCollection = dbConnections(deviceDataCollection)
    data = myCollection.find({},{"_id":0})
    results = list(data)
    return results 
    



def dbConnections(colName : str):
    CONNECTION_STRING = mongodbUri
    client = MongoClient(CONNECTION_STRING)
    myDatabase = client[database]
    myCollection = myDatabase[colName]
    return myCollection



