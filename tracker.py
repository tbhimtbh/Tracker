import requests
import time

def get_fb_page(profile_id):
    url = f"https://www.facebook.com/profile.php?id={profile_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
    response = requests.get(url, headers=headers)
    return response.text

profile_id = input("Enter the profile ID you want to check: ")
previous_data = get_fb_page(profile_id)

while True:
    current_data = get_fb_page(profile_id)
    if current_data != previous_data:
        print("ALERT: A new post has been added!")
        previous_data = current_data
    time.sleep(60)
