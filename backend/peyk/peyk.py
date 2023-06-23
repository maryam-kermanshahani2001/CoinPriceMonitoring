import json
import string
from typing import Union
from db.Schema import *
from fastapi import FastAPI, File, HTTPException, Response, UploadFile
import uvicorn
from db.Postgres import *
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class Info(BaseModel):
    email: str
    coinName: str | None = None
    priceChange: float



app = FastAPI(title="Peyk")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/up')
async def up():
    return f"Hey!"


@app.post("/subscribe/")
async def subscribe_coin(info:Info):
    # insert to db
    query = AlertSubscriptions_table.insert().values(
        Email=info.email,
        CoinName=info.coinName,
        DifferencePercentage=info.priceChange
    )

    await database.execute(query=query)
    return f"Your submission was registered."


# # curl -X GET "http://localhost:8000/check_email/?id=5"
@app.get("/price/")
async def get_price_history(coin_name: str):
    try:
        print(f"INFO: Got price history from prices_table for {coin_name}")
        return get_from_Prices(coin_name)
        # with engine.connect() as conn:
        #     query = Prices_table.select().where(Prices_table.CoinName == coin_name)
        #     result = conn.execute(query)
        #     data = result.fetchall()
        #     if not data:
        #         print(f"INFO: Got price history from prices_table for {coin_name}")
        #         return [dict(row) for row in data]
        #     else:
        #         print(f"INFO: No data found in DB for {coin_name}")
        #         return []
    except Exception as e:
        print(f"ERROR: Failed to get data from DB for {coin_name}")
        print(f"Error message: {e}")
        return []


if __name__ == '__main__':
    uvicorn.run("peyk:app", host='localhost', port=8080, reload=True)
