<!-- SYNC IMPACT REPORT
Version change: N/A (initial version) → 1.0.0
Modified principles: None (new constitution)
Added sections: All sections (initial constitution)
Removed sections: None
Templates requiring updates: ✅ updated - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# Physical AI Textbook Constitution

## Core Principles

### Zero Hallucination
Answers must only come from indexed book content. The system must not generate information beyond what exists in the source material.

### Explainability
Every chatbot answer must cite sources. Users must be able to verify the origin of all information provided by the system.

### Modularity
Frontend, backend, data, and AI components must be separable. Each component should function independently and communicate through well-defined interfaces.

### Free-Tier Friendly
No paid infrastructure required. The system must operate within free tier limits of cloud services to ensure accessibility.

### Hackathon Ready
Demoable within minutes. The system must be deployable and demonstrable quickly with minimal setup requirements.

## AI Rules
- Claude is used ONLY for:
  - Content generation
  - Summarization
  - Query reasoning
- Claude NEVER answers directly to users
- Claude only rewrites retrieved chunks

## Security Requirements
- JWT authentication
- Rate limiting (10 req/min/IP)
- CORS restricted to frontend domain

## Non-Goals
- No real robot control
- No live LLM chatting

## Development Workflow
- Content generation follows RAG pattern
- Frontend and backend development are separate
- All AI processing happens server-side

## Governance
- This constitution supersedes all other practices
- All changes must align with core principles
- Features must be tested against hallucination prevention

**Version**: 1.0.0 | **Ratified**: 2025-12-15 | **Last Amended**: 2025-12-15