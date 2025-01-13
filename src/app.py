from datetime import datetime

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from src.configuration.config_handler import handle_config

from .configuration.config_handler import GenderIdentity, Name, User 
from .configuration.config_handler import  get_option, update_config, _backup_user_config

app = FastAPI()
templates = Jinja2Templates(directory="src/component")


@app.get("/onboarding")
async def onboarding(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})


@app.post("/onboarding")
async def process_onboarding(
    firstName: str = Form("user"),
    lastName: str = Form(...),
    genderIdentity: GenderIdentity = Form("prefer_not_to_say"),
    onboardingStatus: bool  = Form("false"),
):

    user = User(
        name=Name(firstName=firstName, lastName=lastName),
        onboardingStatus=onboardingStatus,
        genderIdentity=genderIdentity,
        joiningDate= datetime.now().strftime("%Y-%b-%d-%H:%M:%S"),
    )
    _backup_user_config()
    update_config(user)


@app.get("/")
async def root():
    config_data = get_option()
    if config_data.onboardingStatus:
        return RedirectResponse(url="/onboarding")
    else:
        return RedirectResponse(url="/dashboard")


@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



def run_app():
    print("\napplication is running...")
    handle_config()
    uvicorn.run("src.app:app", reload=True)
