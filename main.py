import imaplib
import email
import webbrowser
import time
import requests

# Read input from input.txt
with open("input.txt", "r") as f:
    lines = f.readlines()
    email_address = lines[0].strip()
    email_password = lines[1].strip()
    discord_token = lines[2].strip()

# IMAP settings
imap_server = "imap.gmail.com"  # or imap.outlook.com, etc.
imap_port = 993

# Log in to IMAP server
mail = imaplib.IMAP4_SSL(imap_server, imap_port)
mail.login(email_address, email_password)
mail.select("inbox")

# Search for the verification email
status, response = mail.search(None, "(UNSEEN SUBJECT \"Discord Email Verification\")")
unread_msgs = response[0].split()

# Parse the verification email
for num in unread_msgs:
    status, response = mail.fetch(num, "(RFC822)")
    raw_message = response[1]
    message = email.message_from_bytes(raw_message)
    for part in message.walk():
        if part.get_content_type() == "text/html":
            html_content = part.get_payload(decode=True)
            break

# Extract the verification link
import re
pattern = r"https://discord\.com/verify/[a-zA-Z0-9]+"
match = re.search(pattern, html_content.decode("utf-8"))
if match:
    verification_link = match.group(0)
    print("Verification link:", verification_link)
else:
    print("Verification link not found.")
    exit(1)

# Open the verification link in a browser
webbrowser.open(verification_link)

# Wait for the user to verify the email address
print("Please verify your email address in the browser.")
time.sleep(30)  # wait for 30 seconds

# Verify the email address using the Discord API
url = "https://discord.com/api/v9/users/@me"
headers = {
    "Authorization": f"Bearer {discord_token}",
    "Content-Type": "application/json"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    user_data = response.json()
    if user_data["verified"]:
        print("Email address verified successfully!")
    else:
        print("Email address not verified yet.")
else:
    print("Error verifying email address:", response.text)
