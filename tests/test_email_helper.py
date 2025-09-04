import pytest
from unittest.mock import Mock, patch
from py_utils.email_helper import EmailHelper, send_quick_email


class TestEmailHelper:
    """Test cases for EmailHelper class."""

    def test_setup_smtp_basic(self):
        """Test basic SMTP setup without authentication."""
        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = Mock()
            mock_smtp.return_value = mock_server

            result = EmailHelper.setup_smtp("smtp.example.com", 25)

            assert result == mock_server
            mock_smtp.assert_called_once_with("smtp.example.com", 25)

    def test_setup_smtp_with_tls(self):
        """Test SMTP setup with TLS encryption."""
        with patch('smtplib.SMTP_SSL') as mock_smtp_ssl:
            mock_server = Mock()
            mock_smtp_ssl.return_value = mock_server

            result = EmailHelper.setup_smtp("smtp.example.com", 465, use_tls=True)

            assert result == mock_server
            # Verify SMTP_SSL was called with correct parameters
            mock_smtp_ssl.assert_called_once()
            call_args = mock_smtp_ssl.call_args
            assert call_args[0][0] == "smtp.example.com"
            assert call_args[0][1] == 465
            # SSL context should be passed
            assert 'context' in call_args[1]

    def test_setup_smtp_with_auth(self):
        """Test SMTP setup with authentication."""
        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = Mock()
            mock_smtp.return_value = mock_server

            result = EmailHelper.setup_smtp(
                "smtp.example.com", 25,
                username="test@example.com",
                password="password123"
            )

            assert result == mock_server
            mock_server.login.assert_called_once_with("test@example.com", "password123")

    def test_setup_smtp_failure(self):
        """Test SMTP setup failure handling."""
        with patch('smtplib.SMTP') as mock_smtp:
            mock_smtp.side_effect = Exception("Connection failed")

            with pytest.raises(Exception, match="Failed to setup SMTP connection"):
                EmailHelper.setup_smtp("smtp.example.com", 25)

    def test_send_email_basic(self):
        """Test basic email sending functionality."""
        mock_server = Mock()

        result = EmailHelper.send_email(
            server=mock_server,
            from_addr="sender@example.com",
            to_addr="recipient@example.com",
            subject="Test Subject",
            body="Test Body"
        )

        assert result is True
        mock_server.sendmail.assert_called_once()
        args = mock_server.sendmail.call_args[0]
        assert args[0] == "sender@example.com"
        assert args[1] == "recipient@example.com"

    def test_send_email_with_html(self):
        """Test sending email with HTML body."""
        mock_server = Mock()

        result = EmailHelper.send_email(
            server=mock_server,
            from_addr="sender@example.com",
            to_addr="recipient@example.com",
            subject="Test Subject",
            body="Plain text body",
            html_body="<h1>HTML Body</h1>"
        )

        assert result is True
        mock_server.sendmail.assert_called_once()

    def test_send_email_failure(self):
        """Test email sending failure handling."""
        mock_server = Mock()
        mock_server.sendmail.side_effect = Exception("Send failed")

        with pytest.raises(Exception, match="Failed to send email"):
            EmailHelper.send_email(
                server=mock_server,
                from_addr="sender@example.com",
                to_addr="recipient@example.com",
                subject="Test Subject",
                body="Test Body"
            )


class TestSendQuickEmail:
    """Test cases for the send_quick_email convenience function."""

    @patch('py_utils.email_helper.EmailHelper.setup_smtp')
    @patch('py_utils.email_helper.EmailHelper.send_email')
    def test_send_quick_email_basic(self, mock_send, mock_setup):
        """Test basic quick email sending."""
        mock_server = Mock()
        mock_setup.return_value = mock_server
        mock_send.return_value = True

        result = send_quick_email(
            smtp_server="smtp.example.com",
            from_addr="sender@example.com",
            to_addr="recipient@example.com",
            subject="Test Subject",
            body="Test Body"
        )

        assert result is True
        mock_setup.assert_called_once_with("smtp.example.com", 25, None, None, False)
        mock_send.assert_called_once()
        mock_server.quit.assert_called_once()

    @patch('py_utils.email_helper.EmailHelper.setup_smtp')
    @patch('py_utils.email_helper.EmailHelper.send_email')
    def test_send_quick_email_with_auth(self, mock_send, mock_setup):
        """Test quick email with authentication."""
        mock_server = Mock()
        mock_setup.return_value = mock_server
        mock_send.return_value = True

        result = send_quick_email(
            smtp_server="smtp.example.com",
            from_addr="sender@example.com",
            to_addr="recipient@example.com",
            subject="Test Subject",
            body="Test Body",
            username="user@example.com",
            password="password123",
            use_tls=True
        )

        assert result is True
        mock_setup.assert_called_once_with("smtp.example.com", 25, "user@example.com", "password123", True)

    @patch('py_utils.email_helper.EmailHelper.setup_smtp')
    @patch('py_utils.email_helper.EmailHelper.send_email')
    def test_send_quick_email_server_cleanup(self, mock_send, mock_setup):
        """Test that server is properly closed even on failure."""
        mock_server = Mock()
        mock_setup.return_value = mock_server
        mock_send.side_effect = Exception("Send failed")

        with pytest.raises(Exception):
            send_quick_email(
                smtp_server="smtp.example.com",
                from_addr="sender@example.com",
                to_addr="recipient@example.com",
                subject="Test Subject",
                body="Test Body"
            )

        # Server should still be closed
        mock_server.quit.assert_called_once()
