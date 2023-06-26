from fastapi import FastAPI
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



@app.get("/price/")
async def get_price_history(coin_name: str):
    try:
        print(f"INFO: Got price history from prices_table for {coin_name}")
        return get_from_Prices(coin_name)
    except Exception as e:
        print(f"ERROR: Failed to get data from DB for {coin_name}")
        print(f"Error message: {e}")
        return []


if __name__ == '__main__':
    uvicorn.run("peyk:app", host='localhost', port=8080, reload=True)
