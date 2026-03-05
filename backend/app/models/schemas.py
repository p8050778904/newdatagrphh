from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime
from bson import ObjectId

# NOTE: Entity schemas (Employee, Product, etc.) are now handled dynamically
# through MCP tool chaining and schema inference.

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    chart_type: str
    x_field: str
    y_field: str
    title: str
    data: List[Dict[str, Any]]
