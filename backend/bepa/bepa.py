from mailgun import Mailgun
from db.Schema import *
import asyncio
import requests
from db.Postgres import *
from datetime import datetime
from mailgun import *
import json


with open('config.json') as json_config_file:
    config_data = json.load(json_config_file)

coinnews_url = config_data['COIN_NEWS_HOST']

def get_data():
    # url = "http://localhost:8000/api/data"  # get list of all currencies
    # url = "http://coinnews-container:8000/api/data"   #get list of all currencies
    url = coinnews_url
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # get all currencies data and add to Prices table
        for CoinName in data:
            url_currency = f"{coinnews_url}{CoinName}"  # get currency data
            # url_currency = f"http://localhost:8000/api/data/{CoinName}"  # get currency data

            response_currency = requests.get(url_currency)
            data_currency = response_currency.json()
            print(data_currency)
            timestamp_str = data_currency['updated_at']
            roc = float(data_currency['roc'])
            price = data_currency['value']
            try:
                with engine.connect() as conn:
                    # insert to db
                    query = Prices_table.insert().values(CoinName=CoinName,
                                                         Timestamp=timestamp_str,
                                                         Price=price,
                                                         RoC=roc)

                    conn.execute(query)
                    handle_subscription(CoinName, roc)
                    print("INFO: Database inserted.")
            except Exception as e:
                print("ERROR: Failed to connect to the database.")
                print(f"Error message: {e}")

        print('done')


    else:
        print("Error occurred!")


def sendMail(email, CoinName, mode):
    subject = f'Hurry Up! {CoinName} alert'
    m = ''
    if mode == 1:
        m += 'increasing!'
    else:
        m += 'decreasing!'
    text = f'Hi,Notice that {CoinName} is {m}'
    # mailgun_instance = Mailgun.Mailgun()
    Mailgun.send_simple_message(email, subject, text)
    print('Email sent successfully!')


def handle_subscription(CoinName, roc):
    print(f'Handling for {CoinName}')
    persons = get_from_Alert(CoinName)
    for person in persons:
        email = person['Email']
        dp = person['DifferencePercentage']
        if 100 * abs(roc) >= dp:
            if roc >= 0:
                sendMail(email, CoinName, 1)
            else:
                sendMail(email, CoinName, 0)


def check_database_connection():
    try:
        with engine.connect() as conn:
            tables_exist = engine.dialect.has_table(conn, "Prices_table") and engine.dialect.has_table(conn,
                                                                                                       "AlertSubscriptions_table")
            if tables_exist:
                print("INFO: Database tables are created.")
            else:
                print("INFO: Database tables are not created.")

    except Exception as e:
        print("ERROR: Failed to connect to the database.")
        print(f"Error message: {e}")


if __name__ == '__main__':
    check_database_connection()
    get_data()
