import requests
import time
import os
import smtplib
from email.mime.text import MIMEText

FB_API_URL = 'https://graph.facebook.com/v12.0/'
USER_ID = '<enter user id here>'
ACCESS_TOKEN = '<enter access token here>'
MONITOR_INTERVAL = 60  # seconds

# email settings
import smtplib

def send_notification(message):
    """
    Send a notification via email using Gmail.
    """
    sender_email = "your_gmail_address@gmail.com"
    sender_password = "your_gmail_password"
    recipient_email = "recipient_email_address"

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)

            subject = "Facebook profile update"
            body = message

            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(sender_email, recipient_email, msg)
            
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Error sending notification: {e}")



def monitor_user_profile():
    """
    Monitor the user's Facebook profile for updates and send a notification when a new update is detected.
    """
    url = f'{FB_API_URL}{USER_ID}?fields=updated_time&access_token={ACCESS_TOKEN}'
    last_updated_time = None
    last_post_time = None

    while True:
        try:
            # check profile update
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            updated_time_str = data['updated_time']
            updated_time = time.strptime(updated_time_str, '%Y-%m-%dT%H:%M:%S+0000')
            
            if last_updated_time is None or updated_time > last_updated_time:
                message = f'The user updated their profile at {updated_time_str}'
                send_email('Facebook Profile Update', message)
                last_updated_time = updated_time
            
            # check for new post
            post_url = f'{FB_API_URL}{USER_ID}/feed?access_token={ACCESS_TOKEN}'
            post_response = requests.get(post_url)
            post_response.raise_for_status()
            post_data = post_response.json()
            new_post_time = time.strptime(post_data['data'][0]['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
            
            if last_post_time is None or new_post_time > last_post_time:
                message = f'The user posted something new at {post_data["data"][0]["created_time"]}'
                send_email('New Facebook Post', message)
                last_post_time = new_post_time
                
        except requests.exceptions.HTTPError as e:
            print(f'Error monitoring user profile: {e}')

        time.sleep(MONITOR_INTERVAL)


if __name__ == '__main__':
    monitor_user_profile()
