import requests

email = "marmarakt1379@gmail.com"
coinName = "docoin"
priceChange = 4

url = "http://localhost:8080/subscribe/?email={}&coinName={}&priceChange={}".format(email, coinName, priceChange)

response = requests.post(url)

if response.status_code == 200:
    print("Subscription successful!")
else:
    print(response.status_code)
    print("Failed to subscribe. Error:", response.text)
