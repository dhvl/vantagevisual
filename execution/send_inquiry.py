import os
import resend
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

def send_inquiry_email(data):
    """
    Sends an inquiry email using Resend.
    
    Args:
        data (dict): A dictionary containing form data:
            - name: sender name
            - company: sender company
            - email: sender email
            - phone: sender phone
            - service: service required
            - eventDate: date of event
            - location: venue location
            - message: project description
    """
    contact_email = os.getenv("CONTACT_EMAIL", "sales@vantagevisual.co.uk")
    email_val = data.get('email', '').strip()
    
    # Validate email format to prevent Resend 422 error
    import re
    is_valid_email = bool(re.match(r"[^@]+@[^@]+\.[^@]+", email_val))
    
    reply_to_email = email_val if is_valid_email else "do-not-reply@vantagevisual.co.uk"
    email_note = "" if is_valid_email else "<p style='color: red; font-weight: bold;'>⚠️ WARNING: The sender provided an invalid email address. You cannot reply directly to this email. Please check their phone number or company details if provided.</p>"

    subject = f"New Inquiry: {data.get('service', 'General')} from {data.get('name')}"
    
    html_content = f"""
    {email_note}
    <h2>New Event Graphics Inquiry</h2>
    <p><strong>Name:</strong> {data.get('name')}</p>
    <p><strong>Company:</strong> {data.get('company', 'N/A')}</p>
    <p><strong>Email:</strong> {email_val} {"(INVALID)" if not is_valid_email else ""}</p>
    <p><strong>Phone:</strong> {data.get('phone', 'N/A')}</p>
    <p><strong>Service:</strong> {data.get('service')}</p>
    <p><strong>Event Date:</strong> {data.get('eventDate', 'N/A')}</p>
    <p><strong>Location:</strong> {data.get('location', 'N/A')}</p>
    <hr>
    <p><strong>Project Description:</strong></p>
    <p>{data.get('message')}</p>
    """
    
    params = {
        "from": "Vantage Visual <onboarding@resend.dev>", # Replace with your verified domain in Resend
        "to": [contact_email],
        "subject": subject,
        "html": html_content,
        "reply_to": reply_to_email
    }

    try:
        email = resend.Emails.send(params)
        return email
    except Exception as e:
        print(f"Error sending email: {e}")
        return None

if __name__ == "__main__":
    # Test data
    test_data = {
        "name": "Test User",
        "email": "test@example.com",
        "message": "This is a test inquiry from the execution script."
    }
    result = send_inquiry_email(test_data)
    if result:
        print("Test email sent successfully!")
        print(result)
    else:
        print("Failed to send test email.")
