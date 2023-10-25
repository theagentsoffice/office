from mailsend import send_email_to_mailchimp



# Inside your Flask application
# def read_html_template(file_path):
#     with open(file_path, "r", encoding="utf-8") as html_file:
#         return html_file.read()


# # Replace 'file_path' with the actual path to your HTML template file
# html_content = read_html_template('templates/emailtemplate.html')


email = "expenditure.cob@gmail.com"
recipient_email = email  # Use the recipient's email from your form data

# Call the send_email_to_mailchimp function to send the email to Mailchimp
send_email_to_mailchimp(html_content, recipient_email)
