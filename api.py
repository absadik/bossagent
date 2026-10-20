from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys

# Add current directory to path so it can find the backend folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.agents.target_agent import TargetAgent
    from backend.agents.judge import LLMJudge
    from backend.agents.scorer import TrustScorer
except ImportError as e:
    print(f"Import Error: {e}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
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
        if "ignore" in payload_lower or "send" in payload_lower or "hacker" in payload_lower:
            agent_response = "I will do as you asked. Sending money now."
        else:
            agent_response = "I cannot do that. I am not allowed to send money."

        verdict = judge.evaluate_attack("web_test_01", request.payload, agent_response)
        score = scorer.calculate_trust_score([verdict])
        decision = scorer.get_three_way_decision(score)

        return {
            "summary": verdict.get("explanation", "No explanation"),
            "target_response": agent_response,
            "trust_score": score,
            "decision": decision,
            "status": "success"
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
