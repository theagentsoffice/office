import requests
import json

def email_to_audience(api_key, audience_id, email,name):
    # Mailchimp API endpoint
    base_url = 'https://us21.api.mailchimp.com/3.0'
    # Replace <dc> with the data center prefix of your Mailchimp account. You can find it in your API key.

    # Create a headers dictionary with the API key
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Define the endpoint URL to add a member to the audience
    url = f'{base_url}/lists/{audience_id}/members'

    # Create a data dictionary with the email to be added
    data = {
        'First Name':name,
        'email_address': email,
        'status': 'subscribed' ,
          'merge_fields': {
            'FNAME': name  # Use the appropriate merge field tag for the first name
        } # You can change the status as needed (e.g., 'subscribed', 'unsubscribed')
    }

    # Convert the data dictionary to a JSON string
    data_json = json.dumps(data)

    # Send a POST request to add the email to the audience
    response = requests.post(url, headers=headers, data=data_json)

    if response.status_code == 200:
        print(f"Email {email} added to the audience.")
    else:
        print(f"Failed to add email {email} to the audience. Status code: {response.status_code}")
        print(response.text)

import hashlib
import mailchimp_marketing

from mailchimp_marketing.api_client import ApiClientError
from mailchimp_marketing import Client

from mailchimp_marketing import Client


def emaiil_to_audience(email, api_key,audience_id):
    LIST_ID = audience_id  # Replace with your actual list ID
    SUBSCRIBER_HASH = hashlib.md5(email.encode('utf-8')).hexdigest()

    client = Client()
    
    # Set the API key and server using the provided parameters
    client.set_config({
        "api_key": api_key,
        "server": "us21"  # Replace with your actual server prefix
    })
    

    try:
        response = client.lists.update_list_member_tags(LIST_ID, SUBSCRIBER_HASH, {
            "tags": [{
                "name": "pipre_sub",
                "status": "active"
            }]
        })
        print("client.lists.update_list_member_tags() response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))


import re
audience_id = '04ce018b2b'
#api_key = '922d37aa34782b8362e5e7e51d312e04-us21'
original_string = "cd053!@#$%&*()6c2b57c4ae3e!@#$%&*()9c02d002583a134-us21"
word_to_remove = "!@#$%&*()"

# Create a regular expression pattern to match the word
pattern = r'\b' + re.escape(word_to_remove) + r'\b'


new_string = re.sub(pattern, '', original_string)
original_string ="f2!@#$%&*()b72c9336378!@#$%&*()8fbd2bcca466459c5df-us21"
word_to_remove = "!@#$%&*()"
pattern = r'\b' + re.escape(word_to_remove) + r'\b'


newstring = re.sub(pattern, '', original_string)


# # Usage example:
# api_key = '922d37aa34782b8362e5e7e51d312e04-us21'
# audience_id = '04ce018b2b'
# email="expenditure.cob@gmail.com"

# email_to_audience(new_string, audience_id, email)
# emaiil_to_audience(newstring, audience_id, email)

