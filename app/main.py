from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
import requests
import json

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    model_name = Column(String)
    endpoint = Column(String)
    request = Column(String)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ItemCreate(BaseModel):
    name: str
    model_name: str
    endpoint: str
    request: str


class ItemResponse(BaseModel):
    success: int


@app.post("/add", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):

    if item.endpoint == "string":
        db_item = Item(**item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    else:
        try:
            json.loads(item.request)
        except:
            return ItemResponse(success=0)

        req = requests.post(item.endpoint, json=json.loads(item.request))
        if req.ok:
            db_item = Item(**item.model_dump())
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return ItemResponse(success=1)
        else:
            return ItemResponse(success=0)


@app.post("/get")
async def get(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items
