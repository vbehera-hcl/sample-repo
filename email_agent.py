"""
AI Email Agent for Gmail
This agent can compose and send emails through Gmail's SMTP server.

Prerequisites:
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password: Google Account > Security > 2-Step Verification > App passwords
3. Use the 16-character App Password (not your regular password)
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EmailConfig:
    """Configuration for Gmail SMTP connection."""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str = ""
    app_password: str = ""


@dataclass
class Email:
    """Email message structure."""
    to: List[str]
    subject: str
    body: str
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
    attachments: Optional[List[str]] = None
    is_html: bool = False


class EmailAgent:
    """AI Agent for sending emails via Gmail."""
    
    def __init__(self, sender_email: str, app_password: str):
        """
        Initialize the Email Agent.
        
        Args:
            sender_email: Your Gmail address
            app_password: Gmail App Password (16 characters, no spaces)
        """
        self.config = EmailConfig(
            sender_email=sender_email,
            app_password=app_password
        )
        self.connection = None
    
    def connect(self) -> bool:
        """Establish connection to Gmail SMTP server."""
        try:
            self.connection = smtplib.SMTP(
                self.config.smtp_server, 
                self.config.smtp_port
            )
            self.connection.starttls()  # Enable TLS encryption
            self.connection.login(
                self.config.sender_email, 
                self.config.app_password
            )
            print("✓ Connected to Gmail SMTP server successfully!")
            return True
        except smtplib.SMTPAuthenticationError:
            print("✗ Authentication failed. Check your email and App Password.")
            return False
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close the SMTP connection."""
        if self.connection:
            self.connection.quit()
            self.connection = None
            print("✓ Disconnected from Gmail SMTP server.")
    
    def compose_email(self, email: Email) -> MIMEMultipart:
        """Compose an email message."""
        message = MIMEMultipart()
        message["From"] = self.config.sender_email
        message["To"] = ", ".join(email.to)
        message["Subject"] = email.subject
        message["Date"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
        
        if email.cc:
            message["Cc"] = ", ".join(email.cc)
        
        # Attach body
        content_type = "html" if email.is_html else "plain"
        message.attach(MIMEText(email.body, content_type))
        
        # Attach files if any
        if email.attachments:
            for file_path in email.attachments:
                self._attach_file(message, file_path)
        
        return message
    
    def _attach_file(self, message: MIMEMultipart, file_path: str):
        """Attach a file to the email."""
        try:
            with open(file_path, "rb") as file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.read())
                encoders.encode_base64(part)
                filename = os.path.basename(file_path)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}"
                )
                message.attach(part)
                print(f"  ✓ Attached: {filename}")
        except FileNotFoundError:
            print(f"  ✗ File not found: {file_path}")
        except Exception as e:
            print(f"  ✗ Failed to attach {file_path}: {e}")
    
    def send_email(self, email: Email) -> bool:
        """
        Send an email.
        
        Args:
            email: Email object containing message details
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            message = self.compose_email(email)
            
            # Collect all recipients
            all_recipients = list(email.to)
            if email.cc:
                all_recipients.extend(email.cc)
            if email.bcc:
                all_recipients.extend(email.bcc)
            
            self.connection.sendmail(
                self.config.sender_email,
                all_recipients,
                message.as_string()
            )
            
            print(f"✓ Email sent successfully to: {', '.join(email.to)}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to send email: {e}")
            return False
    
    def send_quick_email(
        self, 
        to: str, 
        subject: str, 
        body: str,
        is_html: bool = False
    ) -> bool:
        """
        Quick method to send a simple email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
            is_html: Whether body contains HTML
            
        Returns:
            True if successful, False otherwise
        """
        email = Email(
            to=[to],
            subject=subject,
            body=body,
            is_html=is_html
        )
        return self.send_email(email)


class InteractiveEmailAgent:
    """Interactive command-line interface for the Email Agent."""
    
    def __init__(self):
        self.agent = None
    
    def setup(self):
        """Set up the email agent with user credentials."""
        print("\n" + "="*50)
        print("       Gmail Email Agent Setup")
        print("="*50)
        print("\nNote: You need a Gmail App Password to use this agent.")
        print("Get one at: Google Account > Security > App passwords\n")
        
        email = input("Enter your Gmail address: ").strip()
        password = input("Enter your App Password (16 chars): ").strip()
        
        self.agent = EmailAgent(email, password)
        return self.agent.connect()
    
    def compose_interactive(self) -> Optional[Email]:
        """Interactively compose an email."""
        print("\n--- Compose New Email ---\n")
        
        to = input("To (comma-separated for multiple): ").strip()
        if not to:
            print("✗ Recipient is required.")
            return None
        
        subject = input("Subject: ").strip()
        
        print("Body (enter 'END' on a new line to finish):")
        body_lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            body_lines.append(line)
        body = "\n".join(body_lines)
        
        cc = input("CC (optional, comma-separated): ").strip()
        attachments = input("Attachments (optional, comma-separated paths): ").strip()
        
        return Email(
            to=[e.strip() for e in to.split(",")],
            subject=subject,
            body=body,
            cc=[e.strip() for e in cc.split(",")] if cc else None,
            attachments=[a.strip() for a in attachments.split(",")] if attachments else None
        )
    
    def run(self):
        """Run the interactive email agent."""
        if not self.setup():
            print("\nFailed to connect. Please check your credentials.")
            return
        
        print("\n" + "="*50)
        print("       Email Agent Ready!")
        print("="*50)
        
        while True:
            print("\nOptions:")
            print("  1. Send a new email")
            print("  2. Send a quick email")
            print("  3. Reconnect")
            print("  4. Exit")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                email = self.compose_interactive()
                if email:
                    self.agent.send_email(email)
            
            elif choice == "2":
                to = input("To: ").strip()
                subject = input("Subject: ").strip()
                body = input("Body: ").strip()
                if to:
                    self.agent.send_quick_email(to, subject, body)
            
            elif choice == "3":
                self.agent.disconnect()
                self.agent.connect()
            
            elif choice == "4":
                self.agent.disconnect()
                print("\nGoodbye!")
                break
            
            else:
                print("Invalid option. Please try again.")


def send_email_programmatically():
    """Example of using the Email Agent programmatically."""
    
    # Configuration - Replace with your credentials
    SENDER_EMAIL = "your-email@gmail.com"
    APP_PASSWORD = "your-app-password"  # 16-character App Password
    
    # Create agent
    agent = EmailAgent(SENDER_EMAIL, APP_PASSWORD)
    
    # Connect to Gmail
    if not agent.connect():
        return
    
    # Send a simple email
    agent.send_quick_email(
        to="recipient@example.com",
        subject="Hello from Email Agent",
        body="This is a test email sent by the AI Email Agent!"
    )
    
    # Send a more complex email
    email = Email(
        to=["recipient1@example.com", "recipient2@example.com"],
        subject="Meeting Reminder",
        body="""
        <h1>Meeting Reminder</h1>
        <p>Don't forget our meeting tomorrow at <strong>2:00 PM</strong>.</p>
        <p>Best regards,<br>Email Agent</p>
        """,
        cc=["cc@example.com"],
        is_html=True,
        attachments=["document.pdf"]  # Optional file attachment
    )
    agent.send_email(email)
    
    # Disconnect
    agent.disconnect()


if __name__ == "__main__":
    print("\n" + "="*50)
    print("     AI EMAIL AGENT FOR GMAIL")
    print("="*50)
    print("\nChoose mode:")
    print("  1. Interactive mode (recommended)")
    print("  2. Show programmatic example")
    
    mode = input("\nSelect (1 or 2): ").strip()
    
    if mode == "1":
        interactive_agent = InteractiveEmailAgent()
        interactive_agent.run()
    else:
        print("\n--- Programmatic Usage Example ---\n")
        print("See the send_email_programmatically() function in the code.")
        print("Edit the SENDER_EMAIL and APP_PASSWORD variables to use it.")
