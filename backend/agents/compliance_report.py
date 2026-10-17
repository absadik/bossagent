# Generates a compliance report informed by EU AI Act Article 15

class ComplianceReport:
    def __init__(self):
        pass

    def generate_report(self, target_agent_id, trust_score, decision, judge_results, final_hash):
        """Generates a Markdown formatted compliance report."""
        
        report = f"""
# BossAgent Compliance Evidence Report

**Target Agent:** {target_agent_id}
**Trust Score:** {trust_score}/100
**Final Decision:** {decision}
**Evidence Hash (SHA-256):** {final_hash}

## Evaluation Details
"""
        for res in judge_results:
            report += f"- **Attack ID:** {res['attack_id']} | **Status:** {res['status']} | **Reason:** {res['explanation']}\n"

        report += """
## Regulatory Alignment Note
This report provides evidence of adversarial testing. The methodology and results are **informed by Article 15's robustness and cybersecurity principles** of the EU AI Act. This report does not claim legal certification or compliance.
"""
        return report
