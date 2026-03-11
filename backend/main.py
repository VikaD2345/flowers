import json
import os
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from database import get_db, get_optional_db
from models import FlowerModel

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CATALOG_PATH = BASE_DIR / "data" / "catalog.json"
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
MOCK_DATA_FILE = Path(os.getenv("MOCK_DATA_FILE", str(DEFAULT_CATALOG_PATH)))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FlowerBase(BaseModel):
    name: str
    price: float
    image_url: HttpUrl


class Flower(FlowerBase):
    id: int


class FlowerCreate(FlowerBase):
    pass


def load_mock_flowers() -> list[Flower]:
    if not MOCK_DATA_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Mock catalog file not found: {MOCK_DATA_FILE}",
        )

    with MOCK_DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return [Flower(**item) for item in data]


def get_db_flowers(db: Session) -> list[Flower]:
    rows = db.query(FlowerModel).all()
    return [
        Flower(id=row.id, name=row.name, price=float(row.price), image_url=row.image_url)
        for row in rows
    ]


@app.get("/health")
def health():
    return {"status": "ok", "use_mock_data": USE_MOCK_DATA}


@app.get("/flowers", response_model=list[Flower])
def list_flowers(db: Session | None = Depends(get_optional_db)):
    if USE_MOCK_DATA:
        return load_mock_flowers()
    if db is None:
        raise HTTPException(status_code=500, detail="DATABASE_URL is not configured")
    return get_db_flowers(db)


@app.get("/flowers/{flower_id}", response_model=Flower)
def get_flower(flower_id: int, db: Session | None = Depends(get_optional_db)):
    if not USE_MOCK_DATA and db is None:
        raise HTTPException(status_code=500, detail="DATABASE_URL is not configured")
    flowers = load_mock_flowers() if USE_MOCK_DATA else get_db_flowers(db)
    for flower in flowers:
        if flower.id == flower_id:
            return flower
    raise HTTPException(status_code=404, detail="Flower not found")


@app.post("/admin/flowers", response_model=Flower)
def create_flower(payload: FlowerCreate, db: Session = Depends(get_db)):
    if USE_MOCK_DATA:
        raise HTTPException(
            status_code=405,
            detail="Admin flower creation is disabled in mock mode",
        )

    row = FlowerModel(
        name=payload.name,
        price=payload.price,
        image_url=str(payload.image_url),
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return Flower(id=row.id, name=row.name, price=float(row.price), image_url=row.image_url)
