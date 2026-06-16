import os
import django
import smtplib

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def debug_email():
    print("\n--- Email Configuration Debugger ---")
    
    user = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    port = settings.EMAIL_PORT
    host = settings.EMAIL_HOST
    use_tls = settings.EMAIL_USE_TLS

    print(f"HOST: {host}")
    print(f"PORT: {port}")
    print(f"TLS: {use_tls}")
    print(f"USER: {user}")
    print(f"PASSWORD SET: {'[YES]' if password else '[NO]'}")

    if not password:
        print("\n[CRITICAL ERROR] Password is missing!")
        print("You have configured the system to use environment variables, but 'EMAIL_HOST_PASSWORD' is not set.")
        print("\nFix this by running the following command in your terminal before running the script:")
        print('PowerShell: $env:EMAIL_HOST_PASSWORD = "your-16-digit-app-password"')
        print('CMD: set EMAIL_HOST_PASSWORD=your-16-digit-app-password')
        return

    print(f"\nAttempting to send test email to {user}...")
    try:
        send_mail(
            'Debug Test Email',
            'If you are reading this, your email configuration is working perfectly!',
            user,
            [user],
            fail_silently=False,
        )
        print("[SUCCESS] Email sent without errors.")
        print("Please check your Inbox and SPAM folder.")
    except smtplib.SMTPAuthenticationError:
        print("[ERROR] Authentication Failed!")
        print("Possible causes:")
        print("1. The App Password is incorrect.")
        print("2. You are using your normal Gmail password instead of an App Password.")
        print("3. 'Less secure app access' might need to be enabled (though App Passwords avoid this).")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

if __name__ == "__main__":
    debug_email()
