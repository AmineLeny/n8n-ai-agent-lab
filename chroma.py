# server.py (Updated with Memory)
import chromadb
import uuid
from fastapi import FastAPI, Body
from mcp.server.fastmcp import FastMCP
import uvicorn
from pydantic import BaseModel

app = FastAPI()
mcp = FastMCP(app)

# Initialize ChromaDB [cite: 50-54]
client = chromadb.Client()
collection = client.create_collection(name="customer_memory")

# Data Models
class MemoryInput(BaseModel):
    user_input: str
    user_id: str = "default_user"

class MemoryStore(BaseModel):
    summary: str
    user_id: str = "default_user"

@app.post("/memory/retrieve")
def retrieve_memory(data: MemoryInput):
    # Logic from Manual Section 12.2 [cite: 116-117]
    results = collection.query(
        query_texts=[data.user_input],
        n_results=1 # Limit to 1 for simplicity
    )
    # Return the first document if found, else empty
    context = results['documents'][0][0] if results['documents'] and results['documents'][0] else "No previous context."
    return {"context": context}

@app.post("/memory/store")
def store_memory(data: MemoryStore):
    # Logic from Manual Section 12.1 [cite: 110-113]
    collection.add(
        documents=[data.summary],
        metadatas=[{"user_id": data.user_id}],
        ids=[str(uuid.uuid4())]
    )
    return {"status": "success"}

# Existing Tool
@mcp.tool()
def get_order_status(order_id: str):
    return {"status": "Shipped", "delivery": "2 days"} 

if __name__ == "__main__":
    uvicorn.run(app, port=3333)