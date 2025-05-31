#!/usr/bin/env python3
"""
Direct test of Mailgun SMTP credentials
Run this script to test your Mailgun SMTP connection outside of Django
"""

import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your Mailgun SMTP settings - update these with your actual values
SMTP_SERVER = "smtp.mailgun.org"
SMTP_PORT = 587
SMTP_USERNAME = "b11-1_admin@sandbox55233cc73cfc46cfb6cf94605a6e5c36.mailgun.org"
SMTP_PASSWORD = "5bb48b80eb56400f1d95ed224cb2a36b-f3238714-05495171"
TO_EMAIL = "yann.crausaz@gmail.com"

def test_smtp_connection():
    """Test SMTP connection and authentication"""
    print("🔧 Testing Mailgun SMTP Connection...")
    print(f"Server: {SMTP_SERVER}:{SMTP_PORT}")
    print(f"Username: {SMTP_USERNAME}")
    print(f"Password: {'*' * len(SMTP_PASSWORD)}")
    print("-" * 50)
    
    try:
        print("1️⃣ Connecting to SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        print("2️⃣ Starting TLS encryption...")
        server.starttls()
        
        print("3️⃣ Attempting login...")
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        print("✅ SMTP authentication successful!")
        
        print("4️⃣ Sending test email...")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = TO_EMAIL
        msg['Subject'] = "Direct SMTP Test from Python"
        
        body = """
        This is a direct SMTP test email sent from Python.
        
        If you receive this email, your Mailgun SMTP credentials are working correctly!
        
        Test performed at: {timestamp}
        """.format(timestamp=__import__('datetime').datetime.now())
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        text = msg.as_string()
        server.sendmail(SMTP_USERNAME, TO_EMAIL, text)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print(f"📧 Check {TO_EMAIL} for the test email")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication failed: {e}")
        print("🔍 This usually means:")
        print("   - Wrong username or password")
        print("   - SMTP credentials have expired")
        print("   - Account has been suspended")
        return False
        
    except smtplib.SMTPServerDisconnected as e:
        print(f"❌ SMTP Server disconnected: {e}")
        print("🔍 This usually means:")
        print("   - Network connectivity issues")
        print("   - Firewall blocking SMTP ports")
        print("   - Incorrect server settings")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

def test_network_connectivity():
    """Test basic network connectivity to Mailgun"""
    import socket
    
    print("\n🌐 Testing network connectivity...")
    try:
        # Test DNS resolution
        print("1️⃣ Testing DNS resolution...")
        ip = socket.gethostbyname(SMTP_SERVER)
        print(f"✅ {SMTP_SERVER} resolves to {ip}")
        
        # Test port connectivity
        print("2️⃣ Testing port connectivity...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((SMTP_SERVER, SMTP_PORT))
        sock.close()
        
        if result == 0:
            print(f"✅ Port {SMTP_PORT} is reachable")
            return True
        else:
            print(f"❌ Cannot connect to port {SMTP_PORT}")
            return False
            
    except Exception as e:
        print(f"❌ Network test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Mailgun SMTP Test Script")
    print("=" * 50)
    
    # Test network first
    network_ok = test_network_connectivity()
    if not network_ok:
        print("\n❌ Network connectivity failed. Please check your internet connection.")
        sys.exit(1)
    
    # Test SMTP
    smtp_ok = test_smtp_connection()
    
    print("\n" + "=" * 50)
    if smtp_ok:
        print("🎉 All tests passed! Your Mailgun SMTP is working correctly.")
        print("✨ You can now use these credentials in your Django app.")
    else:
        print("🔧 SMTP test failed. Please:")
        print("   1. Verify your Mailgun SMTP credentials")
        print("   2. Check if your Mailgun account is active")
        print("   3. Try creating new SMTP credentials in Mailgun")
        print("   4. Ensure your recipient email is authorized (for sandbox domains)")
    
    print("\n📚 Next steps:")
    print("   - Update your .env file with working credentials")
    print("   - Restart your Django development server")
    print("   - Run: python manage.py test_email --recipient=your@email.com")
