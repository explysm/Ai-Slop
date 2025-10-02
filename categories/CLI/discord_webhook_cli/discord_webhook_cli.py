
#!/usr/bin/env python3

import requests

def send_discord_webhook():
    webhook_url = input("Enter the Discord webhook URL: ")
    message_content = input("Enter the message content: ")

    payload = {
        "content": message_content
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"Pushed '{message_content}' to '{webhook_url}'!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook: {e}")

if __name__ == "__main__":
    send_discord_webhook()
