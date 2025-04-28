import smtplib
import imaplib
import email
from email.utils import parsedate_to_datetime, parseaddr
from email.message import EmailMessage
from typing import List, Tuple
import ssl

# Gmail SMTP and IMAP settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
IMAP_SERVER = "imap.gmail.com"


def authenticate_email(gmail_address: str, app_password: str):
    """Authenticate Gmail SMTP and IMAP using app password (not regular password)."""
    try:
        smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp_server.starttls(context=ssl.create_default_context())
        smtp_server.login(gmail_address, app_password)

        imap_server = imaplib.IMAP4_SSL(IMAP_SERVER)
        imap_server.login(gmail_address, app_password)

        return smtp_server, imap_server
    except Exception as e:
        print("Authentication failed:", str(e))
        return None, None


def send_recommendations(
    smtp_server,
    sender_email: str,
    recipient_emails: List[str],
    subject: str,
    recommendation_text: str,
    attachments: List[Tuple[str, bytes]] = None,
):
    """
    Send an email with paper recommendations.
    Attachments should be a list of (filename, file_bytes) tuples.
    """
    for recipient in recipient_emails:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient
        msg.set_content(recommendation_text)

        if attachments:
            for filename, file_data in attachments:
                msg.add_attachment(
                    file_data, maintype="application", subtype="octet-stream", filename=filename
                )

        try:
            smtp_server.send_message(msg)
            print(f"Sent recommendation to {recipient}")
        except Exception as e:
            print(f"Failed to send email to {recipient}:", str(e))

def fetch_feedback(imap_server, folder="INBOX", keyword="Liked Papers", limit=10):
    """
    Check inbox for feedback emails. Returns a list of (sender_email, subject, body, received_time) tuples.
    Filters emails by checking if the first line of the body starts with 'Liked Papers'.
    Includes both seen and unseen emails.
    """
    feedback = []
    try:
        imap_server.select(folder)
        result, data = imap_server.search(None, 'ALL')  # Fetch both seen and unseen emails

        if result != "OK":
            print("No messages found!")
            return feedback

        email_ids = data[0].split()[-limit:]  # Get the latest 'limit' emails

        for eid in email_ids:
            res, msg_data = imap_server.fetch(eid, "(RFC822)")
            if res != "OK":
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            sender = msg["From"]
            subject = msg["Subject"]
            date = msg["Date"]
            received_time = parsedate_to_datetime(date) if date else None
            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and not part.get('Content-Disposition'):
                        body += part.get_payload(decode=True).decode(errors="replace")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="replace")

            first_line = body.strip().splitlines()[0] if body.strip() else ""

            if first_line.strip().startswith(keyword):
                feedback.append((sender, subject, body, received_time))

    except Exception as e:
        print("Error fetching feedback:", str(e))

    return feedback