from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.services.llm_service import generate_aggregation_pipeline
from app.services.query_service import execute_aggregation_pipeline

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    try:
        # 1. LLM interprets user query
        llm_output = await generate_aggregation_pipeline(request.query)
        
        # 2. Execute the generated pipeline
        results = await execute_aggregation_pipeline(
            llm_output["collection"], 
            llm_output["pipeline"]
        )
        
        # 3. Return structured response
        return QueryResponse(
            chart_type=llm_output["chart_type"],
            x_field=llm_output["x_field"],
            y_field=llm_output["y_field"],
            title=llm_output["title"],
            data=results
        )
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))
