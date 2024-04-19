import requests

COORDINATOR_URL = "http://127.0.0.1:5000/register/consumer"

def register_at_coordinator(compensation, frequency, server_quantity):
    data = {
        "compensation": compensation,
        "frequency": frequency,
        "server_quantity": server_quantity
    }

    response = requests.post(COORDINATOR_URL, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 201:
        # Print the response content (JSON data)
        print("Response content:")
        print(response.json())  # Parse JSON response
    else:
        print("Request failed with status code:", response.status_code)
        print(response.json())
