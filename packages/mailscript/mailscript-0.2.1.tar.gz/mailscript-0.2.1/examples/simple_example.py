"""
Example usage of the mailscript package.
"""

from mailscript import Mailer
from mailscript.templates import TemplateRenderer

def main():
    """Run the example."""
    # Initialize the mailer
    mailer = Mailer(
        smtp_host="smtp.example.com",
        smtp_port=587,
        smtp_user="your-email@example.com",
        smtp_password="your-password",
        use_tls=True,
    )
    
    # Initialize template renderer
    renderer = TemplateRenderer()
    
    # Set up template and context
    template = """
    <html>
    <body>
        <h1>Hello, {{ name }}!</h1>
        <p>This is a test email from the MailScript package.</p>
        <p>Current date: {{ date }}</p>
    </body>
    </html>
    """
    
    # Add a current date global
    import datetime
    renderer.add_global("date", datetime.datetime.now().strftime("%Y-%m-%d"))
    
    # Render the template
    context = {"name": "World"}
    html_content = renderer.render_from_string(template, context)
    
    # Send HTML email
    try:
        success = mailer.send(
            sender="your-email@example.com",
            recipients="recipient@example.com",
            subject="Test Email from MailScript",
            body=html_content,
            is_html=True,
            # Disable validation for this example
            validate_deliverability=False,
        )
        
        if success:
            print("Email sent successfully!")
        
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    main()
