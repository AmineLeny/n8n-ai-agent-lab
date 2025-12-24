# Customer Support API & UI

This project provides a simple API for storing and retrieving customer support memory, and a web UI for interacting with it.

## Features

- FastAPI backend with endpoints for storing and retrieving memory
- ChromaDB for document storage
- Streamlit UI for user interaction
- Example tool endpoint for order status

## How to Run

1. **Install dependencies**

   - Python 3.10+
   - `pip install -r requirements.txt`

2. **Start the API server**

   - Run: `python chroma.py`
   - The API will be available at `http://localhost:3333`

3. **Start the Streamlit UI**
   - Run: `streamlit run ui.py`
   - The UI will be available at `http://localhost:8501`

## API Endpoints

- `POST /memory/store` — Store a summary for a user
- `POST /memory/retrieve` — Retrieve memory context for a user input
- `POST /tool/get_order_status` — Example tool endpoint

## Project Files

- `chroma.py` — FastAPI server and ChromaDB logic
- `ui.py` — Streamlit user interface
- `main.py` — Example tool registration

## Notes

- CORS is enabled for development.
- All memory is stored in ChromaDB.
- For production, restrict CORS and secure endpoints.
