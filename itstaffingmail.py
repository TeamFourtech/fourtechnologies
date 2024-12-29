from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import mailtrap as mt
import os

app = Flask(__name__)

# Enable CORS for the entire app
CORS(app)

@app.route('/send_it_staffing_email', methods=['POST'])
def send_it_staffing_email():
    try:
        # Debugging: Print the raw form data to check if it's being sent correctly
        print("Received Form Data:", request.form)

        # Strip any leading/trailing spaces from form data keys and values
        form_data = {key.strip(): value.strip() for key, value in request.form.items()}

        # Extract the data from the cleaned form
        first_name = form_data.get('first_name', '').strip()
        last_name = form_data.get('last_name', '').strip()
        email = form_data.get('email', '').strip()
        phone = form_data.get('phone', '').strip()
        company_name = form_data.get('company_name', '').strip()
        job_title = form_data.get('job_title', '').strip()
        hire_type = form_data.get('type_of_hire', '').strip()
        openings = form_data.get('number_of_openings', '').strip()
        location = form_data.get('job_location', '').strip()
        job_description = form_data.get('job_description', '').strip()

        # Print the cleaned form data for debugging
        print("Cleaned Form Data:", form_data)

        # Prepare Mailtrap email with dynamic recipient email and name
        mail = mt.MailFromTemplate(
            sender=mt.Address(email="itstaffing@fourtechnologies.in", name="Four Technologies"),
            to=[mt.Address(email=email)],
            template_uuid="97f56f88-c032-4882-9d66-623ca888b2f0",
            template_variables={
                "company_info_name": company_name,
                "first_name": first_name,
                "last_name": last_name,
                "name": f"{first_name} {last_name}",
                "phone": phone,
                "job_title": job_title,
                "hire_type": hire_type,
                "openings": openings,
                "location": location,
                "job_description": job_description,
                "message": "Thank you for reaching out to us regarding our IT staffing services. Sit back, relax, and allow us to handle the details. We will get back to you soon with your IT staffing proposal."
            }
        )

        # Initialize Mailtrap client and send email
        client = mt.MailtrapClient(token="520298668e9603dcedc48913ac4b0d9e")
        response = client.send(mail)

        # Return success response
        return jsonify({"status": "success", "message": "Email sent successfully."}), 200

    except Exception as e:
        # Log the error and return error response
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Ensure app listens on the correct host and port
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Adjust port if needed
    app.run(host='0.0.0.0', port=port, debug=True)
