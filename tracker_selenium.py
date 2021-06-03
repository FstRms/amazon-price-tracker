import os
import smtplib
from selenium import webdriver
from dotenv import load_dotenv

load_dotenv()

PRODUCT_URL = os.environ.get("PRODUCT_URL")
ORIGIN_EMAIL = os.environ.get("ORIGIN_EMAIL")
PASSW = os.environ.get("PASSWORD")
RECEIVER = os.environ.get("RECEIVER_EMAIL")
MINIMAL_PRICE = os.environ.get("PRICE")
DRIVER_PATH = os.environ.get("DRIVER_PATH")

driver = webdriver.Chrome(executable_path=DRIVER_PATH)

driver.get(PRODUCT_URL)
scrapped_price = driver.find_element_by_id("price_inside_buybox")
locate_price = scrapped_price.text
driver.quit()

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
