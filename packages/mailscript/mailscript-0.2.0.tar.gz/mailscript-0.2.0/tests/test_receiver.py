"""
Tests for the Receiver class.
"""

import pytest
import os
import json
from unittest.mock import MagicMock, patch, mock_open
from mailscript import Receiver


@pytest.fixture
def mock_imap():
    """Create a mock IMAP4_SSL object for testing."""
    mock = MagicMock()
    mock.login = MagicMock(return_value=(True, "Success"))
    mock.select = MagicMock(return_value=("OK", None))
    mock.search = MagicMock(return_value=("OK", [b"1 2 3 4 5"]))
    
    # Mock fetch return value for an email
    mock_email_data = (
        "OK",
        [(b"1", (b"HEADER", b"Subject: Test Email\r\nFrom: test@example.com\r\nDate: Mon, 11 Jun 2025 10:00:00 +0000\r\n\r\nTest body"))]
    )
    mock.fetch = MagicMock(return_value=mock_email_data)
    
    mock.logout = MagicMock()
    return mock


@pytest.fixture
def receiver():
    """Create a Receiver instance for testing."""
    return Receiver(
        imap_host="imap.example.com",
        imap_port=993,
        username="test@example.com",
        password="password123"
    )


@patch("imaplib.IMAP4_SSL")
def test_receiver_connect(mock_imap_class, receiver):
    """Test connecting to an IMAP server."""
    mock_imap_instance = MagicMock()
    mock_imap_class.return_value = mock_imap_instance
    
    result = receiver.connect()
    
    assert result is True
    mock_imap_class.assert_called_once_with("imap.example.com", 993)
    mock_imap_instance.login.assert_called_once_with("test@example.com", "password123")


@patch("imaplib.IMAP4_SSL")
def test_receiver_select_mailbox(mock_imap_class, receiver):
    """Test selecting a mailbox."""
    mock_imap_instance = MagicMock()
    mock_imap_class.return_value = mock_imap_instance
    mock_imap_instance.select.return_value = ("OK", None)
    
    # Connect first
    receiver.connect()
    
    result = receiver.select_mailbox("INBOX")
    
    assert result is True
    mock_imap_instance.select.assert_called_once_with("INBOX")


@patch("imaplib.IMAP4_SSL")
@patch("os.path.exists")
@patch("os.makedirs")
def test_fetch_emails(mock_makedirs, mock_exists, mock_imap_class, receiver):
    """Test fetching emails."""
    # Mock IMAP
    mock_imap_instance = MagicMock()
    mock_imap_class.return_value = mock_imap_instance
    
    # Setup mock responses
    mock_imap_instance.search.return_value = ("OK", [b"1 2 3"])
      # Create proper email bytes that match what imaplib would return
    email_content = b"""From: sender@example.com
Subject: Test Subject
Date: Mon, 11 Jun 2025 10:00:00 +0000

This is the email body."""
    
    # Mock fetch response with a simple email - structure should match what imap.fetch returns
    mock_fetch_response = [
        (b"1", email_content)
    ]
    mock_imap_instance.fetch.return_value = ("OK", mock_fetch_response)
    
    # Mock directory check
    mock_exists.return_value = False
    
    # Connect
    receiver.connect()
    
    # Fetch emails
    emails = receiver.fetch_emails(count=1, save_attachments=True)
    
    # Assertions
    assert len(emails) == 1
    assert emails[0]["from"] == "sender@example.com"
    assert emails[0]["subject"] == "Test Subject"
    mock_makedirs.assert_called_once()


@patch("imaplib.IMAP4_SSL")
def test_logout(mock_imap_class, receiver):
    """Test logging out from the IMAP server."""
    mock_imap_instance = MagicMock()
    mock_imap_class.return_value = mock_imap_instance
    
    # Connect first
    receiver.connect()
    
    # Logout
    receiver.logout()
    
    # Verify logout was called
    mock_imap_instance.logout.assert_called_once()
    assert receiver.imap is None
