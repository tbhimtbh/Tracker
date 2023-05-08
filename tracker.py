import requests
from bs4 import BeautifulSoup
import time

url = "https://www.facebook.com/profile.php?id=100090350417345"
latest_html = None

def scrape_page():
    global latest_html
    # Make a GET request to the page
    response = requests.get(url)
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    # Find the ProfileTimeline div
    timeline = soup.find("div", {"data-pagelet": "ProfileTimeline"})
    # Check if the HTML of the ProfileTimeline div has changed since the last time we scraped the page
    if timeline and timeline.prettify() != latest_html:
        # Update the latest_html variable with the new HTML
        latest_html = timeline.prettify()
        # Return True to indicate that there is a change
        return True
    # If the HTML has not changed, return False
    return False

while True:
    # Scrape the page
    if scrape_page():
        # If there is a change, print an alert and the new HTML
        print("Profile has been updated!")
        # Wait for 1 second before sending the console message to avoid it being missed
        time.sleep(1)
    # Print a message to show that the program is still scraping every 5 seconds
    print("Scraping...")
    # Wait 5 seconds before scraping again
    time.sleep(5)
