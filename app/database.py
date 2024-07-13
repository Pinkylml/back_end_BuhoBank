from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)

try:
    client.admin.command('ping')
    print("Connected to MongoDB")
except ConnectionFailure:
    print("Server not available")

database = client.BuhoBanco
customer_collection = database.get_collection("Clientes")
account_collection = database.get_collection("CuentasBancarias")
