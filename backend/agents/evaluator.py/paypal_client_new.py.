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
