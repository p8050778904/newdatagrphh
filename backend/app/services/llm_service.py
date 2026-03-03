import os
import json
from openai import AsyncOpenAI
from app.services.llm.prompt import SYSTEM_PROMPT

# Initialize OpenAI Client
# The user should set OPENAI_API_KEY in backend/.env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY == "your_openai_api_key_here":
    OPENAI_API_KEY = None

client = AsyncOpenAI(api_key=OPENAI_API_KEY or "dummy")

async def generate_aggregation_pipeline(user_query: str) -> dict:
    """
    Sends the user query to the LLM and returns the structured aggregation pipeline.
    If no API key is provided, it falls back to the simulated logic to prevent crashes.
    """
    if not OPENAI_API_KEY or OPENAI_API_KEY == "dummy":
        print("Running in Simulation Mode (No API Key).")
        return await simulated_generate_pipeline(user_query)

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the LLM output
        llm_json = json.loads(response.choices[0].message.content)
        return llm_json

    except Exception as e:
        print(f"LLM Error: {e}")
        return await simulated_generate_pipeline(user_query)

async def simulated_generate_pipeline(user_query: str) -> dict:
    # Simulation logic for Croma Retail Model
    query_lower = user_query.lower()
    
    if "region" in query_lower:
        return {
            "collection": "sales",
            "pipeline": [
                {"$addFields": {"region_str": {"$toString": "$region_id"}}},
                {"$lookup": {"from": "regions", "localField": "region_str", "foreignField": "_id", "as": "reg"}},
                {"$unwind": "$reg"},
                {"$group": {"_id": "$reg.region_name", "total_sales": {"$sum": "$total_amount"}}},
                {"$project": {"region": "$_id", "total_sales": 1, "_id": 0}},
                {"$sort": {"total_sales": -1}}
            ],
            "chart_type": "bar",
            "x_field": "region",
            "y_field": "total_sales",
            "title": "Total Sales by Region"
        }
    elif "brand" in query_lower:
        return {
            "collection": "sales",
            "pipeline": [
                {"$unwind": "$product_breakdown"},
                {"$addFields": {"prod_id_str": {"$toString": "$product_breakdown.product_id"}}},
                {"$lookup": {"from": "products", "localField": "prod_id_str", "foreignField": "_id", "as": "prod"}},
                {"$unwind": "$prod"},
                {"$group": {"_id": "$prod.brand", "revenue": {"$sum": "$product_breakdown.amount"}}},
                {"$project": {"brand": "$_id", "revenue": 1, "_id": 0}},
                {"$sort": {"revenue": -1}}
            ],
            "chart_type": "bar",
            "x_field": "brand",
            "y_field": "revenue",
            "title": "Brand-wise Sales Performance"
        }
    elif "employee" in query_lower:
        return {
            "collection": "sales",
            "pipeline": [
                {"$addFields": {"emp_id_str": {"$toString": "$employee_id"}}},
                {"$lookup": {"from": "employees", "localField": "emp_id_str", "foreignField": "_id", "as": "emp"}},
                {"$unwind": "$emp"},
                {"$group": {"_id": "$emp.name", "revenue": {"$sum": "$total_amount"}}},
                {"$project": {"employee": "$_id", "revenue": 1, "_id": 0}},
                {"$sort": {"revenue": -1}},
                {"$limit": 5}
            ],
            "chart_type": "bar",
            "x_field": "employee",
            "y_field": "revenue",
            "title": "Top 5 Employees by Revenue"
        }
    else:
        # Default: Monthly Sales Trend
        return {
            "collection": "sales",
            "pipeline": [
                {"$group": {"_id": {"$dateToString": {"format": "%Y-%m", "date": "$sale_date"}}, "sales": {"$sum": "$total_amount"}}},
                {"$project": {"month": "$_id", "sales": 1, "_id": 0}},
                {"$sort": {"month": 1}}
            ],
            "chart_type": "line",
            "x_field": "month",
            "y_field": "sales",
            "title": "Monthly Sales Trend"
        }
