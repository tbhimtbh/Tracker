import requests
import hashlib
import time

# Prompt user for Facebook profile ID
profile_id = input("Enter the Facebook profile ID to monitor: ")

# Construct the URL to monitor
url = f"https://www.facebook.com/profile.php?id={profile_id}"

# Use a hash of the page content to detect changes
hash_old = ""

# Continuously scrape the page
while True:
    # Make a request to the URL
    response = requests.get(url)

    # Compute the hash of the response content
    hash_new = hashlib.sha256(response.content).hexdigest()

    # If the hash has changed, alert the user
    if hash_new != hash_old:
        print("ALERT: The page has changed!")
        hash_old = hash_new

    # If the hash has not changed, indicate that the program is still running
    else:
        print("Scraping... Tracking...")
    
    # Wait for 5 seconds before scraping again
    time.sleep(5)
