"""
Example demonstrating the template functionality of the mailscript package.
"""

import os
from mailscript import Mailer
from datetime import datetime

# Create templates directory for this example
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(TEMPLATE_DIR, exist_ok=True)

# Create a template file
TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, "newsletter.html")
with open(TEMPLATE_PATH, "w", encoding="utf-8") as f:
    f.write("""
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #4285f4; color: white; padding: 10px; text-align: center; }
        .content { padding: 20px; }
        .footer { text-align: center; padding: 10px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ company_name }} Newsletter</h1>
        </div>
        <div class="content">
            <h2>Hello, {{ recipient_name }}!</h2>
            <p>Welcome to our {{ edition_month }} newsletter.</p>
            
            <h3>Latest Updates</h3>
            <ul>
                {% for update in updates %}
                <li>{{ update }}</li>
                {% endfor %}
            </ul>
            
            <p>Thank you for subscribing to our newsletter!</p>
        </div>
        <div class="footer">
            <p>© {{ current_year }} {{ company_name }}. All rights reserved.</p>
            <p>You received this email because you subscribed to our newsletter.</p>
        </div>
    </div>
</body>
</html>
    """)

def main():
    """Run the template example."""
    # Create a mailer instance
    mailer = Mailer(
        smtp_host="smtp.example.com",
        smtp_port=587,
        smtp_user="your-email@example.com",
        smtp_password="your-password",
        use_tls=True,
    )
    
    # Example 1: Using template string
    template_string = """
    <html>
    <body>
        <h1>Welcome, {{ name }}!</h1>
        <p>Thank you for joining our platform.</p>
        <p>Your account was created on: {{ join_date }}.</p>
        <p>Start exploring our features:</p>
        <ul>
            {% for feature in features %}
            <li>{{ feature }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """
    
    # Prepare context data
    context = {
        "name": "John Doe",
        "join_date": datetime.now().strftime("%Y-%m-%d"),
        "features": [
            "Email Templates",
            "SMTP Configuration",
            "Attachment Support",
            "HTML Formatting"
        ]
    }
    
    print("Sending welcome email using template string...")
    
    try:
        success = mailer.send_template(
            sender="no-reply@example.com",
            recipients="john.doe@example.com",
            subject="Welcome to Our Platform!",
            template_string=template_string,
            context=context,
            is_html=True,
            validate_deliverability=False,  # Disable for this example
        )
        
        if success:
            print("Template email sent successfully!")
            
    except Exception as e:
        print(f"Error sending template email: {e}")
    
    # Example 2: Using template file
    print("\nSending newsletter using template file...")
    
    newsletter_context = {
        "company_name": "MailScript Inc.",
        "recipient_name": "Jane Smith",
        "edition_month": "June",
        "current_year": datetime.now().year,
        "updates": [
            "New template rendering engine released",
            "Improved attachment handling",
            "Enhanced email validation"
        ]
    }
    
    try:
        success = mailer.send_template_file(
            sender="newsletter@example.com",
            recipients="jane.smith@example.com",
            subject="June Newsletter",
            template_name="newsletter.html",
            template_folder=TEMPLATE_DIR,
            context=newsletter_context,
            is_html=True,
            validate_deliverability=False,  # Disable for this example
        )
        
        if success:
            print("Newsletter email sent successfully!")
            
    except Exception as e:
        print(f"Error sending newsletter email: {e}")

if __name__ == "__main__":
    main()
