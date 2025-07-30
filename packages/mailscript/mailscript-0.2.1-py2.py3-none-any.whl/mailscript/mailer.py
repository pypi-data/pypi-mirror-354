"""
Core mailer module for MailScript.

This module provides the main Mailer class for creating and sending emails.
"""

import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr
from typing import Union, List, Dict, Optional, BinaryIO, Any

from .templates import TemplateRenderer


class Mailer:
    """
    A class for creating and sending emails.
    
    This class provides methods to create email messages with plain text or HTML content,
    add attachments, and send emails via SMTP.
    """
    
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        use_tls: bool = True,
        timeout: int = 60,
    ):
        """
        Initialize a new Mailer instance.
        
        Args:
            smtp_host: SMTP server hostname
            smtp_port: SMTP server port
            smtp_user: SMTP username
            smtp_password: SMTP password
            use_tls: Whether to use TLS for the connection (default: True)
            timeout: Connection timeout in seconds (default: 60)
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.use_tls = use_tls
        self.timeout = timeout
        
    def validate_email(self, email: str) -> bool:
        """
        Validate an email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            bool: True if the email format is valid, False otherwise
        """
        # Simple email regex validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
        
    def create_message(
        self,
        sender: str,
        recipients: Union[str, List[str]],
        subject: str,
        body: str,
        is_html: bool = False,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[str] = None,
        attachments: Optional[Dict[str, BinaryIO]] = None,
        validate_deliverability: bool = True,
    ) -> MIMEMultipart:
        """
        Create an email message.
        
        Args:
            sender: Sender email address
            recipients: Recipient email address(es)
            subject: Email subject
            body: Email body content
            is_html: Whether the body content is HTML (default: False)
            cc: Carbon copy recipients
            bcc: Blind carbon copy recipients
            reply_to: Reply-to email address
            attachments: Dictionary of attachment filenames and file objects
            validate_deliverability: Whether to validate email addresses
            
        Returns:
            MIMEMultipart: The created email message
            
        Raises:
            ValueError: If an email address validation fails
        """
        # Validate email addresses if required
        if validate_deliverability:
            if not self.validate_email(sender):
                raise ValueError(f"Invalid sender email address: {sender}")
                
            # Validate recipients
            if isinstance(recipients, str):
                if not self.validate_email(recipients):
                    raise ValueError(f"Invalid recipient email address: {recipients}")
            else:
                for recipient in recipients:
                    if not self.validate_email(recipient):
                        raise ValueError(f"Invalid recipient email address: {recipient}")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender
        
        # Handle recipient list
        if isinstance(recipients, list):
            msg['To'] = ', '.join(recipients)
        else:
            msg['To'] = recipients
            
        msg['Subject'] = subject
        
        # Add CC recipients if provided
        if cc:
            if isinstance(cc, list):
                msg['Cc'] = ', '.join(cc)
            else:
                msg['Cc'] = cc
                
        # Add BCC recipients if provided (These won't be visible in the header)
        if bcc:
            if isinstance(bcc, list):
                msg['Bcc'] = ', '.join(bcc)
            else:
                msg['Bcc'] = bcc
                
        # Add Reply-To if provided
        if reply_to:
            msg['Reply-To'] = reply_to
            
        # Attach body with appropriate content type
        content_type = 'html' if is_html else 'plain'
        msg.attach(MIMEText(body, content_type))
        
        # Add attachments if provided
        if attachments:
            for filename, fileobj in attachments.items():
                part = MIMEApplication(fileobj.read(), Name=filename)
                part['Content-Disposition'] = f'attachment; filename="{filename}"'
                msg.attach(part)
                
        return msg
        
    def send(
        self,
        sender: str,
        recipients: Union[str, List[str]],
        subject: str,
        body: str,
        is_html: bool = False,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[str] = None,
        attachments: Optional[Dict[str, BinaryIO]] = None,
        validate_deliverability: bool = True,
    ) -> bool:
        """
        Create and send an email.
        
        Args:
            sender: Sender email address
            recipients: Recipient email address(es)
            subject: Email subject
            body: Email body content
            is_html: Whether the body content is HTML (default: False)
            cc: Carbon copy recipients
            bcc: Blind carbon copy recipients
            reply_to: Reply-to email address
            attachments: Dictionary of attachment filenames and file objects
            validate_deliverability: Whether to validate email addresses
            
        Returns:
            bool: True if the email was sent successfully
            
        Raises:
            ValueError: If an email validation fails
            ConnectionError: If connection to the SMTP server fails
            smtplib.SMTPException: If there's an error sending the email
        """
        # Create the message
        msg = self.create_message(
            sender=sender,
            recipients=recipients,
            subject=subject,
            body=body,
            is_html=is_html,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            attachments=attachments,
            validate_deliverability=validate_deliverability,
        )
        
        # Prepare recipient list
        all_recipients = []
        
        # Add To recipients
        if isinstance(recipients, list):
            all_recipients.extend(recipients)
        else:
            all_recipients.append(recipients)
            
        # Add CC recipients if provided
        if cc:
            if isinstance(cc, list):
                all_recipients.extend(cc)
            else:
                all_recipients.append(cc)
                
        # Add BCC recipients if provided
        if bcc:
            if isinstance(bcc, list):
                all_recipients.extend(bcc)
            else:
                all_recipients.append(bcc)
        
        # Send the email
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=self.timeout) as server:
                if self.use_tls:
                    server.starttls()
                    
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(sender, all_recipients, msg.as_string())
                
            return True
            
        except (smtplib.SMTPException, OSError) as e:
            # Re-raise with more context
            raise ConnectionError(f"Failed to send email: {str(e)}")
            
    def send_template(
        self,
        sender: str,
        recipients: Union[str, List[str]],
        subject: str,
        template_string: str,
        context: Dict[str, Any],
        is_html: bool = True,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[str] = None,
        attachments: Optional[Dict[str, BinaryIO]] = None,
        validate_deliverability: bool = True,
    ) -> bool:
        """
        Render a template string and send it as an email.
        
        Args:
            sender: Sender email address
            recipients: Recipient email address(es)
            subject: Email subject
            template_string: Template string to render
            context: Template context variables
            is_html: Whether the template is HTML (default: True)
            cc: Carbon copy recipients
            bcc: Blind carbon copy recipients
            reply_to: Reply-to email address
            attachments: Dictionary of attachment filenames and file objects
            validate_deliverability: Whether to validate email addresses
            
        Returns:
            bool: True if the email was sent successfully
            
        Raises:
            ValueError: If an email validation fails
            ConnectionError: If connection to the SMTP server fails
            smtplib.SMTPException: If there's an error sending the email
        """
        # Create a template renderer
        renderer = TemplateRenderer()
        
        # Render the template
        body = renderer.render_from_string(template_string, context)
        
        # Send the email
        return self.send(
            sender=sender,
            recipients=recipients,
            subject=subject,
            body=body,
            is_html=is_html,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            attachments=attachments,
            validate_deliverability=validate_deliverability,
        )
        
    def send_template_file(
        self,
        sender: str,
        recipients: Union[str, List[str]],
        subject: str,
        template_name: str,
        template_folder: str,
        context: Dict[str, Any],
        is_html: bool = True,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[str] = None,
        attachments: Optional[Dict[str, BinaryIO]] = None,
        validate_deliverability: bool = True,
    ) -> bool:
        """
        Render a template from a file and send it as an email.
        
        Args:
            sender: Sender email address
            recipients: Recipient email address(es)
            subject: Email subject
            template_name: Name of the template file
            template_folder: Path to the folder containing templates
            context: Template context variables
            is_html: Whether the template is HTML (default: True)
            cc: Carbon copy recipients
            bcc: Blind carbon copy recipients
            reply_to: Reply-to email address
            attachments: Dictionary of attachment filenames and file objects
            validate_deliverability: Whether to validate email addresses
            
        Returns:
            bool: True if the email was sent successfully
            
        Raises:
            ValueError: If an email validation fails
            ConnectionError: If connection to the SMTP server fails
            smtplib.SMTPException: If there's an error sending the email
            jinja2.exceptions.TemplateNotFound: If template file not found
        """
        # Create a template renderer with the template folder
        renderer = TemplateRenderer(template_folder)
        
        # Render the template
        body = renderer.render_from_file(template_name, context)
        
        # Send the email
        return self.send(
            sender=sender,
            recipients=recipients,
            subject=subject,
            body=body,
            is_html=is_html,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            attachments=attachments,
            validate_deliverability=validate_deliverability,
        )
