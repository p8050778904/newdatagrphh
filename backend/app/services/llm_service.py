import os
import json
import asyncio
from typing import Dict, Any, List
# Fix import to use the renamed module
from mcp.mcp_server import generate_query, execute_query, format_response

async def generate_aggregation_pipeline(user_query: str) -> dict:
    """
    Interpretation of user query using MCP tools.
    1. Calls generate_query (which internally lists collections and gets schemas).
    2. Executes the query.
    3. Formats the response for the UI.
    """
    try:
        # Step 1: Generate the query/metadata via MCP tool
        # In a real MCP setup, this would be a client call. 
        # Here we call the decorated functions directly for the bridge.
        query_metadata = await generate_query(user_query)
        
        if "error" in query_metadata:
            raise Exception(query_metadata["error"])
        
        # Step 2: Execute the query
        raw_data = await execute_query(
            query_metadata["collection"], 
            query_metadata["pipeline"]
        )
        
        # Step 3: Format the response for the frontend
        final_response = await format_response(raw_data, query_metadata)
        
        # Ensure collection and pipeline are included if needed by other logic
        final_response["collection"] = query_metadata["collection"]
        final_response["pipeline"] = query_metadata["pipeline"]
        
        return final_response

    except Exception as e:
        print(f"Error in LLM Service (via MCP): {e}")
        return {
            "error": str(e),
            "chart_type": "bar",
            "x_field": "error",
            "y_field": "count",
            "title": "Error Processing Query",
            "data": [{"error": str(e), "count": 1}]
        }
