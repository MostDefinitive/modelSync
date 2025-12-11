import pandas as pd
from modelsync.engine.state_machine import determine_state

def test_gap_when_no_evidence_and_active():
    row = pd.Series({
        "Status": "Active",
        "has_pl": False,
        "has_enc": False,
        "has_evidence": False
    })
    assert determine_state(row) == "Gap"
