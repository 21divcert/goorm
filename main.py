from fastapi import FastAPI
import csv
from contextlib import asynccontextmanager


def load_data():
    with open('./data/gyul.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=",")
        result = {
            int(row.pop("year")): row for row in reader
        }
    return result


gyul_stats = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global gyul_stats
    gyul_stats = load_data()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello, Jeju!"}


@app.get("/stats")
async def get_stats():
    return gyul_stats


@app.get("/stats/{year}")
async def get_single_year_stats(year: int):
    return gyul_stats.get(year, {})
