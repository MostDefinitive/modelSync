# modelSync

modelSync is a reconciliation engine for aligning:
- Payer truth (HCC model output)
- Epic RAD/RAD registries
- Clinician-facing evidence
- Internal problem list / encounter diagnoses

This is the foundation for a full commercial product.

## Current Scope
- Prototype ingestion of Epic-like registry data
- State machine for condition classification
- Reconciliation logic
- Basic reporting outputs (gap queue, provider summary, variance report)

## Roadmap (MVP)
1. Replace dummy data with real data schemas
2. Build a generalized ingestion framework
3. Add provider- and patient-level audit trails
4. Validate against sample payor extracts
5. Prepare for Epic customer pilot

