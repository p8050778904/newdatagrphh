from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.mongodb_connector import connect_to_mongo, close_mongo_connection
from app.services.routes import query

app = FastAPI(title="AI-Driven Analytics Dashboard")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Include routes
app.include_router(query.router, prefix="/api", tags=["Analytics"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Analytics API"}
