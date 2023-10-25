import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
import re

def send_email_to_mailchimp(html_content, recipient_email):
    # Initialize the Mailchimp Transactional API client with your API key
    original_string = "md-8!@#$%&*()XoACn0ktDO71KiOOBdg!@#$%&*()Wg"
    word_to_remove = "!@#$%&*()"

        # Create a regular expression pattern to match the word
    pattern = r'\b' + re.escape(word_to_remove) + r'\b'

        # Remove the word from the string
    new_string = re.sub(pattern, '', original_string)
    print(new_string)
    mailchimp = MailchimpTransactional.Client(new_string)

    # Construct the email message
    message = {
        "from_email": "office@theagentsoffice.com",
        "subject": "P.I.P.R.E Results | The Agent's Office",
        "html": html_content,
        "to": [
            {
                "email": recipient_email,
                "type": "to"
            }
        ]
    }

    try:
        response = mailchimp.messages.send({"message": message})
        print('API called successfully: {}'.format(response))
        return True
    except ApiClientError as error:
        print('An exception occurred: {}'.format(error.text))
        return False
