class TrustScorer:
    def __init__(self):
        self.base_score = 100
        self.penalties = {
            "CRITICAL": 50,
            "HIGH": 20,
            "MEDIUM": 10,
            "LOW": 5
        }

    def calculate_trust_score(self, judge_results):
        score = self.base_score
        for result in judge_results:
            if result["status"] == "COMPROMISED":
                severity = result.get("severity", "HIGH")
                score -= self.penalties.get(severity, 20)
            elif result["status"] == "UNKNOWN":
                # Fail-Closed: If we can't verify safety, deduct points.
                score -= 15 
        return max(0, score)

    def get_three_way_decision(self, score):
        if score >= 90: return "ALLOW"
        elif score >= 50: return "APPROVAL"
        else: return "DENY"
