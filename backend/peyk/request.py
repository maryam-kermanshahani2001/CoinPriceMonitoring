import requests

email = "marmarakt1379@gmail.com"
coinName = "docoin"
priceChange = 4

url = "http://127.0.0.1:9076/subscribe/"

data = {
    "email": email,
    "coinName": coinName,
    "priceChange": priceChange
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Subscription successful!")
    print(response.text)
else:
    print(response.status_code)
    print("Failed to subscribe. Error:", response.text)
