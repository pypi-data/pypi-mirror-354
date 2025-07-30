"""
Command-line interface for the MailScript package.
This module allows MailScript to be run as a module with 'python -m mailscript'.
"""

import argparse
import sys
import os
import json
from getpass import getpass

from mailscript import Mailer, Receiver
from mailscript.templates import TemplateRenderer

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="MailScript - Email Utility")
    
    # Command subparsers
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Send command
    send_parser = subparsers.add_parser("send", help="Send an email")
    send_parser.add_argument("--host", required=True, help="SMTP server hostname")
    send_parser.add_argument("--port", type=int, default=587, help="SMTP server port (default: 587)")
    send_parser.add_argument("--user", required=True, help="SMTP username")
    send_parser.add_argument("--password", help="SMTP password (will prompt if not provided)")
    send_parser.add_argument("--no-tls", action="store_true", help="Disable TLS encryption")
    send_parser.add_argument("--from", dest="sender", required=True, help="Sender email address")
    send_parser.add_argument("--to", required=True, nargs="+", help="Recipient email address(es)")
    send_parser.add_argument("--cc", nargs="+", help="CC recipient email address(es)")
    send_parser.add_argument("--bcc", nargs="+", help="BCC recipient email address(es)")
    send_parser.add_argument("--subject", required=True, help="Email subject")
    send_parser.add_argument("--body", help="Email body text")
    send_parser.add_argument("--body-file", help="File containing the email body")
    send_parser.add_argument("--html", action="store_true", help="Treat body as HTML")
    send_parser.add_argument("--attach", nargs="+", help="File(s) to attach")
    
    # Template command
    template_parser = subparsers.add_parser("template", help="Send a templated email")
    template_parser.add_argument("--host", required=True, help="SMTP server hostname")
    template_parser.add_argument("--port", type=int, default=587, help="SMTP server port (default: 587)")
    template_parser.add_argument("--user", required=True, help="SMTP username")
    template_parser.add_argument("--password", help="SMTP password (will prompt if not provided)")
    template_parser.add_argument("--no-tls", action="store_true", help="Disable TLS encryption")
    template_parser.add_argument("--from", dest="sender", required=True, help="Sender email address")
    template_parser.add_argument("--to", required=True, nargs="+", help="Recipient email address(es)")
    template_parser.add_argument("--cc", nargs="+", help="CC recipient email address(es)")
    template_parser.add_argument("--bcc", nargs="+", help="BCC recipient email address(es)")
    template_parser.add_argument("--subject", required=True, help="Email subject")
    template_parser.add_argument("--template", required=True, help="Template file path")
    template_parser.add_argument("--context", nargs="+", help="Context variables in key=value format")
    template_parser.add_argument("--attach", nargs="+", help="File(s) to attach")
    
    # Version command
    version_parser = subparsers.add_parser("version", help="Show version information")
    
    # Receive command
    receive_parser = subparsers.add_parser("receive", help="Receive emails")
    receive_parser.add_argument("--host", required=True, help="IMAP server hostname")
    receive_parser.add_argument("--port", type=int, default=993, help="IMAP server port (default: 993)")
    receive_parser.add_argument("--user", required=True, help="IMAP username")
    receive_parser.add_argument("--password", help="IMAP password (will prompt if not provided)")
    receive_parser.add_argument("--count", type=int, default=10, help="Number of emails to retrieve (default: 10)")
    receive_parser.add_argument("--mailbox", default="INBOX", help="Mailbox to access (default: INBOX)")
    receive_parser.add_argument("--save-attachments", action="store_true", help="Save email attachments to disk")
    receive_parser.add_argument("--output-dir", default="./email_attachments", 
                               help="Directory to save attachments (default: ./email_attachments)")
    receive_parser.add_argument("--output-file", help="Save email data to a JSON file")
    
    return parser.parse_args()

