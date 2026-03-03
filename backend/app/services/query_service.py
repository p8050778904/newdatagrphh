from app.database.mongodb_connector import get_database
from typing import List, Dict, Any

async def execute_aggregation_pipeline(collection_name: str, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    db = get_database()
    collection = db[collection_name]
    
    # Security: Validate pipeline doesn't contain destructive operations (though $group/$match/etc are safe)
    # This is a simple check; in production, use a more robust validation.
    forbidden = ["$out", "$merge"]
    for stage in pipeline:
        if any(key in stage for key in forbidden):
            raise ValueError("Forbidden aggregation stage detected.")

    cursor = collection.aggregate(pipeline)
    results = await cursor.to_list(length=1000)
    
    # Convert ObjectIDs to strings for JSON serialization
    for doc in results:
        for k, v in doc.items():
            if hasattr(v, "__str__") and "ObjectId" in str(type(v)):
                doc[k] = str(v)
                
    return results
