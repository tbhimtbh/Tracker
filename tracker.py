import requests
from bs4 import BeautifulSoup
import time

url = "https://www.facebook.com/profile.php?id=100090350417345"

def scrape_page():
    # Make a GET request to the page
    response = requests.get(url)
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    # Find the latest post
    latest_post = soup.find("div", {"class": "_1dwg _1w_m _q7o"})
    return latest_post

while True:
    print("Scraping...")
    latest_post = scrape_page()
    time.sleep(5) # Wait 5 seconds before scraping again
    new_post = scrape_page()
    if latest_post != new_post:
        print("New post alert!")
