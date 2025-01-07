from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="src/component")


@app.get("/setup")
async def setup():
    return {"allow": "permission", "type-mic":"mic","type-audio":"audio"}

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def run_app():
    print("\napplication is running...")
    uvicorn.run("src.app:app",reload=True)
