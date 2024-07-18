from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

MONGO_DETAILS = "mongodb+srv://jeffcan1995:zRlRxsF5sRbZiL5O@buhobankcluster.ei1v8qq.mongodb.net/?retryWrites=true&w=majority&appName=BuhoBankCluster"

client = AsyncIOMotorClient(MONGO_DETAILS)

try:
    client.admin.command('ping')
    print("Connected to MongoDB")
except ConnectionFailure:
    print("Server not available")

database = client.BuhoBanco
customer_collection = database.get_collection("Clientes")
account_collection = database.get_collection("CuentasBancarias")
code_verify_collection= database.get_collection("CodigosVerificación")
