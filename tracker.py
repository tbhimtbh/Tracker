import argparse
import requests
import time

FB_API_URL = 'https://graph.facebook.com/v16.0/'
USER_ID = ''
ACCESS_TOKEN = ''
MONITOR_INTERVAL = 60  # seconds

def send_notification(message):
    """
    Print the message to the console as a notification
    """
    print(message)

def get_user_input():
    """
    Prompt the user to enter the USER_ID and ACCESS_TOKEN
    """
    global USER_ID, ACCESS_TOKEN

    while not USER_ID:
        USER_ID = input('Enter the USER_ID you want to track: ')

    while not ACCESS_TOKEN:
        ACCESS_TOKEN = input('Enter your ACCESS_TOKEN: ')

    # validate USER_ID and ACCESS_TOKEN
    user_url = f'{FB_API_URL}{USER_ID}?access_token={ACCESS_TOKEN}&fields=name'
    try:
        response = requests.get(user_url)
        response.raise_for_status()
        data = response.json()
        user_name = data['name']
        print(f'Successfully authenticated as {user_name} ({USER_ID})')
    except requests.exceptions.HTTPError as e:
        print(f'Error validating USER_ID and ACCESS_TOKEN: {e}')
        USER_ID = ''
        ACCESS_TOKEN = ''
        get_user_input()

def monitor_user_profile():
    """
    Monitor the user's Facebook profile for updates and send a notification when a new update is detected.
    """
    global USER_ID, ACCESS_TOKEN

    last_updated_time = None
    last_post_time = None

    while True:
        try:
            # check profile update
            profile_url = f'{FB_API_URL}{USER_ID}?access_token={ACCESS_TOKEN}&fields=updated_time'
            response = requests.get(profile_url)
            response.raise_for_status()
            data = response.json()
            updated_time_str = data['updated_time']
            updated_time = time.strptime(updated_time_str, '%Y-%m-%dT%H:%M:%S+0000')

            if last_updated_time is None or updated_time > last_updated_time:
                message = f'{USER_ID} updated their profile at {updated_time_str}'
                send_notification(message)
                last_updated_time = updated_time

            # check for new post
            post_url = f'{FB_API_URL}{USER_ID}/posts?access_token={ACCESS_TOKEN}&fields=created_time'
            post_response = requests.get(post_url)
            post_response.raise_for_status()
            post_data = post_response.json()

            if 'data' in post_data and len(post_data['data']) > 0:
                new_post_time = time.strptime(post_data['data'][0]['created_time'], '%Y-%m-%dT%H:%M:%S+0000')

                if last_post_time is None or new_post_time > last_post_time:
                    message = f'{USER_ID} posted something new at {post_data["data"][0]["created_time"]}'
                    send_notification(message)
                    last_post_time = new_post_time

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 190:
                print('Invalid USER_ID or ACCESS_TOKEN. Please enter valid inputs.')
                USER_ID = ''
                ACCESS_TOKEN = ''
                get_user_input()
            else:
                print(f'Error monitoring user profile: {e}')

        time.sleep(MONITOR_INTERVAL)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-kill', action='store_true', help='Kill the monitoring process')
    args = parser.parse_args()

    if args.kill:
        # Kill the monitoring process
        pid = os.getpid()
        os.system(f'kill {pid}')
    else:
        get_user_input()
        monitor_user_profile()
