import os
import json
import mcp.server.fastmcp as fastmcp_mod
from mcp.server.fastmcp import FastMCP
from openai import AsyncOpenAI
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any, Optional

# Initialize FastMCP server
mcp = FastMCP("Dynamic Analytics MCP")

# Global DB state
db_client = None
db = None

# Initialize OpenAI Client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@mcp.tool()
async def connect_to_database() -> str:
    """
    Connects to MongoDB using environment variables and stores the connection.
    """
    global db_client, db
    try:
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "newmcp_database")
        db_client = AsyncIOMotorClient(mongodb_url)
        db = db_client[database_name]
        return f"Connected to MongoDB database: {database_name}"
    except Exception as e:
        return f"Error connecting to database: {str(e)}"

@mcp.tool()
async def list_collections() -> List[str]:
    """
    Returns all available MongoDB collections dynamically.
    """
    global db
    if db is None:
        await connect_to_database()
    try:
        collections = await db.list_collection_names()
        return collections
    except Exception as e:
        return [f"Error listing collections: {str(e)}"]

@mcp.tool()
async def get_collection_schema(collection_name: str) -> Dict[str, Any]:
    """
    Infers schema structure from a collection by sampling documents.
    """
    global db
    if db is None:
        await connect_to_database()
    try:
        sample_docs = await db[collection_name].find().limit(5).to_list(length=5)
        if not sample_docs:
            return {"error": f"Collection '{collection_name}' is empty."}
        
        schema = {}
        for doc in sample_docs:
            for key, value in doc.items():
                if key not in schema:
                    schema[key] = str(type(value).__name__)
        
        return {"collection": collection_name, "fields": schema}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def generate_query(user_prompt: str) -> Dict[str, Any]:
    """
    Accepts natural language input, analyzes schemas, and generates a MongoDB query.
    This tool performs 'chaining' by internal retrieval of collections and schemas.
    """
    try:
        # 1. Get available collections
        collections = await list_collections()
        
        # 2. Get schemas for context
        schemas = []
        for coll in collections:
            schema = await get_collection_schema(coll)
            schemas.append(schema)
            
        system_prompt = f"""
        You are an expert MongoDB Query Generator.
        Context:
        Available Collections: {json.dumps(collections)}
        Schemas: {json.dumps(schemas)}
        
        Task:
        Generate a valid MongoDB aggregation pipeline based on the user's natural language question.
        Return a JSON object with:
        "collection": The collection to query
        "pipeline": The aggregation pipeline array
        "chart_type": "bar", "line", or "pie"
        "x_field": Field name for X axis
        "y_field": Field name for Y axis
        "title": A descriptive title for the chart
        """
        
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def execute_query(collection_name: str, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Executes the generated MongoDB query/pipeline.
    """
    global db
    if db is None:
        await connect_to_database()
    try:
        cursor = db[collection_name].aggregate(pipeline)
        results = await cursor.to_list(length=100)
        
        # Convert ObjectIDs to strings
        for doc in results:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
        
        return results
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
async def format_response(data: List[Dict[str, Any]], chart_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts raw DB output to the standard QueryResponse format.
    """
    return {
        "chart_type": chart_metadata.get("chart_type", "bar"),
        "x_field": chart_metadata.get("x_field", ""),
        "y_field": chart_metadata.get("y_field", ""),
        "title": chart_metadata.get("title", "Analytics Results"),
        "data": data
    }

if __name__ == "__main__":
    mcp.run()
