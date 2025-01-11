from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import uvicorn
from src.configuration.config_handler import handle_config

app = FastAPI()
templates = Jinja2Templates(directory="src/component")


@app.get("/setup")
async def setup(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})

@app.get("/")
async def root():
    if check_onboarding_status():
        return RedirectResponse(url="/setup")
    else:
        return RedirectResponse(url="/dashboard")

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def check_onboarding_status():
    return True


def run_app():
    print("\napplication is running...")
    handle_config()
    uvicorn.run("src.app:app",reload=True)
