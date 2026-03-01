import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

SMTP_HOST = settings.smtp_host
SMTP_PORT = settings.smtp_port
SMTP_USER = settings.smtp_user
SMTP_PASS = settings.smtp_pass
FROM_EMAIL = settings.from_email

def send_welcome_email(to_email: str, password: str):
    print("Email function called for:", to_email)
    msg = MIMEMultipart()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = "Your account is created"

    body = f"""
Hi,

Your account has been created successfully.

Email: {to_email}
Temporary Password: {password}

Please log in and change your password immediately.

Thanks,
Your Team
    """

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)