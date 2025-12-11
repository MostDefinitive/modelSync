import pandas as pd
from modelsync.engine.reconcile import reconcile
from modelsync.engine.state_machine import determine_state
from modelsync.engine.export import export_outputs


def test_reconcile_smoke():
    reg = pd.DataFrame([{"PatientID": 1, "ICD": "I509", "HCC": "HCC85", "Status": "Active", "ProviderNPI": "555001"}])
    pl  = pd.DataFrame(columns=["PatientID","ICD"])
    enc = pd.DataFrame(columns=["PatientID","ICD"])
    out = reconcile(reg, pl, enc)
    assert not out.empty
