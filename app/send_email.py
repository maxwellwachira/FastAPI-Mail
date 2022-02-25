from fastapi import FastAPI, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.responses import JSONResponse
from starlette.requests import Request
from decouple import config
from app.models import EmailSchema
from pathlib import Path

#Landing page template
templates = Jinja2Templates(directory=Path(__file__).parent / '../templates/')

conf = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_USERNAME"),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM = config("MAIL_FROM"),
    MAIL_PORT = config("MAIL_PORT"),
    MAIL_SERVER = config("MAIL_SERVER"),
    MAIL_TLS = config("MAIL_TLS"),
    MAIL_SSL = config("MAIL_SSL"),
    USE_CREDENTIALS = config("USE_CREDENTIALS"),
    VALIDATE_CERTS = config("VALIDATE_CERTS"),
    TEMPLATE_FOLDER = Path(__file__).parent / '../templates/email',
   
)


app = FastAPI(title='Sending Email using FastAPI')


@app.get("/", response_class=HTMLResponse, tags=["root"])
async def root(request: Request):
     return templates.TemplateResponse('landing_page.html', context={'request': request})

#Send Email Asynchronously
@app.post("/email-async", tags=["Send Email Asynchronously"])
async def send_email_async(data: EmailSchema) -> JSONResponse:
    
    message = MessageSchema (
        subject = data.subject,
        recipients = data.dict().get("email"),
        template_body=data.dict().get("body"),
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="email.html")
    return JSONResponse(status_code=200, content={"message": "Email has been sent"})


#SEnd Email using Background Tasks
@app.post("/email-background", tags=["Send Email using Background Tasks"])
async def send_email_background(data: EmailSchema, background_tasks: BackgroundTasks) -> JSONResponse:
    
    message = MessageSchema (
        subject = data.subject,
        recipients = data.dict().get("email"),
        template_body=data.dict().get("body"),
        subtype="html"
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message, template_name="email.html")
    return JSONResponse(status_code=200, content={"message": "Email has been sent"})

