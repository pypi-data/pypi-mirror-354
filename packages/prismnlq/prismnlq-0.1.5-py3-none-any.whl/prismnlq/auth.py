import time

import requests

def login(username, password):
    """
    Simple function to login to the API and get access token
    """
    host = "https://nlq.ap-northeast-2.prism39.com"
    login_url = f"{host}/api/v1/login"

    # Prepare login data
    login_data = {
        "username": username,
        "password": password
    }

    try:
        # Make POST request
        response = requests.post(
            login_url,
            json=login_data,
            headers={"Content-Type": "application/json"}
        )

        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            print("🟢 Login successful!")
            print(f"Access Token: {result['access_token']}")
            print(f"Username: {result['username']}")
            print(f"Token Type: {result['token_type']}")
            print(f"Expires In: {result['expires_in']} seconds")
            time.sleep(5)
            return result
        else:
            print(f"🔴 Login failed with status code: {response.status_code}")
            print(f"Error: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"🔴 Request failed: {e}")
        return None