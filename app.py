
import requests
import smtplib
from email.mime.text import MIMEText
import threading
import time

# Define the API URL
api_url = "https://flowise.oschlo.ai/api/v1/prediction/a8f1c4de-87f2-4a9e-b857-52fa44ad0998"

# Define the question payload
payload = {
    "question": "hvem jobber i Oschlo"
}

# Function to send the alert
def send_alert():
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    subject = "Flowise Alert: Oschlo Response Issue"
    body = "Jeg har ikke informasjon om hvem som jobber i Oschlo akkurat nå. Please restart the service."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, os.getenv("EMAIL_PASSWORD"))
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Alert email sent!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to check the response from the API
def check_flowise_response():
    try:
        response = requests.post(api_url, json=payload)
        response_data = response.json()
        answer = response_data.get("response", "")

        if "Jeg har ikke informasjon om hvem som jobber i Oschlo akkurat nå." in answer:
            print("Alert condition met!")
            send_alert()
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
