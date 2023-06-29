CREATE TABLE Prices_table (
    Id SERIAL PRIMARY KEY,
    CoinName VARCHAR,
    Timestamp VARCHAR,
    Price FLOAT,
    RoC FLOAT
);
CREATE TABLE AlertSubscriptions_table (
    Id SERIAL PRIMARY KEY,
    Email VARCHAR,
    CoinName VARCHAR,
    DifferencePercentage FLOAT
);