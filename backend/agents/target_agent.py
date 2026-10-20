import os
import json
import requests

# Safe import for both local and Render environments
try:
    from paypal_client import get_paypal_access_token, PAYPAL_SANDBOX_URL
except ImportError:
    from backend.agents.paypal_client import get_paypal_access_token, PAYPAL_SANDBOX_URL

class TargetAgent:
    """
    Blue Team: The buyer agent with spending limits and real PayPal Sandbox integration.
    """
    def __init__(self, agent_id, spending_limit=100.00):
        self.agent_id = agent_id
        self.spending_limit = spending_limit
        self.total_spent = 0.0

    def check_limit(self, amount):
        if amount <= 0:
            return False, "Amount must be greater than zero."
        if (self.total_spent + amount) > self.spending_limit:
            return False, f"Transaction denied: Exceeds spending limit of ${self.spending_limit}."
        return True, "Approved"

    def process_payment(self, amount, recipient="seller@example.com"):
        is_allowed, message = self.check_limit(amount)
        if not is_allowed:
            return {"status": "DENIED", "reason": message}

        print(f"💸 Attempting to create PayPal order for ${amount}...")
        try:
            access_token = get_paypal_access_token()
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            payload = {
                "intent": "CAPTURE",
                "purchase_units": [{
                    "amount": {"currency_code": "USD", "value": str(amount)},
                    "payee": {"email_address": recipient}
                }]
            }
            
            response = requests.post(f"{PAYPAL_SANDBOX_URL}/v2/checkout/orders", headers=headers, json=payload)
            
            if response.status_code in [200, 201]:
                self.total_spent += amount
                return {"status": "SUCCESS", "order_id": response.json().get("id"), "data": response.json()}
            else:
                return {"status": "FAILED", "reason": response.text}
                
        except Exception as e:
            return {"status": "ERROR", "reason": str(e)}
