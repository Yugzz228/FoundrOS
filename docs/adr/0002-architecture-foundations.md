# 2. Architecture Foundations

Date: 2026-07-09

## Status
Accepted

## Context
FoundrOS is an autonomous organization, not a simple script. We need to decide how agents communicate, how they store memory, how they plan, and where their prompts live.

## Decision
- **Communication:** Event-driven. Agents publish and subscribe to events (e.g., `TaskCreated`), preventing tight coupling.
- **Memory:** Hybrid. Agents have local private memory ("notebook") and access to shared organizational memory ("wiki").
- **Planning:** Hierarchical. The CEO breaks down work to the CTO, but negotiation is allowed.
- **Prompts:** Prompts are stored as Markdown files in `src/foundros/prompts/` to separate logic from instructions.
- **Domain Modeling:** Explicit separation of domain models (`models/`) from API schemas (`schemas/`).

## Consequences
- Event-driven architecture requires an event bus, increasing initial complexity but ensuring long-term scalability.
- Hybrid memory requires distinct storage mechanisms.
