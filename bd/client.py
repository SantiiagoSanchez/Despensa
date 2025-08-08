from pymongo import MongoClient

MONGO_URI = "mongodb+srv://santi2005531:JKTNBYJ2xwTgcaDj@despensacluster.s86ambp.mongodb.net/despensa?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["despensa"]  