# server.py
import chromadb
import uuid
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# Allow all CORS (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mcp = FastMCP("Demo") 

client = chromadb.Client()
collection = client.create_collection(name="customer_memory")

# Data Models
class MemoryInput(BaseModel):
    user_input: str
    user_id: str = "default_user"

class MemoryStore(BaseModel):
    summary: str
    user_id: str = "default_user"

# --- FIX 1: Add Root Route (Stops 404 at http://localhost:3333/) ---
@app.get("/")
def read_root():
    return {"status": "Online", "message": "Server is running"}

@app.post("/memory/retrieve")
def retrieve_memory(data: MemoryInput):
    results = collection.query(
        query_texts=[data.user_input],
        n_results=1 
    )
    # Return the first document if found, else empty
    context = results['documents'][0][0] if results['documents'] and results['documents'][0] else "No previous context."
    return {"context": context}

@app.post("/memory/store")
def store_memory(data: MemoryStore):
    collection.add(
        documents=[data.summary],
        metadatas=[{"user_id": data.user_id}],
        ids=[str(uuid.uuid4())]
    )
    return {"status": "success"}

# --- FIX 2: Add HTTP Route for n8n ---
# We add @app.get so n8n can call this via HTTP GET
@app.get("/tools/order-status")
@mcp.tool()
def get_order_status(order_id: str):
    return {"status": "Shipped", "delivery": "2 days"} 

if __name__ == "__main__":
    uvicorn.run(app, port=3333)