import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import json

load_dotenv(override=True)

async def debug_aggregation():
    uri = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db_name = os.getenv("DATABASE_NAME", "newmcp_database")
    client = AsyncIOMotorClient(uri)
    db = client[db_name]
    
    print(f"Connecting to {db_name}...")

    # Test Region Aggregation
    pipeline = [
        {"$addFields": {"region_str": {"$toString": "$region_id"}}},
        {"$lookup": {"from": "regions", "localField": "region_str", "foreignField": "_id", "as": "reg"}},
        # Remove unwind temporarily to see if lookup works
        {"$project": {"region_id": 1, "region_str": 1, "reg_count": {"$size": "$reg"}}}
    ]
    
    print("\n--- Region Join Test ---")
    cursor = db.sales.aggregate(pipeline)
    results = await cursor.to_list(length=5)
    for r in results:
        print(r)

    # Test Product Unwind and Join
    pipeline = [
        {"$unwind": "$product_breakdown"},
        {"$addFields": {"prod_id_str": {"$toString": "$product_breakdown.product_id"}}},
        {"$lookup": {"from": "products", "localField": "prod_id_str", "foreignField": "_id", "as": "prod"}},
        {"$project": {"prod_id_str": 1, "prod_count": {"$size": "$prod"}}}
    ]
    
    print("\n--- Product Join Test ---")
    cursor = db.sales.aggregate(pipeline)
    results = await cursor.to_list(length=5)
    for r in results:
        print(r)
        
    client.close()

if __name__ == "__main__":
    asyncio.run(debug_aggregation())
