from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from pymongo import IndexModel, ASCENDING


MONGO_DETAILS = "mongodb+srv://buhobanco:cB5W7tVdZxuUQYWN@buhobanco.tpw58ga.mongodb.net/?retryWrites=true&w=majority&appName=BuhoBanco"

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

async def create_ttl_index():
    try:
        index = IndexModel([("expiresAt", ASCENDING)], expireAfterSeconds=0)
        await reset_verify_colletion.create_indexes([index])
        print("TTL Index created successfully")
    except Exception as e:
        print(f"Failed to create TTL index: {e}")

async def setup_database():
    await create_ttl_index()