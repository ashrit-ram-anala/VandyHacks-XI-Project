from flask import Flask
import requests
import time
import json
import threading

# Function to send the JSON data via a POST request to the Node.js backend
def send_json_to_nodejs():
    while True:
        # Fetch the JSON data from the other server




        if json_data:
            try:
                # Send a POST request with the JSON data to the Node.js endpoint
                headers = {'Content-Type': 'application/json'}
                response = requests.post('http://localhost:8080/api/save-tkr', data=json.dumps(json_data), headers=headers)
                if response.status_code == 200:
                    print(f"POST request successful: {response.json()}")
                else:
                    print(f"Failed POST request. Status code: {response.status_code}")

            except Exception as e:
                print(f"Error sending POST request: {e}")

        time.sleep(0.8)  # Wait 5 seconds before fetching and sending data again

# Run the Flask app and start the POST request loop in a separate thread
if __name__ == "__main__":
    # Start the POST request function in a background thread
    post_request_thread = threading.Thread(target=send_json_to_nodejs)
    post_request_thread.daemon = True  # Ensure thread exits when Flask app stops
    post_request_thread.start()


    # Start the Flask app
    app.run(debug=True)
