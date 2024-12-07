import smtplib
from email.mime.text import MIMEText
from django.conf import settings

# Use more secure authentication methods
# Consider using OAuth 2.0 or app-specific passwords
def email_server():
    smtp_server = 'smtp.office365.com'
    smtp_port = 587  # TLS port
    username = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD

    # Ensure you're using TLS
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)