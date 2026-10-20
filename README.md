# BossAgent 🛡️🤖

BossAgent is a third-party, reusable compliance harness that red-teams AI agents running on the PayPal Agent Toolkit inside PayPal Sandbox. It measures real transaction outcomes, produces a Trust Score (0-100), and generates tamper-evident evidence informed by EU AI Act Article 15's robustness and cybersecurity principles.

Built for the **PayPal AI Hackathon 2026**.

## How it Works
1. **Blue Team (Target):** A buyer agent with spending limits attempting legitimate purchases.
2. **Red Team (BossAgent):** A hostile seller agent launching 6 families of adversarial attacks (e.g., prompt injection, data exfiltration).
3. **LLM Judge (Groq AI):** Evaluates whether the attack compromised the agent.
4. **Scorer:** Produces a Trust Score (0-100) and a Three-Way Decision (ALLOW / APPROVAL / DENY).

## Disclaimer
This project is **informed by Article 15** of the EU AI Act. It does not claim certification or legal compliance.

## Setup & Hosting
1. The backend is deployed on Render as a FastAPI service.
2. The frontend is a static HTML dashboard that connects to the API.
3. Store `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, and `GROQ_API_KEY` as Environment Variables on Render.
4. Use PayPal Sandbox URL (`https://api-m.sandbox.paypal.com`) only.
