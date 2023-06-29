import sqlalchemy
import databases

DATABASE_URL = 'postgresql://root:hIW5IrLdxhMsBDy2XYsTw6Xz@billy.iran.liara.ir:33737/postgres'
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)

Prices_table = sqlalchemy.Table(
    "Prices_table",
    metadata,
    sqlalchemy.Column("Id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("CoinName", sqlalchemy.String),
    sqlalchemy.Column("Timestamp", sqlalchemy.String),
    sqlalchemy.Column("Price", sqlalchemy.Float),
    sqlalchemy.Column("RoC", sqlalchemy.Float)
)

AlertSubscriptions_table = sqlalchemy.Table(
    "AlertSubscriptions_table",
    metadata,
    sqlalchemy.Column("Id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("Email", sqlalchemy.String),
    sqlalchemy.Column("CoinName", sqlalchemy.String),
    # sqlalchemy.Column("checked", sqlalchemy.Boolean),
    sqlalchemy.Column("DifferencePercentage", sqlalchemy.Float)
)


metadata.create_all(engine)

# def delete_rows():
#     with engine.connect() as conn:
#         delete_statement = AlertSubscriptions_table.delete().where(AlertSubscriptions_table.c.column_name == "value")

def get_from_Alert(CoinName):
    try:
        with engine.connect() as conn:
            query = AlertSubscriptions_table.select().where(AlertSubscriptions_table.c.CoinName == CoinName)
            result = conn.execute(query)
            data = result.fetchall()
            if data:
                print(f"INFO: Got data from DB for {CoinName}")
                return [dict(row) for row in data]
            else:
                print(f"INFO: No data found in DB for {CoinName}")
                return []
    except Exception as e:
        print(f"ERROR: Failed to get data from DB for {CoinName}")
        print(f"Error message: {e}")
        return []


def get_from_Prices(CoinName):
    try:
        with engine.connect() as conn:
            query = Prices_table.select().where(Prices_table.c.CoinName == CoinName)
            result = conn.execute(query)
            data = result.fetchall()
            if data:
                print(f"INFO: Got data from DB for {CoinName}")
                return [dict(row) for row in data]
            else:
                print(f"INFO: No data found in DB for {CoinName}")
                return []
    except Exception as e:
        print(f"ERROR: Failed to get data from DB for {CoinName}")
        print(f"Error message: {e}")
        return []


def check_database_connection():
    try:
        with engine.connect() as conn:
            tables_exist = engine.dialect.has_table(conn, "Prices_table") and engine.dialect.has_table(conn,
                                                                                                       "AlertSubscriptions_table")
            if tables_exist:
                print("INFO: Database tables are created.")
            else:
                print("INFO: Database tables are not created.")

            conn.execute("SELECT 1")  # Execute a simple query to check the database connection
            print("INFO: Database connection established.")
    except Exception as e:
        print("ERROR: Failed to connect to the database.")
        print(f"Error message: {e}")

