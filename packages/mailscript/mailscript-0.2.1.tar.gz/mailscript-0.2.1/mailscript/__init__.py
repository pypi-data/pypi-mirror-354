"""
MailScript - A Python library for simplified email sending and receiving.

This package provides tools to easily send and receive emails with support for:
- Plain text and HTML emails
- Template rendering
- File attachments
- Email validation
- Email retrieval from IMAP servers
"""

__version__ = "0.2.1"

from .mailer import Mailer
from .receiver import Receiver

__all__ = ["Mailer", "Receiver"]
