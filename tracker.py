import requests
import time

# prompt user for Facebook ID
user_id = input("Enter Facebook ID: ")

# create URL with the user ID
url = f"https://www.facebook.com/{user_id}/"

# initialize empty set to store previous posts
prev_posts = set()

while True:
    # send GET request to the URL
    response = requests.get(url)

    # check if response is successful
    if response.status_code == 200:
        # extract all post elements from the response
        posts = response.text.split('<div class="_5pcb _4b0l _2q8l">')[1:]

        # create a set of new posts
        new_posts = set(posts) - prev_posts

        # check if there are any new posts
        if new_posts:
            # display alert message in console
            print("New post detected!")
            print(f"Number of new posts: {len(new_posts)}")

            # update the previous posts set
            prev_posts.update(new_posts)
        else:
            # display message if no new posts
            print("No new changes, continuing scrape")
    else:
        # display error message if request is unsuccessful
        print(f"Error: {response.status_code}")

    # wait for 5 seconds before scraping again
    time.sleep(5)
