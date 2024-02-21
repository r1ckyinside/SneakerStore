from typing import Union
import jinja2
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3

app = FastAPI(
    title="Ricky Sneaker"
)

app.mount("/sql", StaticFiles(directory="sql"), name="sql")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def some_route(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, })


def get_items():
    connection = sqlite3.connect('sql/db.db')
    cursor = connection.cursor()
    rows = cursor.execute(
        "SELECT id, name, description, size, brand, condition, price, city, photo FROM Catalog").fetchall()

    class item(BaseModel):
        id: int
        name: str
        description: str
        size: int
        brand: str
        condition: str
        price: int
        city: str
        photo: str

    for i in range(len(rows)):
        item.id = rows[i][0]
        item.name = rows[i][1]
        item.description = rows[i][2]
        item.size = rows[i][3]
        item.brand = rows[i][4]
        item.condition = rows[i][5]
        item.price = rows[i][6]
        item.city = rows[i][7]
        item.photo = rows[i][8]
    return item

