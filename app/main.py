from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from rich.console import Console

from app.api.generate import generate_documentation, GenerateRequest
from app.services.database_service import MongoDBService
from sentence_transformers import SentenceTransformer

app = FastAPI(
    title="DocGen API",
    description="API for generating documentation websites from GitHub repositories.",
    version="1.0.0",
)

console = Console()

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Templates for rendering HTML
templates = Jinja2Templates(directory="frontend/static")

OUTPUT_BASE_DIR = Path("output")
OUTPUT_BASE_DIR.mkdir(exist_ok=True)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_doc_endpoint(request: GenerateRequest):
    try:
        console.log(f"[bold blue]Received request to generate docs for: {request.repo_url}[/bold blue]")
        result = await generate_documentation(request, OUTPUT_BASE_DIR)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        console.log(f"[bold red]API Error: {e}[/bold red]")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search_documentation(query: str, mongo_uri: str, mongo_db_name: str, index_name: str = "default_vector_index", limit: int = 5):
    try:
        console.log(f"[bold blue]Received search request for query: {query}[/bold blue]")
        db_service = MongoDBService(mongo_uri, mongo_db_name)
        if not db_service.connect():
            raise HTTPException(status_code=500, detail="Failed to connect to MongoDB Atlas.")

        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        query_vector = embedding_model.encode(query).tolist()

        search_results = db_service.vector_search("analysis_results", query_vector, index_name, limit)
        db_service.disconnect()
        return JSONResponse(status_code=200, content={"query": query, "results": search_results})
    except Exception as e:
        console.log(f"[bold red]API Error during search: {e}[/bold red]")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
