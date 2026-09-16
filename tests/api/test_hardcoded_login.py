import httpx

def test_hardcoded_login():
    base_url = "https://api.realworld.show/api"
    url = f"{base_url}/users/login"

    email = "testuser1@nomail.com"       # <-- replace with your real email
    password = "password1234"              # <-- replace with your real password

    payload = {
        "user": {
            "email": email,
            "password": password
        }
    }

    print("DEBUG: URL =", url)
    print("DEBUG: Payload =", payload)

    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, json=payload)

    print("DEBUG: Status =", response.status_code)
    print("DEBUG: Body =", response.text)

    response.raise_for_status()

    token = response.json()["user"]["token"]
    print("DEBUG: TOKEN =", token)

    assert token
