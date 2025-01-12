import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from .configuration.config_handler import User 

from src.configuration.config_handler import handle_config

app = FastAPI()
templates = Jinja2Templates(directory="src/component")


@app.get("/onboarding")
async def onboarding(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})


@app.post("/onboarding")
async def process_onboarding(
    firstName: str = Form(...),
    lastName: str = Form(...),
    genderIdentity: str = Form(...),
    onboardingStatus: str = Form("false"),
):
    CONFIG = {
      "user": {
        "joiningDate": datetime.now().strftime("%Y-%b-%d-%H:%M:%S"),
        "genderIdentity": genderIdentity,
        "onboardingStatus": onboardingStatus,
        "name": {
          "firstName": firstName,
          "lastName": lastName
        },
      }
    }

    valid_data = User(**CONFIG["user"])
    print(valid_data)


@app.get("/")
async def root():
    if check_onboarding_status():
        return RedirectResponse(url="/onboarding")
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
    uvicorn.run("src.app:app", reload=True)
