from pydantic import BaseModel


class Prices_model(BaseModel):
    CoinName: str
    Timestamp: str
    Price: float


class AlertSubscriptions_model(BaseModel):
    Email: str
    CoinName: str
    DifferencePercentage: int
