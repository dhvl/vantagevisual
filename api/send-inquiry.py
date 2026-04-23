from http.server import BaseHTTPRequestHandler
import json
import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        contact_email = os.getenv("CONTACT_EMAIL", "sales@vantagevisual.co.uk")

        if not name or not email or not message:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing required fields"}).encode())
            return

        subject = f"New Inquiry: {data.get('service', 'General')} from {name}"
        
        html_content = f"""
        <h2>New Event Graphics Inquiry</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Company:</strong> {data.get('company', 'N/A')}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Phone:</strong> {data.get('phone', 'N/A')}</p>
        <p><strong>Service:</strong> {data.get('service')}</p>
        <p><strong>Event Date:</strong> {data.get('eventDate', 'N/A')}</p>
        <p><strong>Location:</strong> {data.get('location', 'N/A')}</p>
        <hr>
        <p><strong>Project Description:</strong></p>
        <p>{message}</p>
        """

        try:
            from_email = os.getenv("FROM_EMAIL", "Vantage Visual <onboarding@resend.dev>")
            params = {
                "from": from_email,
                "to": [contact_email],
                "subject": subject,
                "html": html_content,
                "reply_to": email
            }
            resend.Emails.send(params)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Enquiry sent successfully"}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
        
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
