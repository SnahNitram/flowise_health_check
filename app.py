import requests
import os
import threading
import time

# Load environment variables for the API URL and Slack webhook
api_url = os.getenv("FLOWISE_API_URL")
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

# Define the question payload
payload = {
    "question": "hvem jobber i Oschlo"
}

# Function to send an alert to Slack via webhook
def send_slack_alert():
    message = {
        "text": "Jeg har ikke informasjon om hvem som jobber i Oschlo akkurat nå. Please restart the service."
    }
    
    try:
        response = requests.post(slack_webhook_url, json=message)
        if response.status_code == 200:
            print("Slack alert sent successfully!")
        else:
            print(f"Failed to send alert. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending Slack alert: {e}")

# Function to check the response from the API
def check_flowise_response():
    try:
        response = requests.post(api_url, json=payload)
        response_data = response.json()
        answer = response_data.get("response", "")

        if "Jeg har ikke informasjon om hvem som jobber i Oschlo akkurat nå." in answer:
            print("Alert condition met!")
            send_slack_alert()
        else:
            print("Service is working as expected.")
    except Exception as e:
        print(f"Error during API request: {e}")

# Function to run the check at regular intervals
def run_scheduler():
    while True:
        check_flowise_response()
        time.sleep(1800)  # Runs every 30 minutes

# Start the scheduler
if __name__ == "__main__":
    run_scheduler()
