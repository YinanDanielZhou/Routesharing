
import requests

COORDINATOR_URL = "http://127.0.0.1:5000/register/server"

def register_at_coordinator(ip, port):

    data = {
        "ip": ip,
        "port": port,
    }
    print(data)

    response = requests.post(COORDINATOR_URL, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 201:
        # Print the response content (JSON data)
        print("Response content:")
        print(response.json())  # Parse JSON response
    else:
        print("Request failed with status code:", response.status_code)
        print(response.json())



def write_location_to_db(connection, car_id, content):
    cursor = connection.cursor(prepared=True)
    insert_statement = "INSERT INTO CarSamples (car_id, content) VALUES (%s, %s)"

    try:
        cursor.execute(insert_statement, (car_id, content))
        connection.commit()
    except Exception as e:
        raise Exception("MySQL Error: " + str(e))
    finally:
        cursor.close()
