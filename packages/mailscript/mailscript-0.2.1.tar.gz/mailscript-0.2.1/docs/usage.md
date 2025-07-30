# MailScript Usage Guide

This guide provides detailed instructions on how to use the MailScript package for sending emails.

## Table of Contents

- [Basic Setup](#basic-setup)
- [Sending Simple Emails](#sending-simple-emails)
- [HTML Emails](#html-emails)
- [Working with Templates](#working-with-templates)
- [Adding Attachments](#adding-attachments)
- [Using CC and BCC](#using-cc-and-bcc)
- [Email Validation](#email-validation)
- [Error Handling](#error-handling)
- [Advanced Configuration](#advanced-configuration)

## Basic Setup

First, install the package:

```bash
pip install mailscript
```

Then create a `Mailer` instance with your SMTP server details:

```python
from mailscript import Mailer

mailer = Mailer(
    smtp_host="smtp.example.com",  # Your SMTP server host
    smtp_port=587,                 # SMTP port (commonly 587 for TLS, 465 for SSL)
    smtp_user="your-email@example.com",
    smtp_password="your-password",
    use_tls=True,                  # Use False for no encryption or if using port 465
    timeout=60                     # Connection timeout in seconds (optional)
)
```

Common SMTP providers:
- Gmail: `smtp.gmail.com` (port 587)
- Outlook/Office 365: `smtp.office365.com` (port 587)
- Yahoo: `smtp.mail.yahoo.com` (port 587)
- Amazon SES: `email-smtp.us-east-1.amazonaws.com` (port 587, region may vary)

## Sending Simple Emails

To send a plain text email:

```python
mailer.send(
    sender="your-email@example.com",
    recipients="recipient@example.com",  # Can also be a list of emails
    subject="Hello from MailScript",
    body="This is a test email sent using MailScript."
)
```

## HTML Emails

To send an HTML email, set the `is_html` parameter to `True`:

```python
html_content = """
<!DOCTYPE html>
<html>
<body>
    <h1>Hello from MailScript</h1>
    <p>This is an <b>HTML</b> email with <span style="color: blue;">styled text</span>!</p>
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

## Working with Templates

### Using the Template Renderer

You can use the built-in template renderer to create dynamic emails using Jinja2 templates:

```python
from mailscript.templates import TemplateRenderer

# Create a renderer
renderer = TemplateRenderer()

# Define your template string
template = """
<html>
<body>
    <h1>Hello, {{ name }}!</h1>
    <p>Welcome to {{ company }}.</p>
    <p>Your account was created on {{ date }}.</p>
    <ul>
        {% for feature in features %}
        <li>{{ feature }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

# Define context variables
context = {
    "name": "John",
    "company": "Example Corp",
    "date": "2025-06-05",
    "features": ["Templates", "Attachments", "HTML Support"]
}

# Render the template
html_content = renderer.render_from_string(template, context)

# Send the email
mailer.send(
    sender="your-email@example.com",
    recipients="recipient@example.com",
    subject="Welcome Email",
    body=html_content,
    is_html=True
)
```

### Using Template Files

You can store templates in files and render them:

```python
# Create a renderer with a template directory
renderer = TemplateRenderer(template_folder="path/to/templates")

# Render from a template file
html_content = renderer.render_from_file("welcome.html", context)
```

### Simplified Template Methods

MailScript provides convenience methods for sending templated emails directly:

```python
# Using a template string
mailer.send_template(
    sender="your-email@example.com",
    recipients="recipient@example.com",
    subject="Welcome Email",
    template_string="<h1>Welcome, {{ name }}!</h1><p>{{ message }}</p>",
    context={"name": "John", "message": "Thank you for signing up!"},
    is_html=True
)

# Using a template file
mailer.send_template_file(
    sender="your-email@example.com",
    recipients="recipient@example.com",
    subject="Newsletter",
    template_name="newsletter.html",
    template_folder="path/to/templates",
    context={"name": "John", "month": "June"},
    is_html=True
)
```

## Adding Attachments

To add file attachments to your emails:

```python
# Single attachment
with open("document.pdf", "rb") as f:
    attachments = {"document.pdf": f}
    
    mailer.send(
        sender="your-email@example.com",
        recipients="recipient@example.com",
        subject="Document Attached",
        body="Please find the attached document.",
        attachments=attachments
    )

# Multiple attachments
with open("document.pdf", "rb") as pdf, open("image.jpg", "rb") as img:
    attachments = {
        "document.pdf": pdf,
        "image.jpg": img
    }
    
    mailer.send(
        sender="your-email@example.com",
        recipients="recipient@example.com",
        subject="Files Attached",
        body="Please find the attached files.",
        attachments=attachments
    )
```

## Using CC and BCC

To include CC and BCC recipients:

```python
mailer.send(
    sender="your-email@example.com",
    recipients="primary@example.com",
    subject="Meeting Reminder",
    body="Don't forget our meeting tomorrow!",
    cc="manager@example.com",  # Can also be a list of emails
    bcc=["records@example.com", "backup@example.com"]
)
```

## Email Validation

By default, MailScript validates email addresses before sending. You can disable this:

```python
# With validation disabled
mailer.send(
    sender="your-email@example.com",
    recipients="recipient@example.com",
    subject="Test Email",
    body="This is a test.",
    validate_deliverability=False
)

# Manual validation
is_valid = mailer.validate_email("test@example.com")
print(f"Email is valid: {is_valid}")
```

## Error Handling

Handle potential errors when sending emails:

```python
try:
    mailer.send(
        sender="your-email@example.com",
        recipients="recipient@example.com",
        subject="Test Email",
        body="This is a test."
    )
    print("Email sent successfully!")
    
except ValueError as e:
    print(f"Validation error: {e}")
    
except ConnectionError as e:
    print(f"SMTP connection error: {e}")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Advanced Configuration

### Custom Template Filters

You can add custom filters to your templates:

```python
from mailscript.templates import TemplateRenderer

renderer = TemplateRenderer()

# Add a custom filter
def uppercase(value):
    return value.upper()

renderer.add_filter("uppercase", uppercase)

# Use in template
template = "Hello {{ name | uppercase }}!"
result = renderer.render_from_string(template, {"name": "john"})
# Result: "Hello JOHN!"
```

### Add Global Variables

Add global variables that are available in all templates:

```python
import datetime

renderer = TemplateRenderer()

# Add global variables
renderer.add_global("app_name", "MyApp")
renderer.add_global("current_year", datetime.datetime.now().year)

# Use in template
template = "Welcome to {{ app_name }}! © {{ current_year }}"
result = renderer.render_from_string(template, {})
# Result: "Welcome to MyApp! © 2025"
```

### Setting Reply-To Address

Set a different reply-to address:

```python
mailer.send(
    sender="no-reply@example.com",
    recipients="customer@example.com",
    subject="Your Order Confirmation",
    body="Thank you for your order!",
    reply_to="support@example.com"  # Replies will go to this address
)
```