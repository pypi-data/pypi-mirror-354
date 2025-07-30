"""
Test module for the mailscript.mailer module.
"""
import pytest
from unittest.mock import patch, MagicMock

from mailscript import Mailer

@pytest.fixture
def mailer():
    """Create a Mailer instance for testing."""
    return Mailer(
        smtp_host="smtp.example.com",
        smtp_port=587,
        smtp_user="user@example.com",
        smtp_password="password",
        use_tls=True,
    )

def test_validate_email(mailer):
    """Test email validation."""
    assert mailer.validate_email("user@example.com") is True
    assert mailer.validate_email("invalid-email") is False
    assert mailer.validate_email("user@invalid") is False
    assert mailer.validate_email("user@example.co.uk") is True

@patch("smtplib.SMTP")
def test_send_email_success(mock_smtp, mailer):
    """Test sending an email successfully."""
    # Setup the mock
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server
    
    # Call the method
    result = mailer.send(
        sender="from@example.com",
        recipients="to@example.com",
        subject="Test Subject",
        body="Test Body",
        validate_deliverability=False,
    )
    
    # Assert the result
    assert result is True
    
    # Assert the SMTP calls
    mock_smtp.assert_called_once_with("smtp.example.com", 587, timeout=60)
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with("user@example.com", "password")
    mock_server.sendmail.assert_called_once()

@patch("smtplib.SMTP")
def test_send_email_with_cc_bcc(mock_smtp, mailer):
    """Test sending an email with CC and BCC recipients."""
    # Setup the mock
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server
    
    # Call the method
    result = mailer.send(
        sender="from@example.com",
        recipients=["to1@example.com", "to2@example.com"],
        subject="Test Subject",
        body="Test Body",
        cc="cc@example.com",
        bcc=["bcc1@example.com", "bcc2@example.com"],
        validate_deliverability=False,
    )
    
    # Assert the result
    assert result is True
    
    # Check that all recipients are included in the sendmail call
    all_recipients = ["to1@example.com", "to2@example.com", "cc@example.com", "bcc1@example.com", "bcc2@example.com"]
    args, _ = mock_server.sendmail.call_args
    assert args[0] == "from@example.com"
    assert sorted(args[1]) == sorted(all_recipients)
