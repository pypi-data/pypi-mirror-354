"""
Configuration template for MailScript.

This template should be copied outside the package directory and filled with your credentials.
DO NOT include sensitive credentials in the package directory.
"""

# Email credentials
# SMTP settings for sending emails
smtp_config = {
    "username": "your-email@example.com",
    "password": "your-password",  # Use an app password if 2FA is enabled
    "host": "smtp.example.com", 
    "port": 587,
    "use_tls": True
}

# IMAP settings for receiving emails
imap_config = {
    "username": "your-email@example.com",
    "password": "your-password",  # Use an app password if 2FA is enabled
    "host": "imap.example.com",
    "port": 993
}

# Default recipient for testing
default_recipient = "recipient@example.com"
