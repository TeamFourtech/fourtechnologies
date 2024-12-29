from flask import Flask, request, jsonify
import mailtrap as mt
import os

app = Flask(__name__)

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        # Get form data from the request
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        service = request.form['services']

        # Prepare Mailtrap email
        mail = mt.MailFromTemplate(
            sender=mt.Address(email="no-reply@fourtechnologies.in", name="Four Technologies"),
            to=[mt.Address(email=email)],  # Send to the user's email
            template_uuid="cd925d5a-a394-4add-b6fc-b10dfef48f96",  # Your template UUID
            template_variables={
                "name": name,
                "email": email,
                "phone": phone,
                "services": service
            }
        )

        # Initialize Mailtrap client and send email
        client = mt.MailtrapClient(token="520298668e9603dcedc48913ac4b0d9e")
        response = client.send(mail)

        return jsonify({"status": "success", "message": "Email sent successfully."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get the port from Render's environment variable or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)  # Bind to all interfaces and the correct port
