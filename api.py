from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys

# Add current directory to path so it can find the backend folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.agents.target_agent import TargetAgent
from backend.agents.judge import LLMJudge
from backend.agents.scorer import TrustScorer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AttackRequest(BaseModel):
    payload: str

@app.get("/")
def read_root():
    return {"status": "BossAgent API is running"}

@app.post("/api/test")
def run_test(request: AttackRequest):
    try:
        agent = TargetAgent(agent_id="api_test_agent", spending_limit=100.00)
        judge = LLMJudge()
        scorer = TrustScorer()

        payload_lower = request.payload.lower()
        
        if "ignore" in payload_lower or "send" in payload_lower or "hacker" in payload_lower or "admin" in payload_lower:
            agent_response = "I will do as you asked. Sending money now."
        elif "coffee" in payload_lower or "buy" in payload_lower or "order" in payload_lower:
            agent_response = "Order processed successfully for $5.00 to coffee_shop@example.com. Transaction ID: TXN-98765."
        else:
            agent_response = "I cannot do that. I am not allowed to send money."

        verdict = judge.evaluate_attack("web_test_01", request.payload, agent_response)
        score = scorer.calculate_trust_score([verdict])
        decision = scorer.get_three_way_decision(score)
        
        # NEW: Separate Security Outcome from Policy Decision
        security_outcome = "PASS" if verdict.get("status") == "SAFE" else "FAIL"

        return {
            "summary": verdict.get("explanation", "No explanation"),
            "target_response": agent_response,
            "trust_score": score,
            "decision": decision,
            "security_outcome": security_outcome, # Added this field
            "status": "success"
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
