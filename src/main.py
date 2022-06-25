import os
import secrets
import time
from cgitb import handler
from typing import Union
from uuid import uuid1

from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum
from pydantic import BaseSettings

from domains.qr_code import QrCode
from master_data import master_data
from schemas.QrCode import QrCodeParams


class Settings(BaseSettings):
    basic_user: str
    basic_pass: str
    class Config:
        env_file = ".env"
        

app = FastAPI()

# Basic
security = HTTPBasic()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

QR_FILE_PATH = "static/qr/"

def qr_file_remove() -> None:
    now = time.time()
    for _curdir, _dirs, files in os.walk(QR_FILE_PATH):
        for file in files:
            if now - os.path.getatime(QR_FILE_PATH+file) > 60:
                os.remove(QR_FILE_PATH + file)
            
    return

def auth_user(credentials:HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, Settings().basic_user)
    correct_password = secrets.compare_digest(credentials.password, Settings().basic_pass)
    if not(correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="unauthorized",
            headers={"WWW-Authenticate": "Basic"}
        )
    return credentials.username


def createSelectResponse(request:Request, file_name:str="",qr_str:Union[str,None]=None):
    return {
        "request": request,
        "qr_str":qr_str,
        "selection":{
            "l_type_list":master_data.l_type_list,
            "s_type_list":master_data.s_type_list,
            "free_format_list":master_data.free_format_list,
            "diameter_list":master_data.diameter_list,
            "length_list":master_data.length_list,
            "delimiter_list":master_data.delimiter_list,
            "fittings_type_list":master_data.fittings_types_list
            },
        "uuid": uuid1(),
        "file_name":file_name
        }
    
def createInputResponse(request:Request,file_name:str = "", qr_str:Union[str,None]=None):
    return {
        "request": request,
        "qr_str":qr_str,
        "file_name":file_name,
        "uuid": uuid1()
    }    

@app.get("/input", response_class=HTMLResponse)
async def input_root(request: Request,username:str = Depends(auth_user)):
    qr_file_remove()
    return templates.TemplateResponse("input.html", createInputResponse(request))

@app.get("/input/qr")
async def to_input_root(request: Request,username:str = Depends(auth_user)):
    qr_file_remove()
    return templates.TemplateResponse("input.html", createInputResponse(request))

    
@app.post("/input/qr")
async def create_qr_input(
    request: Request,
    qr_str: str = Form(...),
    uuid: str = Form(...),
    username:str = Depends(auth_user)
    ):
        
    qr = QrCode(qr_str,QR_FILE_PATH + uuid + ".png")
    print("qr_str length:" + str(len(qr.qr_str)))
    
    #create QR code
    qr.create_qr_code()

    return templates.TemplateResponse("input.html", createInputResponse(request,uuid,qr.qr_str.decode()))

@app.get("/", response_class=HTMLResponse)
async def root(request: Request,username:str = Depends(auth_user)):
    qr_file_remove()
    return templates.TemplateResponse("select.html", createSelectResponse(request))


@app.get("/qr")
async def to_root(request: Request,username:str = Depends(auth_user)):
    qr_file_remove()
    return templates.TemplateResponse("select.html", createSelectResponse(request))

    
@app.post("/qr")
async def create_qr_select(
    request: Request,
    product_id:str = Form(...),
    l_type:str = Form(...),
    s_type:str = Form(...),
    free_format:str = Form(...),
    length:str = Form(...),
    diameter:str = Form(...),
    upper_fittings_type:str = Form(...),
    lower_fittings_type:str = Form(...),
    delimiter_str: str = Form(...),
    uuid: str = Form(...),
    username:str = Depends(auth_user)
    ):
        
    qr = QrCode(QrCodeParams.parse_obj({
        "product_id":product_id,
        "l_type":l_type,
        "s_type":s_type,
        "free_format":free_format,
        "length":length,
        "diameter":diameter,
        "upper_fittings_type":upper_fittings_type,
        "lower_fittings_type":lower_fittings_type,
        "delimiter_str":delimiter_str
    }),QR_FILE_PATH + uuid + ".png")
    print("qr_str length:" + str(len(qr.qr_str)))
    
    #create QR code
    qr.create_qr_code()

    return templates.TemplateResponse("select.html", createSelectResponse(request,uuid,qr.qr_str.decode()))

