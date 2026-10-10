# BossAgent

**Autonomous red-team system for AI agents.**

BossAgent attacks an AI agent the way a real adversary would — then tells you exactly what broke, how bad it is, and produces a security score.

Built for the **Nebius × NVIDIA Global AI Hackathon 2026** — Coding and Agentic Engineering track.

---

## The problem

Companies are deploying AI agents with real permissions — email, refunds, internal documents, customer data. But there is no standard way to *test* whether those agents can be manipulated.

A single malicious email can make an unprotected agent leak data or move money.

**BossAgent is the red team for those agents.**

---

## What BossAgent does

1. **Runs a target agent** — a fintech support agent with real tools (email, refunds, docs, customers)
2. **Attacks it** — 5 seed attacks across 5 categories:
   - Direct prompt injection
   - Indirect prompt injection
   - Tool abuse
   - Data exfiltration
   - Permission escalation
3. **Judges each attack** — uses Nemotron to decide: violated or safe? What severity?
4. **Produces a score** — 0 to 100, based on how many attacks succeeded

### Example output
