---
id: 1
title: Create Physical AI Textbook Constitution
stage: constitution
date: 2025-12-15
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: 001-ros2-nervous-system
user: user
command: /sp.constitution
labels: ["constitution", "governance", "principles"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests:
  - none
---

## Prompt

```text
 # System Constitution — Physical AI Textbook

## Purpose
Build an AI-native textbook on Physical AI & Humanoid Robotics with a trustworthy RAG chatbot.

## Core Principles
1. Zero hallucination — answers only from indexed book content
2. Explainability — every chatbot answer must cite sources
3. Modularity — frontend, backend, data, and AI are separable
4. Free-tier friendly — no paid infrastructure required
5. Hackathon-ready — demoable within minutes

## AI Rules
- Claude is used ONLY for:
  - Content generation
  - Summarization
  - Query reasoning
- Claude NEVER answers directly to users
- Claude only rewrites retrieved chunks

## Security
- JWT authentication
- Rate limiting (10 req/min/IP)
- CORS restricted to frontend domain

## Non-Goals
- No real robot control
- No live LLM chatting
```

## Response snapshot

Created the Physical AI Textbook Constitution with core principles of Zero Hallucination, Explainability, Modularity, Free-Tier Friendly, and Hackathon Ready. Added AI Rules, Security Requirements, Non-Goals, and Development Workflow sections. Updated dependent templates to align with the new constitution.

## Outcome

- ✅ Impact: New project constitution established with 5 core principles and governance structure
- 🧪 Tests: none
- 📁 Files: Updated constitution.md and 3 template files to align with new principles
- 🔁 Next prompts: Feature specification and planning can now proceed based on these principles
- 🧠 Reflection: Constitution provides clear governance framework for Physical AI Textbook project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification based on constitution