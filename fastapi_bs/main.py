# imports
from pydantic import BaseModel, Field, EmailStr

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session

from fastapi import FastAPI, Form, Cookie, Request, Response, status, Body, Depends, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer

from starlette.responses import RedirectResponse, Response
import time
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

# Initialize
app = FastAPI()

# Postgres Database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:tumtum47@localhost/fastapi"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345678@localhost/fastapi"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Model
class Floor(Base):
    __tablename__ = "floor"

    floor_id = Column(Integer, primary_key=True, index=True)
    floor_name = Column(String)
    floor_image = Column(String)
    floor_description = Column(String)
    floor_price = Column(Float)


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_email = Column(String)
    user_pass = Column(String)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_email: Optional[str] = None


# Create tables
Base.metadata.create_all(bind=engine)

# Static file serv
app.mount("/static", StaticFiles(directory="static"), name="static")
# Jinja2 Template directory
templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Def TOKEN
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
        token_data = TokenData(user_email=user_email)
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)


# Dependency
def get_db():
    try:
        db = Session(bind=engine)
        yield db
    finally:
        db.close()


# HOME
@app.get("/", response_class=HTMLResponse, tags=["HOME PAGE"])
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/company", response_class=HTMLResponse, tags=["HOME PAGE"])
def home_page(request: Request):
    return templates.TemplateResponse("company.html", {"request": request})


@app.get("/contact", response_class=HTMLResponse, tags=["HOME PAGE"])
def home_page(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


# SIGN UP
@app.get("/signup", response_class=HTMLResponse, tags=["SIGN UP"])
async def create_user_ui(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup", response_class=HTMLResponse, tags=["SIGN UP"])
def create_user(request: Request, userEmail: str = Form(...), userPass: str = Form(...),
                db: Session = Depends(get_db)):
    user = User(user_email=userEmail, user_pass=userPass)
    db.add(user)
    db.commit()
    time.sleep(1)
    message_signup = "Sign up successful!"
    return templates.TemplateResponse("signup.html", {"request": request, "message_signup": message_signup})


# LOGIN
@app.get("/login", response_class=HTMLResponse, tags=["SIGN IN"])
def login_ui(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", tags=["SIGN IN"])
def login(request: Request, userEmail: str = Form(...), userPass: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter((User.user_email == userEmail)
                                 & (User.user_pass == userPass)).first()
    if not user:
        message_signin = "Invalid Credentials"
        return templates.TemplateResponse("login.html", {"request": request, "message_signin": message_signin})
    else:
        message_signin = "Sign in successful!"
        access_token = create_access_token(data={"sub": user.user_email})
        return templates.TemplateResponse("login.html", {"request": request, "message_signin": message_signin,
                                                         "access_token": access_token, "token_type": "bearer"})


# FLOOR
@app.get("/floor", response_class=HTMLResponse, tags=["FLOOR CLIENT"])
def read_all_floor(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        token = request.cookies.get("access_token")
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials")
    except Exception:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials")

    result = db.query(Floor).all()
    return templates.TemplateResponse("list_floor.html", {"request": request, "floor_list": result})


# @app.get("/floor", response_class=HTMLResponse, tags=["FLOOR CLIENT"])
# def read_all_floor(request: Request, db: Session = Depends(get_db)):
#     result = db.query(Floor).all()
#     return templates.TemplateResponse("list_floor.html", {"request": request, "floor_list": result})


@app.get("/token", response_class=HTMLResponse, tags=["FLOOR CLIENT"])
async def get_token(request: Request):
    return templates.TemplateResponse("token.html", {"request": request})


@app.get("/floor/view", response_class=HTMLResponse, tags=["FLOOR CLIENT"])
def read_all_floor(request: Request, db: Session = Depends(get_db)):
    result = db.query(Floor).all()
    return templates.TemplateResponse("list_floor_view.html", {"request": request, "floor_list": result})


@app.get("/floor/{id}", response_class=HTMLResponse, tags=["FLOOR CLIENT"])
def read_floor(request: Request, id: int, db: Session = Depends(get_db)):
    result = db.query(Floor).filter(Floor.floor_id == id).first()
    return templates.TemplateResponse("view_floor.html", {"request": request, "floor": result})


# With post_create + createUI
@app.get("/createui", response_class=HTMLResponse, tags=["FLOOR ADMIN"])
async def create_floor_ui(request: Request):
    return templates.TemplateResponse("new_floor.html", {"request": request})


@app.post("/create", response_class=HTMLResponse, tags=["FLOOR ADMIN"])
def create_floor(request: Request, floorId: str = Form(...), floorName: str = Form(...), floorImage: str = Form(...),
                 floorDescription: str = Form(...), db: Session = Depends(get_db)):
    floor = Floor(floor_id=floorId, floor_name=floorName,
                  floor_image=floorImage, floor_description=floorDescription)
    db.add(floor)
    db.commit()
    time.sleep(1)
    result = db.query(Floor).all()
    return templates.TemplateResponse("list_floor.html", {"request": request, "floor_list": result})


@app.get("/floor/delete/{id}", response_class=HTMLResponse, tags=["FLOOR ADMIN"])
def delete_floor(id: int, response: Response, request: Request, db: Session = Depends(get_db)):
    db.query(Floor).filter(Floor.floor_id == id).delete()
    db.commit()
    time.sleep(1)
    result = db.query(Floor).all()
    return templates.TemplateResponse("list_floor.html", {"request": request, "floor_list": result})


# FLOOR UPDATE
@app.get("/floor/edit/{id}", response_class=HTMLResponse, tags=["FLOOR ADMIN"])
def edit_floor(request: Request, id: int, db: Session = Depends(get_db)):
    result = db.query(Floor).filter(Floor.floor_id == id).first()
    return templates.TemplateResponse("edit_floor.html", {"request": request, "floor": result})


@app.post("/update", response_class=HTMLResponse, tags=["FLOOR ADMIN"])
def update_floor(request: Request, id: int, floorName: str = Form(...), floorImage: str = Form(...),
                 floorDescription: str = Form(...), db: Session = Depends(get_db)):
    db.query(Floor).filter(Floor.floor_id == id).update({
        Floor.floor_name: floorName,
        Floor.floor_image: floorImage,
        Floor.floor_description: floorDescription
    })
    db.commit()
    time.sleep(1)
    result = db.query(Floor).all()
    return templates.TemplateResponse("list_floor.html", {"request": request, "floor_list": result})
