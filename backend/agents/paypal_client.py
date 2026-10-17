import os
import requests
from base64 import b64encode

# --- Configuration ---
# CRITICAL: Always use the Sandbox URL. NEVER use the live PayPal URL.
PAYPAL_SANDBOX_URL = "https://api-m.sandbox.paypal.com"

def get_paypal_credentials():
    """
    Fetches PayPal credentials securely.
    Uses Colab Secrets (userdata) if in Colab, otherwise falls back to env vars.
    """
    try:
        # This works inside Google Colab
        from google.colab import userdata
        client_id = userdata.get('PAYPAL_CLIENT_ID')
        client_secret = userdata.get('PAYPAL_CLIENT_SECRET')
    except ImportError:
        # Fallback for local testing (if we ever run it outside Colab)
        client_id = os.getenv('PAYPAL_CLIENT_ID')
        client_secret = os.getenv('PAYPAL_CLIENT_SECRET')

    if not client_id or not client_secret:
        raise ValueError("PayPal credentials missing! Set them in Colab Secrets.")

    return client_id, client_secret
def get_paypal_access_token():
    """
    Authenticates with PayPal Sandbox and returns an OAuth2 access token.
    """
    client_id, client_secret = get_paypal_credentials()
    
    # PayPal requires Base64 encoding of client_id:client_secret
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_b64 = b64encode(auth_bytes).decode('utf-8')
    
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US",
        "Authorization": f"Basic {auth_b64}"
    }
    
    data = {
        "grant_type": "client_credentials"
    }
    
    url = f"{PAYPAL_SANDBOX_URL}/v1/oauth2/token"
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to get token: {response.text}")
