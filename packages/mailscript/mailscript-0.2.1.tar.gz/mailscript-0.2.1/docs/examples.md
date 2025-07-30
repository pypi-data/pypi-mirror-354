---
layout: default
title: MailScript Examples
description: Code examples demonstrating how to use the MailScript library
---

# MailScript Examples

This page provides various code examples to help you get started with MailScript.

## Sending Emails

### Basic Email

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

### HTML Email

```python
# Send an HTML email
html_content = """
<!DOCTYPE html>
<html>
<body>
    <h1>Hello from MailScript</h1>
    <p>This is an <b>HTML</b> email!</p>
</body>
</html>
"""

mailer.send(
    sender="your-email@example.com",
    recipients="recipient@example.com",
    subject="HTML Email Test",
    body=html_content,
    is_html=True
)
```

### With CC and BCC Recipients

```python
# Send email with CC and BCC recipients
mailer.send(
    sender="your-email@example.com",
    recipients="main-recipient@example.com",
    cc=["cc-recipient1@example.com", "cc-recipient2@example.com"],
    bcc="bcc-recipient@example.com",
    subject="Email with CC and BCC",
    body="This email has CC and BCC recipients."
)
```

## Templates

### Using Template Strings

```python
from mailscript.templates import TemplateRenderer

# Initialize renderer
renderer = TemplateRenderer()

# Render template from string
template = """
<h1>Hello, {{ name }}!</h1>
<p>Welcome to {{ company }}.</p>
"""

context = {"name": "John", "company": "Example Corp"}
html_content = renderer.render_from_string(template, context)

# Send templated email
mailer.send(
    sender="your-email@example.com",
    recipients="recipient@example.com",
    subject="Welcome Email",
    body=html_content,
    is_html=True
)
```

### Using the Simplified Template Methods

```python
# Send an email using a template string directly
context = {
    "name": "John", 
    "features": ["Templates", "Attachments", "HTML Support"]
}

mailer.send_template(
    sender="your-email@example.com",
    recipients="recipient@example.com",
    subject="Welcome Email",
    template_string="<h1>Welcome, {{ name }}!</h1><ul>{% for feature in features %}<li>{{ feature }}</li>{% endfor %}</ul>",
    context=context,
    is_html=True
)

# Send an email using a template file
mailer.send_template_file(
    sender="your-email@example.com",
    recipients="recipient@example.com",
    subject="Newsletter",
    template_name="newsletter.html",
    template_folder="/path/to/templates",
    context={"name": "John", "month": "June"},
    is_html=True
)
```

## Attachments

```python
# Send email with attachment
with open("document.pdf", "rb") as f:
    attachments = {"document.pdf": f}
    
    mailer.send(
        sender="your-email@example.com",
        recipients="recipient@example.com",
        subject="Email with attachment",
        body="Please find the attached document.",
        attachments=attachments
    )
```

## Receiving Emails

```python
from mailscript import Receiver

# Initialize receiver
receiver = Receiver(
    imap_host="imap.example.com", 
    imap_port=993,
    username="your-email@example.com", 
    password="your-password"
)

# Connect to the server
receiver.connect()

# Select mailbox
receiver.select_mailbox("INBOX")

# Fetch recent emails
emails = receiver.fetch_emails(
    count=5,                          # Number of recent emails to retrieve
    save_attachments=True,            # Save attachments to disk
    output_dir="./my_attachments"     # Directory to save attachments
)

# Process emails
for email in emails:
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
    print(f"Date: {email['date']}")
    print(f"Body: {email['body'][:100]}...")  # Print first 100 chars
    
    # Process attachments
    for attachment in email['attachments']:
        print(f"Attachment: {attachment['filename']}")
        print(f"Saved at: {attachment['saved_path']}")
    
    print("---")

# Always logout when done
receiver.logout()
```

## Command Line Interface Examples

### Sending Emails from Command Line

```bash
# Send a plain text email
python -m mailscript send --host smtp.example.com --port 587 --user user@example.com \
    --from "Sender <sender@example.com>" --to recipient@example.com \
    --subject "Hello" --body "This is a test email"

# Send an HTML email with attachments
python -m mailscript send --host smtp.example.com --port 587 --user user@example.com \
    --from "Sender <sender@example.com>" --to recipient@example.com \
    --subject "Hello" --body-file email.html --html --attach document.pdf image.jpg
```

### Receiving Emails from Command Line

```bash
# Retrieve 10 recent emails and display them
python -m mailscript receive --host imap.example.com --port 993 --user user@example.com \
    --count 10

# Retrieve emails and save attachments
python -m mailscript receive --host imap.example.com --port 993 --user user@example.com \
    --count 5 --save-attachments --output-dir ./downloads

# Save email data to a JSON file
python -m mailscript receive --host imap.example.com --port 993 --user user@example.com \
    --output-file emails.json
```
