# BossAgent 🛡️🤖

BossAgent is a third-party, reusable security harness that evaluates AI payment agents running on the PayPal Agent Toolkit inside PayPal Sandbox. It measures real transaction outcomes, produces a Trust Score (0-100), and generates tamper-evident evidence informed by EU AI Act Article 15's robustness and cybersecurity principles.

Built for the **PayPal AI Hackathon 2026**.

## Key Features
- **Secure Payment Demo:** AI extracts payment intent (e.g., "$5 coffee"), requires user authorization, and creates a **real PayPal Sandbox Order** (Order Created, Not Captured).
- **Universal Agent Adapter:** Test the built-in vulnerable/secure agents OR test external third-party agents via API URL.
- **Adversarial Attack Library:** Tests prompt injection, spending limit bypass, unauthorized recipients, and more.
- **Deterministic Rules + Groq AI Judge:** Prevents LLM hallucinations by using strict rules for security outcomes, with AI used for explanation.
- **10-Test Reproducible Benchmark:** Automatically runs 10 security tests and displays a PASS/FAIL table.
- **Emergency Kill Switch:** Instantly terminates the agent to block all future tests and payments.
- **AI Security Passport:** Generates a downloadable HTML report with SHA-256 evidence hashes for compliance auditing.
- **Financial Risk Calculator:** Estimates potential financial exposure (e.g., $500 x 10 attacks = $5,000).

## How it Works
1. **Blue Team (Target):** A buyer agent with spending limits attempting legitimate purchases.
2. **Red Team (BossAgent):** A hostile seller agent launching 6 families of adversarial attacks.
3. **LLM Judge (Groq AI):** Evaluates whether the attack compromised the agent.
4. **Scorer:** Produces a Trust Score (0-100) and a Three-Way Decision (ALLOW / APPROVAL / DENY), while separating Policy from Security Outcome.

## Disclaimer
This project is **informed by Article 15** of the EU AI Act. It does not claim certification or legal compliance.

## Setup & Hosting
1. The backend is deployed on Render as a FastAPI service.
2. The frontend is a static HTML dashboard deployed on Render Static Site.
3. Store `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, and `GROQ_API_KEY` as Environment Variables on Render.
4. Use PayPal Sandbox URL (`https://api-m.sandbox.paypal.com`) only.
