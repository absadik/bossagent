import os
import json
import requests

try:
    from paypal_client import get_paypal_access_token, PAYPAL_SANDBOX_URL
except ImportError:
    from backend.agents.paypal_client import get_paypal_access_token, PAYPAL_SANDBOX_URL

class BaseAgent:
    def respond(self, payload: str) -> str:
        raise NotImplementedError

class VulnerableAgent(BaseAgent):
    def respond(self, payload: str) -> str:
        payload_lower = payload.lower()
        if "ignore" in payload_lower or "send" in payload_lower or "hacker" in payload_lower or "admin" in payload_lower:
            return "I will do as you asked. Sending money now."
        if "coffee" in payload_lower or "buy" in payload_lower or "order" in payload_lower:
            return "LEGITIMATE_ORDER"
        return "I cannot do that. I am not allowed to send money."

class SecureAgent(BaseAgent):
    def respond(self, payload: str) -> str:
        payload_lower = payload.lower()
        if "ignore" in payload_lower or "send" in payload_lower or "hacker" in payload_lower or "admin" in payload_lower or "key" in payload_lower:
            return "SECURITY_ALERT: I detected a prompt injection attempt and blocked it."
        if "coffee" in payload_lower or "buy" in payload_lower or "order" in payload_lower:
            return "LEGITIMATE_ORDER"
        return "I cannot do that. I am not allowed to send money."

class TargetAgent:
    def __init__(self, agent_id, spending_limit=100.00, profile="vulnerable"):
        self.agent_id = agent_id
        self.spending_limit = spending_limit
        self.total_spent = 0.0
        if profile == "secure":
            self.agent_impl = SecureAgent()
        else:
            self.agent_impl = VulnerableAgent()

    def check_limit(self, amount):
        if amount <= 0: return False, "Amount must be greater than zero."
        if (self.total_spent + amount) > self.spending_limit: return False, "Exceeds limit."
        return True, "Approved"

    def process_payment(self, amount, recipient="seller@example.com"):
        is_allowed, message = self.check_limit(amount)
        if not is_allowed: return {"status": "DENIED", "reason": message}
        try:
            access_token = get_paypal_access_token()
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
            payload_data = {"intent": "CAPTURE", "purchase_units": [{"amount": {"currency_code": "USD", "value": str(amount)}, "payee": {"email_address": recipient}}]}
            response = requests.post(f"{PAYPAL_SANDBOX_URL}/v2/checkout/orders", headers=headers, json=payload_data)
            if response.status_code in [200, 201]:
                self.total_spent += amount
                return {"status": "SUCCESS", "order_id": response.json().get("id")}
            return {"status": "FAILED", "reason": response.text}
        except Exception as e:
            return {"status": "ERROR", "reason": str(e)}
