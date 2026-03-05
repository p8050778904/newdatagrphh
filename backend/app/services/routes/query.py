from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.services.llm_service import generate_aggregation_pipeline

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    try:
        # The new llm_service now orchestrates the entire MCP tool flow
        # including query generation, execution, and formatting.
        result = await generate_aggregation_pipeline(request.query)
        
        if "error" in result and len(result) == 1:
             raise HTTPException(status_code=500, detail=result["error"])

        return QueryResponse(**result)
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))
