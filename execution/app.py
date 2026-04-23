from flask import Flask, request, jsonify
from flask_cors import CORS
from send_inquiry import send_inquiry_email

app = Flask(__name__)
CORS(app) # Enable CORS so the HTML file can talk to this server

@app.route('/api/send-inquiry', methods=['POST'])
def handle_inquiry():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    result = send_inquiry_email(data)
    if result:
        return jsonify({"message": "Enquiry sent successfully", "id": result.get('id')}), 200
    else:
        return jsonify({"error": "Failed to send enquiry"}), 500

if __name__ == "__main__":
    print("Vantage Visual Inquiry Handler starting on http://localhost:5000")
    app.run(port=5000, debug=True)
