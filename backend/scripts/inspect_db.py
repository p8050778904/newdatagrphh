import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv(override=True)

async def inspect():
    uri = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db_name = os.getenv("DATABASE_NAME", "newmcp_database")
    client = AsyncIOMotorClient(uri)
    db = client[db_name]
    
    collections = ["regions", "products", "employees", "sales"]
    for coll in collections:
        doc = await db[coll].find_one()
        print(f"\n--- Collection: {coll} ---")
        if doc:
            print(doc)
        else:
            print("EMPTY COLLECTION")
            
    client.close()

if __name__ == "__main__":
    asyncio.run(inspect())
