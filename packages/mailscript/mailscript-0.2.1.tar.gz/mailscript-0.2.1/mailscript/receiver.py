"""
Email receiver module for MailScript.

This module provides the main Receiver class for fetching and processing emails.
"""

import imaplib
import email
from email.header import decode_header
import os
import json
from typing import List, Dict, Any, Optional, Union


class Receiver:
    """
    A class for retrieving and processing emails.
    
    This class provides methods to connect to an IMAP server,
    fetch emails, and extract attachments.
    """
    
    def __init__(
        self,
        imap_host: str,
        imap_port: int,
        username: str,
        password: str
    ):
        """
        Initialize the Receiver with IMAP server details.
        
        Args:
            imap_host: IMAP server hostname
            imap_port: IMAP server port
            username: Email account username
            password: Email account password
        """
        self.imap_host = imap_host
        self.imap_port = imap_port
        self.username = username
        self.password = password
        self.imap = None
    
    def connect(self) -> bool:
        """
        Connect to the IMAP server.
        
        Returns:
            bool: True if connection was successful
        """
        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
            self.imap.login(self.username, self.password)
            return True
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            return False
    
    def select_mailbox(self, mailbox: str = "INBOX") -> bool:
        """
        Select a mailbox/folder to work with.
        
        Args:
            mailbox: Name of the mailbox to select (default: "INBOX")
            
        Returns:
            bool: True if mailbox was successfully selected
        """
        if not self.imap:
            if not self.connect():
                return False
                
        status, _ = self.imap.select(mailbox)
        return status == "OK"
    
    def fetch_emails(self, 
                    count: int = 10, 
                    save_attachments: bool = False,
                    output_dir: str = "./email_attachments"
                    ) -> List[Dict[str, Any]]:
        """
        Fetch recent emails from the selected mailbox.
        
        Args:
            count: Number of recent emails to retrieve (default: 10)
            save_attachments: Whether to save attachments to disk (default: False)
            output_dir: Directory to save attachments (default: ./email_attachments)
            
        Returns:
            List[Dict]: List of dictionaries containing email data
        """
        if not self.imap:
            if not self.connect():
                return []
        
        # Create attachments directory if needed
        if save_attachments and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Search for all emails
        status, messages = self.imap.search(None, 'ALL')
        
        # List of email IDs
        email_ids = messages[0].split()
        
        # Create a list to store email data
        emails_data = []
        
        # Loop through the specified number of recent emails
        for email_id in email_ids[-count:]:
            res, msg = self.imap.fetch(email_id, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    from_ = msg.get("From")
                    date = msg.get("Date")
                    
                    # Extract email body and attachments
                    body = ""
                    attachments = []
                    
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            
                            # Get the body
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                try:
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    body = "Unable to decode body"
                                    
                            # Get attachments
                            if "attachment" in content_disposition:
                                try:
                                    filename = part.get_filename()
                                    if filename:
                                        # Decode filename if needed
                                        if decode_header(filename)[0][1] is not None:
                                            filename = decode_header(filename)[0][0]
                                            if isinstance(filename, bytes):
                                                filename = filename.decode()
                                        
                                        # Clean up filename to make it safe for filesystem
                                        safe_filename = "".join(c for c in filename if c.isalnum() or c in '._- ')
                                        
                                        attachment_data = {
                                            "filename": filename,
                                            "content_type": content_type,
                                            "size": len(part.get_payload(decode=True)),
                                            "saved_path": None
                                        }
                                        
                                        # Save attachment if requested
                                        if save_attachments:
                                            # Create a safe and unique filename using email_id as prefix
                                            email_id_str = email_id.decode()
                                            file_path = os.path.join(output_dir, f"{email_id_str}_{safe_filename}")
                                            
                                            # Write attachment to disk
                                            with open(file_path, "wb") as f:
                                                f.write(part.get_payload(decode=True))
                                            
                                            # Update attachment data with saved path
                                            attachment_data["saved_path"] = file_path
                                        
                                        attachments.append(attachment_data)
                                except Exception as e:
                                    attachments.append({
                                        "error": f"Failed to process attachment: {str(e)}"
                                    })
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode()
                        except:
                            body = "Unable to decode body"
                    
                    # Create email data dictionary
                    email_data = {
                        "id": email_id.decode(),
                        "from": from_,
                        "subject": subject,
                        "date": date,
                        "body": body,
                        "attachments": attachments
                    }
                    
                    # Add to emails list
                    emails_data.append(email_data)
        
        return emails_data
    
    def logout(self) -> None:
        """
        Logout from the IMAP server.
        """
        if self.imap:
            self.imap.logout()
            self.imap = None


# Command-line interface
if __name__ == "__main__":
    import argparse
    from .credentials import get_imap_config
    
    # Get the IMAP config
    imap_config = get_imap_config()
    
    # Define command-line arguments
    parser = argparse.ArgumentParser(description='Fetch emails and output them as JSON')
    parser.add_argument('--host', dest='host', default=imap_config.get('host'),
                       help=f'IMAP server hostname (default: {imap_config.get("host")})')
    parser.add_argument('--port', dest='port', type=int, default=imap_config.get('port'),
                       help=f'IMAP server port (default: {imap_config.get("port")})')
    parser.add_argument('--username', dest='username', default=imap_config.get('username'),
                       help='Email account username')
    parser.add_argument('--password', dest='password', default=imap_config.get('password'),
                       help='Email account password')
    parser.add_argument('--save-attachments', dest='save_attachments', action='store_true',
                       help='Save email attachments to disk')
    parser.add_argument('--output-dir', dest='output_dir', default='./email_attachments',
                       help='Directory to save attachments (default: ./email_attachments)')
    parser.add_argument('--count', dest='email_count', type=int, default=2,
                       help='Number of recent emails to retrieve (default: 2)')
    
    args = parser.parse_args()
    
    # Create receiver instance
    receiver = Receiver(args.host, args.port, args.username, args.password)
    
    # Connect and select inbox
    if receiver.connect() and receiver.select_mailbox():
        # Fetch emails
        emails_data = receiver.fetch_emails(
            count=args.email_count,
            save_attachments=args.save_attachments,
            output_dir=args.output_dir
        )
        
        # Output emails as JSON
        print(json.dumps(emails_data, indent=4))
    
    # Logout
    receiver.logout()
