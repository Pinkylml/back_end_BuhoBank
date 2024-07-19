from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

MONGO_DETAILS = "mongodb+srv://jeanasencio2000:passjean20001207@buhobanco.t77tcy2.mongodb.net/?retryWrites=true&w=majority&appName=BuhoBanco"

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
reset_verify_colletion= database.get_collection("CodigosVerificaciónReseteo")
