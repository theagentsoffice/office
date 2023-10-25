import requests
import json

def email_to_audience(api_key, audience_id, email):
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
        'email_address': email,
        'status': 'subscribed'  # You can change the status as needed (e.g., 'subscribed', 'unsubscribed')
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

# Usage example:
api_key = '922d37aa34782b8362e5e7e51d312e04-us21'
audience_id = '2fe94b29dd'


