---
layout: default
title: MailScript Documentation
description: A Python library for simplified email sending and receiving with support for templates, attachments, and more.
---

# MailScript

**Current Version: 0.2.1**

A Python library for simplified email sending and receiving with support for templates, attachments, and more.

## Overview

MailScript provides an easy-to-use interface for sending and receiving emails in Python applications. Whether you need to send a simple text email, create beautiful HTML templates, or process incoming messages, MailScript has you covered.

## Features

- 📧 **Simple Email Sending**: Send plain text and HTML emails with just a few lines of code
- 📝 **Template Support**: Create dynamic emails using Jinja2 templates
- 📎 **Attachments**: Easily add file attachments to your emails
- 📬 **Email Receiving**: Fetch and process incoming emails via IMAP
- 🔄 **Command Line Interface**: Send and receive emails directly from your terminal
- ✅ **Address Validation**: Validate email addresses before sending
- 🔒 **TLS/SSL Support**: Secure your email transmissions

## Installation

```bash
pip install mailscript
```

## Quick Links

- [Usage Guide](usage.md): Comprehensive guide to using MailScript
- [Examples](examples.md): Code examples showing common use cases
- [API Reference](api.md): Detailed API documentation
- [GitHub Repository](https://github.com/rakshithkalmadi/mailscript): View source code and contribute


## Quick Start

```python
from mailscript import Mailer

# Initialize mailer
mailer = Mailer(
    smtp_host="smtp.example.com", 
    smtp_port=587,
    smtp_user="your-email@example.com",
    smtp_password="your-password",
    use_tls=True
)

# Send a simple email
mailer.send(
    sender="your-email@example.com",
    recipients="recipient@example.com",
    subject="Hello from MailScript",
    body="This is a test email from MailScript."
)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
