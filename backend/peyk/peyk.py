from fastapi import FastAPI
import uvicorn
from db.Postgres import *
from pydantic import BaseModel
import json

class Info(BaseModel):
    email: str
    coinName: str
    priceChange: float


app = FastAPI(title="Peyk")

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/subscribe/")
async def subscribe_coin(info: Info):
    try:
        if not database.is_connected:  # Remove await keyword here
            await database.connect()
            print("Connected to the database")

        email = info.email
        coin_name = info.coinName
        price_change = info.priceChange
        # insert to db
        query = AlertSubscriptions_table.insert().values(
            Email=email,
            CoinName=coin_name,
            DifferencePercentage=price_change
        )
        print(f'{email} added for {price_change}')
        await database.execute(query=query)
        return "yes!"
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return "Failed to subscribe. An error occurred."



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
