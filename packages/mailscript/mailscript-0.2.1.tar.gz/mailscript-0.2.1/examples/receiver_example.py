"""
Example of using the MailScript Receiver to fetch emails.

This example demonstrates how to:
1. Connect to an IMAP server
2. Select a mailbox
3. Fetch recent emails
4. Extract and save attachments
5. Process email data
"""

from mailscript import Receiver
import json
import os
from getpass import getpass

# Email credentials
imap_host = "imap.example.com"
imap_port = 993
username = input("Enter your email address: ")
password = getpass("Enter your password: ")

# Create receiver instance
receiver = Receiver(
    imap_host=imap_host,
    imap_port=imap_port,
    username=username,
    password=password
)

print("Connecting to IMAP server...")
if receiver.connect():
    print("Connected successfully!")
    
    # Select mailbox
    if receiver.select_mailbox("INBOX"):
        print("INBOX selected")
        
        # Create directory for attachments
        attachments_dir = "./email_attachments"
        if not os.path.exists(attachments_dir):
            os.makedirs(attachments_dir)
        
        # Fetch emails
        print("Fetching emails...")
        count = int(input("How many recent emails do you want to fetch? "))
        save_attachments = input("Save attachments? (y/n): ").lower() == 'y'
        
        emails = receiver.fetch_emails(
            count=count,
            save_attachments=save_attachments,
            output_dir=attachments_dir
        )
        
        # Display emails
        print(f"\nFetched {len(emails)} emails:")
        for i, email in enumerate(emails):
            print(f"\n--- Email {i+1} ---")
            print(f"From: {email['from']}")
            print(f"Subject: {email.get('subject', 'No subject')}")
            print(f"Date: {email.get('date', 'No date')}")
            print(f"Body Preview: {email.get('body', 'No body')[:100]}...")
            
            if email['attachments']:
                print(f"Attachments: {len(email['attachments'])}")
                for attachment in email['attachments']:
                    print(f"  - {attachment['filename']} ({attachment['content_type']}, {attachment['size']} bytes)")
                    if save_attachments and attachment['saved_path']:
                        print(f"    Saved to: {attachment['saved_path']}")
        
        # Save to JSON if desired
        save_json = input("\nSave email data to JSON file? (y/n): ").lower() == 'y'
        if save_json:
            filename = input("Enter filename (default: emails.json): ") or "emails.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(emails, f, indent=2)
            print(f"Email data saved to {filename}")
    
    # Logout
    receiver.logout()
    print("Logged out successfully")
else:
    print("Failed to connect to the IMAP server. Please check your credentials and settings.")
