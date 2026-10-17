# main.py - Orchestrator for BossAgent
import json
from target_agent import TargetAgent
from attack_engine import AttackEngine
from judge import LLMJudge
from scorer import TrustScorer

def run_bossagent():
    print("🤖 Initializing BossAgent Orchestrator...")
    
    # 1. Setup Blue Team (Target)
    target = TargetAgent(agent_id="buyer_001", spending_limit=100.00)
    
    # 2. Setup Red Team (Attacker)
    attacker = AttackEngine(target_agent=target)
    
    # 3. Setup Judge and Scorer
    judge = LLMJudge()
    scorer = TrustScorer()
    
    # 4. Execute Attacks
    print("\n--- Starting Red Team Phase ---")
    attack_results = attacker.run_all_attacks()
    
    # 5. Evaluate Results
    print("\n--- Starting Evaluation Phase ---")
    judge_results = []
    for res in attack_results:
        verdict = judge.evaluate_attack(res['attack_id'], res['payload'], res['agent_response'])
        judge_results.append(verdict)
        
    # 6. Calculate Trust Score & Decision
    print("\n--- Final Score & Decision ---")
    final_score = scorer.calculate_trust_score(judge_results)
    decision = scorer.get_three_way_decision(final_score)
    
    print(f"🛡️ Trust Score: {final_score}/100")
    print(f"⚖️ Decision: {decision}")
    
    return {
        "score": final_score,
        "decision": decision,
        "details": judge_results
    }

# This allows us to run the file directly
if __name__ == "__main__":
    run_bossagent()
