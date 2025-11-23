from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from rich.console import Console

from app.api.generate import generate_documentation, GenerateRequest

app = FastAPI(
    title="DocGen API",
    description="API for generating documentation websites from GitHub repositories.",
    version="1.0.0",
)

console = Console()

OUTPUT_BASE_DIR = Path("output")
OUTPUT_BASE_DIR.mkdir(exist_ok=True)

@app.post("/generate")
async def generate_doc_endpoint(request: GenerateRequest):
    try:
        console.log(f"[bold blue]Received request to generate docs for: {request.repo_url}[/bold blue]")
        result = await generate_documentation(request, OUTPUT_BASE_DIR)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        console.log(f"[bold red]API Error: {e}[/bold red]")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return {"message": "Welcome to DocGen API. Use POST /generate to create documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