def send_email(args):
    """Send an email based on command line arguments."""
    # Get password if not provided
    password = args.password if args.password else getpass(f"SMTP Password for {args.user}: ")
    
    # Create mailer
    mailer = Mailer(
        smtp_host=args.host,
        smtp_port=args.port,
        smtp_user=args.user,
        smtp_password=password,
        use_tls=not args.no_tls
    )
    
    # Get email body
    body = None
    if args.body:
        body = args.body
    elif args.body_file:
        try:
            with open(args.body_file, "r", encoding="utf-8") as f:
                body = f.read()
        except Exception as e:
            print(f"Error reading body file: {e}", file=sys.stderr)
            return 1
    else:
        print("Error: Either --body or --body-file must be provided", file=sys.stderr)
        return 1
    
    # Prepare attachments
    attachments = {}
    if args.attach:
        for path in args.attach:
            try:
                filename = os.path.basename(path)
                attachments[filename] = open(path, "rb")
            except Exception as e:
                print(f"Error opening attachment {path}: {e}", file=sys.stderr)
                # Close any opened attachments
                for f in attachments.values():
                    f.close()
                return 1
    
    try:
        # Send the email
        mailer.send(
            sender=args.sender,
            recipients=args.to,
            subject=args.subject,
            body=body,
            is_html=args.html,
            cc=args.cc,
            bcc=args.bcc,
            attachments=attachments
        )
        print("Email sent successfully!")
        return 0
        
    except Exception as e:
        print(f"Error sending email: {e}", file=sys.stderr)
        return 1
        
    finally:
        # Close any opened attachments
        for f in attachments.values():
            f.close()

def send_template(args):
    """Send a templated email based on command line arguments."""
    # Get password if not provided
    password = args.password if args.password else getpass(f"SMTP Password for {args.user}: ")
    
    # Create mailer
    mailer = Mailer(
        smtp_host=args.host,
        smtp_port=args.port,
        smtp_user=args.user,
        smtp_password=password,
        use_tls=not args.no_tls
    )
    
    # Parse template context
    context = {}
    if args.context:
        for item in args.context:
            if "=" in item:
                key, value = item.split("=", 1)
                context[key] = value
            else:
                print(f"Warning: Ignoring invalid context variable format: {item}", file=sys.stderr)
    
    # Prepare attachments
    attachments = {}
    if args.attach:
        for path in args.attach:
            try:
                filename = os.path.basename(path)
                attachments[filename] = open(path, "rb")
            except Exception as e:
                print(f"Error opening attachment {path}: {e}", file=sys.stderr)
                # Close any opened attachments
                for f in attachments.values():
                    f.close()
                return 1
    
    try:
        # Get the template folder and filename
        template_path = os.path.abspath(args.template)
        template_folder = os.path.dirname(template_path)
        template_name = os.path.basename(template_path)
        
        # Send the templated email
        mailer.send_template_file(
            sender=args.sender,
            recipients=args.to,
            subject=args.subject,
            template_name=template_name,
            template_folder=template_folder,
            context=context,
            is_html=True,  # Template emails are typically HTML
            cc=args.cc,
            bcc=args.bcc,
            attachments=attachments
        )
        print("Templated email sent successfully!")
        return 0
        
    except Exception as e:
        print(f"Error sending templated email: {e}", file=sys.stderr)
        return 1
        
    finally:
        # Close any opened attachments
        for f in attachments.values():
            f.close()

def receive_email(args):
    """Receive emails based on command line arguments."""
    # Get password if not provided
    password = args.password if args.password else getpass(f"IMAP Password for {args.user}: ")
    
    # Create receiver
    receiver = Receiver(
        imap_host=args.host,
        imap_port=args.port,
        username=args.user,
        password=password
    )
    
    try:
        # Connect to the server
        if not receiver.connect():
            print("Failed to connect to the IMAP server", file=sys.stderr)
            return 1
            
        # Select the mailbox
        if not receiver.select_mailbox(args.mailbox):
            print(f"Failed to select mailbox: {args.mailbox}", file=sys.stderr)
            return 1
        
        # Fetch emails
        emails_data = receiver.fetch_emails(
            count=args.count,
            save_attachments=args.save_attachments,
            output_dir=args.output_dir
        )
        
        if emails_data:
            print(f"Retrieved {len(emails_data)} emails from {args.mailbox}")
            
            # Save to output file if specified
            if args.output_file:
                try:
                    with open(args.output_file, 'w', encoding='utf-8') as f:
                        json.dump(emails_data, f, indent=4)
                    print(f"Email data saved to {args.output_file}")
                except Exception as e:
                    print(f"Error saving output file: {e}", file=sys.stderr)
            else:
                # Print to stdout
                print(json.dumps(emails_data, indent=4))
                
            return 0
        else:
            print(f"No emails found in {args.mailbox}")
            return 0
            
    except Exception as e:
        print(f"Error receiving emails: {e}", file=sys.stderr)
        return 1
    finally:
        # Always logout
        receiver.logout()

def show_version():
    """Show the package version."""
    from mailscript import __version__
    print(f"MailScript version {__version__}")
    return 0

def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    if args.command == "send":
        return send_email(args)
    elif args.command == "template":
        return send_template(args)
    elif args.command == "receive":
        return receive_email(args)
    elif args.command == "version":
        return show_version()
    else:
        print("Error: Please specify a command (send, template, receive, version)", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
