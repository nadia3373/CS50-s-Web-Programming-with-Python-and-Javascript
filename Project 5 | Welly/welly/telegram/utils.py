import os, requests


BOT_TOKEN = "5158983589:AAGyTtx8Zk3LIpRLjwSjuTYnqwI3YDPkkPk"


def respond(chat, message):
    """
    Check if the received message contains any keywords, and respond accordingly.
    """
    if message.startswith('/start'): text = f"You have successfully subscribed."
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": chat, "text": text, "parse_mode": "Markdown"})