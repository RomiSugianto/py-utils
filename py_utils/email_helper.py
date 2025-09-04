import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import ssl

class EmailHelper:
    """A helper class for sending emails via SMTP."""

    @staticmethod
    def setup_smtp(
        smtp_server: str,
        port: int = 25,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: bool = False
    ) -> smtplib.SMTP:
        """
        Set up an SMTP connection.

        Args:
            smtp_server: SMTP server address
            port: SMTP port (default: 25)
            username: SMTP username for authentication
            password: SMTP password for authentication
            use_tls: Whether to use TLS encryption

        Returns:
            Configured SMTP connection
        """
        try:
            if use_tls:
                server = smtplib.SMTP_SSL(smtp_server, port, context=ssl.create_default_context())
            else:
                server = smtplib.SMTP(smtp_server, port)
                if username and password:
                    server.login(username, password)
            return server
        except Exception as e:
            raise Exception(f"Failed to setup SMTP connection: {str(e)}")

    @staticmethod
    def send_email(
        server: smtplib.SMTP,
        from_addr: str,
        to_addr: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """
        Send an email using the provided SMTP server.

        Args:
            server: Configured SMTP server instance
            from_addr: Sender email address
            to_addr: Recipient email address
            subject: Email subject
            body: Plain text email body
            html_body: Optional HTML email body

        Returns:
            True if email sent successfully
        """
        try:
            msg = MIMEMultipart("alternative")
            msg['Subject'] = subject
            msg['From'] = from_addr
            msg['To'] = to_addr

            # Attach plain text body
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)

            # Attach HTML body if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)

            server.sendmail(from_addr, to_addr, msg.as_string())
            return True
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")

# Convenience function for quick email sending
def send_quick_email(
    smtp_server: str,
    from_addr: str,
    to_addr: str,
    subject: str,
    body: str,
    port: int = 25,
    username: Optional[str] = None,
    password: Optional[str] = None,
    use_tls: bool = False,
    html_body: Optional[str] = None
) -> bool:
    """
    Quick function to send an email with minimal setup.

    Args:
        smtp_server: SMTP server address
        from_addr: Sender email address
        to_addr: Recipient email address
        subject: Email subject
        body: Plain text email body
        port: SMTP port (default: 25)
        username: SMTP username
        password: SMTP password
        use_tls: Whether to use TLS
        html_body: Optional HTML email body

    Returns:
        True if email sent successfully
    """
    server = None
    try:
        server = EmailHelper.setup_smtp(smtp_server, port, username, password, use_tls)
        result = EmailHelper.send_email(server, from_addr, to_addr, subject, body, html_body)
        return result
    finally:
        if server:
            server.quit()
