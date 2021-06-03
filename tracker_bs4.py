import requests
import lxml
import os
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv

load_dotenv()

PRODUCT_URL = os.environ.get("PRODUCT_URL")
ORIGIN_EMAIL = os.environ.get("ORIGIN_EMAIL")
PASSW = os.environ.get("PASSWORD")
RECEIVER = os.environ.get("RECEIVER_EMAIL")
MINIMAL_PRICE = os.environ.get("PRICE")

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "accept-language": "es-ES,es;q=0.9,en;q=0.8",
}
response = requests.get(PRODUCT_URL, headers=headers)


soup = BeautifulSoup(response.content, "lxml")
locate_price = soup.find(id="price_inside_buybox").get_text()
price = locate_price.split("$")[1].strip()

if "," in price:
    price_unformatted = price.split(",")
    price_formatted = price_unformatted[0] + price_unformatted[1]
else:
    price_formatted = price

cost = float(price_formatted)

email_message = None

if cost <= float(MINIMAL_PRICE):
    email_message = f"Subject:Amazon Price Drop\n\nDude your product is at ${cost}.\nGO! GO! GO! {PRODUCT_URL}."
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=ORIGIN_EMAIL, password=PASSW)
        connection.sendmail(
            from_addr=ORIGIN_EMAIL, to_addrs=RECEIVER, msg=email_message.encode("utf-8")
        )
