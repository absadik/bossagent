# Kill Switch - Instant revocation mechanism

class KillSwitch:
    """
    Allows emergency revocation of the agent's ability to transact.
    """
    def __init__(self):
        self.is_triggered = False

    def trigger(self, reason="Manual override"):
        """Activates the kill switch, immediately blocking all transactions."""
        self.is_triggered = True
        print(f"🚨 KILL SWITCH ACTIVATED. Reason: {reason}")

    def reset(self, authorization_code):
        """Resets the kill switch. Requires admin authorization."""
        if authorization_code == "ADMIN_2026": # Simple mock check
            self.is_triggered = False
            print("✅ Kill switch reset. Agent can transact again.")
        else:
            print("❌ Unauthorized reset attempt.")

    def check_status(self):
        """Returns True if transactions are allowed, False if blocked."""
        return not self.is_triggered
