import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Notification configuration from environment
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

def send_booking_requested_notification(studio_owner_email, studio_owner_phone, studio_name, customer_name, booking_date, total_inr):
    """
    Alerts the studio owner that a customer has requested a booking.
    """
    subject = f"🔔 New Booking Request: {customer_name} for {studio_name}"
    message = (
        f"Hello! You have received a new booking request for {studio_name}.\n\n"
        f"• Customer: {customer_name}\n"
        f"• Date: {booking_date}\n"
        f"• Estimated Amount: ₹{int(total_inr):,}\n\n"
        f"Please log in to your Studioza Studio Dashboard to confirm or manage this reservation."
    )
    
    # 1. Send Email
    _dispatch_email(studio_owner_email, subject, message)
    
    # 2. Send SMS if phone provided
    if studio_owner_phone:
        sms_text = f"Studioza Alert: New booking request from {customer_name} for {studio_name} on {booking_date} (₹{int(total_inr):,}). Check dashboard to confirm."
        _dispatch_sms(studio_owner_phone, sms_text)
        
    return True

def send_booking_status_notification(customer_email, customer_phone, studio_name, status, booking_date, total_inr):
    """
    Alerts the customer when their booking status changes (confirmed, rejected, completed).
    """
    status_icon = "✅" if status == "confirmed" else "⚠️"
    subject = f"{status_icon} Your Studioza Booking has been {status.capitalize()}!"
    message = (
        f"Hello! Your booking with {studio_name} on {booking_date} has been updated to: {status.upper()}.\n\n"
        f"• Total Amount: ₹{int(total_inr):,}\n"
        f"• Status: {status.capitalize()}\n\n"
        f"Thank you for booking with Studioza!"
    )
    
    _dispatch_email(customer_email, subject, message)
    if customer_phone:
        _dispatch_sms(customer_phone, f"Studioza Update: Your booking at {studio_name} on {booking_date} is now {status.upper()}.")
        
    return True

def send_payment_receipt_notification(customer_email, studio_name, amount_inr, transaction_id, booking_id):
    """
    Sends payment confirmation receipt.
    """
    subject = f"🧾 Payment Received (₹{int(amount_inr):,}) - Studioza Booking #{booking_id}"
    message = (
        f"Payment Confirmation:\n\n"
        f"• Studio: {studio_name}\n"
        f"• Booking ID: #{booking_id}\n"
        f"• Amount Paid: ₹{int(amount_inr):,}\n"
        f"• Transaction Ref: {transaction_id}\n\n"
        f"Your booking deposit / payment has been confirmed. Have a great shoot!"
    )
    _dispatch_email(customer_email, subject, message)
    return True

def _dispatch_email(to_email, subject, body):
    if not to_email:
        return
        
    # Check if SendGrid API is configured
    if SENDGRID_API_KEY:
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            message = Mail(
                from_email='concierge@studioza.com',
                to_emails=to_email,
                subject=subject,
                plain_text_content=body
            )
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            sg.send(message)
            print(f"[Notifications:SendGrid] Email sent successfully to {to_email}")
            return
        except Exception as e:
            print(f"[Notifications:SendGrid] Error: {e}")

    # Check if standard SMTP is configured
    if SMTP_HOST and SMTP_USER and SMTP_PASSWORD:
        try:
            msg = MIMEMultipart()
            msg['From'] = SMTP_USER
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            print(f"[Notifications:SMTP] Email dispatched to {to_email}")
            return
        except Exception as e:
            print(f"[Notifications:SMTP] Error: {e}")

    # Development audit log fallback
    print(f"\n📨 [EMAIL AUDIT LOG] To: {to_email} | Subject: {subject}\n{body}\n----------------------------------------\n")

def _dispatch_sms(to_phone, text):
    if not to_phone:
        return
        
    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER:
        try:
            from twilio.rest import Client
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=text,
                from_=TWILIO_PHONE_NUMBER,
                to=to_phone
            )
            print(f"[Notifications:Twilio] SMS dispatched to {to_phone}")
            return
        except Exception as e:
            print(f"[Notifications:Twilio] Error: {e}")
            
    # Development audit log fallback
    print(f"📱 [SMS AUDIT LOG] To: {to_phone} | Message: {text}")
