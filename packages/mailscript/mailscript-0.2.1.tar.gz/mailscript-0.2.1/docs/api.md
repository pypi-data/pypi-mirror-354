---
layout: default
title: MailScript API Reference
description: Detailed documentation of the MailScript library API
---

# MailScript API Reference

## Mailer Class

The `Mailer` class is the primary interface for sending emails.

### Constructor

```python
Mailer(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    use_tls: bool = True,
    timeout: int = 60
)
```

**Parameters:**
- `smtp_host`: SMTP server hostname
- `smtp_port`: SMTP server port number
- `smtp_user`: Username for SMTP authentication
- `smtp_password`: Password for SMTP authentication
- `use_tls`: Whether to use TLS encryption (default: True)
- `timeout`: Connection timeout in seconds (default: 60)

### Methods

#### send

```python
def send(
    self,
    sender: str,
    recipients: Union[str, List[str]],
    subject: str,
    body: str,
    cc: Union[str, List[str]] = None,
    bcc: Union[str, List[str]] = None,
    reply_to: Union[str, List[str]] = None,
    attachments: Dict[str, BinaryIO] = None,
    is_html: bool = False,
    headers: Dict[str, str] = None
) -> bool:
```

Sends an email with the specified parameters.

**Parameters:**
- `sender`: Email address of the sender
- `recipients`: Email addresses of the recipients (string or list)
- `subject`: Email subject
- `body`: Email body content (plain text or HTML)
- `cc`: Carbon copy recipients (string or list, optional)
- `bcc`: Blind carbon copy recipients (string or list, optional)
- `reply_to`: Reply-to addresses (string or list, optional)
- `attachments`: Dictionary of attachment filenames and file objects
- `is_html`: Whether the body content is HTML (default: False)
- `headers`: Additional headers to include in the email

**Returns:**
- `bool`: True if the email was sent successfully

#### send_template

```python
def send_template(
    self,
    sender: str,
    recipients: Union[str, List[str]],
    subject: str,
    template_string: str,
    context: Dict[str, Any],
    cc: Union[str, List[str]] = None,
    bcc: Union[str, List[str]] = None,
    reply_to: Union[str, List[str]] = None,
    attachments: Dict[str, BinaryIO] = None,
    is_html: bool = True,
    headers: Dict[str, str] = None
) -> bool:
```

Sends an email using a template string.

**Parameters:**
- `sender`: Email address of the sender
- `recipients`: Email addresses of the recipients
- `subject`: Email subject
- `template_string`: Template string to render
- `context`: Dictionary of variables to use in template rendering
- `cc`, `bcc`, `reply_to`, `attachments`, `is_html`, `headers`: Same as in `send()`

**Returns:**
- `bool`: True if the email was sent successfully

#### send_template_file

```python
def send_template_file(
    self,
    sender: str,
    recipients: Union[str, List[str]],
    subject: str,
    template_name: str,
    template_folder: str,
    context: Dict[str, Any],
    cc: Union[str, List[str]] = None,
    bcc: Union[str, List[str]] = None,
    reply_to: Union[str, List[str]] = None,
    attachments: Dict[str, BinaryIO] = None,
    is_html: bool = True,
    headers: Dict[str, str] = None
) -> bool:
```

Sends an email using a template file.

**Parameters:**
- `sender`: Email address of the sender
- `recipients`: Email addresses of the recipients
- `subject`: Email subject
- `template_name`: Filename of the template
- `template_folder`: Directory containing the template file
- `context`: Dictionary of variables to use in template rendering
- `cc`, `bcc`, `reply_to`, `attachments`, `is_html`, `headers`: Same as in `send()`

**Returns:**
- `bool`: True if the email was sent successfully

## Receiver Class

The `Receiver` class is used for retrieving and processing emails from an IMAP server.

### Constructor

```python
Receiver(
    imap_host: str,
    imap_port: int,
    username: str,
    password: str
)
```

**Parameters:**
- `imap_host`: IMAP server hostname
- `imap_port`: IMAP server port number
- `username`: Username for IMAP authentication
- `password`: Password for IMAP authentication

### Methods

#### connect

```python
def connect(self) -> bool:
```

Connects to the IMAP server.

**Returns:**
- `bool`: True if the connection was successful

#### select_mailbox

```python
def select_mailbox(self, mailbox: str = "INBOX") -> int:
```

Selects a mailbox (folder) on the IMAP server.

**Parameters:**
- `mailbox`: Mailbox name to select (default: "INBOX")

**Returns:**
- `int`: Number of messages in the mailbox

#### fetch_emails

```python
def fetch_emails(
    self,
    count: int = 10,
    criteria: str = "ALL",
    save_attachments: bool = False,
    output_dir: str = "./attachments",
    fetch_body: bool = True
) -> List[Dict[str, Any]]:
```

Fetches emails from the selected mailbox.

**Parameters:**
- `count`: Number of emails to fetch (default: 10)
- `criteria`: Search criteria for emails (default: "ALL")
- `save_attachments`: Whether to save attachments to disk (default: False)
- `output_dir`: Directory to save attachments (default: "./attachments")
- `fetch_body`: Whether to fetch the email body (default: True)

**Returns:**
- List of dictionaries containing email data

#### logout

```python
def logout(self) -> bool:
```

Disconnects from the IMAP server.

**Returns:**
- `bool`: True if the logout was successful

## TemplateRenderer Class

The `TemplateRenderer` class provides functionality to render templates using Jinja2.

### Constructor

```python
TemplateRenderer()
```

### Methods

#### render_from_string

```python
def render_from_string(self, template_string: str, context: Dict[str, Any]) -> str:
```

Renders a template from a string.

**Parameters:**
- `template_string`: Template string to render
- `context`: Dictionary of variables to use in rendering

**Returns:**
- `str`: Rendered template as a string

#### render_from_file

```python
def render_from_file(
    self,
    template_name: str,
    template_folder: str,
    context: Dict[str, Any]
) -> str:
```

Renders a template from a file.

**Parameters:**
- `template_name`: Filename of the template
- `template_folder`: Directory containing the template file
- `context`: Dictionary of variables to use in rendering

**Returns:**
- `str`: Rendered template as a string

## Credentials Utility Functions

### get_smtp_config

```python
get_smtp_config() -> Dict[str, Any]
```

Loads SMTP configuration from config files.

**Returns:**
- Dictionary containing SMTP configuration

### get_imap_config

```python
get_imap_config() -> Dict[str, Any]
```

Loads IMAP configuration from config files.

**Returns:**
- Dictionary containing IMAP configuration
