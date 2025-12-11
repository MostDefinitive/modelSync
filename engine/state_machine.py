# engine/state_machine.py
def determine_state(registry_status, has_evidence, has_pl, has_encounter):
    """
    registry_status: 'Active', 'Closed', 'Suspect', 'Suppressed'
    has_evidence: PL or Encounter present
    """
    if has_evidence:
        # Evidence (PL or Encounter) is enough to treat as validated in this prototype
        return "Validated"

    if registry_status == "Active" and not has_evidence:
        return "Gap"

    if registry_status == "Closed" and has_evidence:
        return "Mismatch"

    # If it's Suspect but we have *some* corroboration (PL or encounter), mark as Upgrade
    if registry_status == "Suspect" and (has_pl or has_encounter):
        return "Upgrade"

    return registry_status
