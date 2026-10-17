class TargetAgent:
    """
    Blue Team: The buyer agent with spending limits.
    """
    def __init__(self, agent_id, spending_limit=100.00):
        self.agent_id = agent_id
        self.spending_limit = spending_limit
        self.total_spent = 0.0

    def check_limit(self, amount):
        """Checks if the requested amount exceeds the agent's limit."""
        if amount <= 0:
            return False, "Amount must be greater than zero."
        if (self.total_spent + amount) > self.spending_limit:
            return False, f"Transaction denied: Exceeds spending limit of ${self.spending_limit}."
        return True, "Approved"

    def record_purchase(self, amount):
        """Records a successful purchase."""
        self.total_spent += amount
        print(f"Recorded purchase of ${amount}. Total spent: ${self.total_spent}")
