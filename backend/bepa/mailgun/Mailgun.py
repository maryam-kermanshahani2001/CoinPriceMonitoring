import requests
import json


# with open('config.json') as json_config_file:
#     config_data = json.load(json_config_file)

DOMAIN ="sandbox70b70422770e452daeb452a18e06b282.mailgun.org"
API_KEY = "1d3565c0fe4dced873335adae8be62a3-135a8d32-117af8df"
# DOMAIN = config_data["MAILGUN_DOMAIN"]
# API_KEY = config_data["MAILGUN_API_KEY"]
# TEXT = f"""
#         <h1>BOOO </h1>
#
#         """
# SUBJECT = "Cloud Computing Final Project - Mail Service"
# EMAIL_ADDRESS = "sch.mahdipour@gmail.com"


def send_simple_message(email, subject, text):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", API_KEY),
        data={"from": f"<mailgun@{DOMAIN}>",
              "to": [email],
              "subject": subject,
              "html": text})


# if __name__ == '__main__':
#     response = send_simple_message(EMAIL_ADDRESS, SUBJECT, TEXT)
#     print(response.json())
