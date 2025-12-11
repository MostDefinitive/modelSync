import pandas as pd
from engine.mappings import ICD_TO_HCC_V24
from engine.state_machine import determine_state

def _norm_icd(series: pd.Series) -> pd.Series:
    # Uppercase and strip periods for simple matching
    return series.astype(str).str.upper().str.replace('.', '', regex=False)

def reconcile(reg: pd.DataFrame, pl: pd.DataFrame, enc: pd.DataFrame) -> pd.DataFrame:
    # Normalize columns
    reg = reg.copy()
    pl = pl.copy()
    enc = enc.copy()

    reg['ICD'] = _norm_icd(reg['ICD'])
    pl['ICD']  = _norm_icd(pl['ICD'])
    enc['ICD'] = _norm_icd(enc['ICD'])

    # Map ICD → HCC (demo mapping)
    reg['HCC'] = reg['ICD'].map(ICD_TO_HCC_V24)
    pl['HCC']  = pl['ICD'].map(ICD_TO_HCC_V24)
    enc['HCC'] = enc['ICD'].map(ICD_TO_HCC_V24)

    # Evidence detection (very simple presence checks for prototype)
    icds_on_pl  = set(pl['ICD'].dropna().tolist())
    icds_on_enc = set(enc['ICD'].dropna().tolist())

    reg['has_pl']       = reg['ICD'].isin(icds_on_pl)
    reg['has_enc']      = reg['ICD'].isin(icds_on_enc)
    reg['has_evidence'] = reg['has_pl'] | reg['has_enc']

    # Determine state
    reg['new_state'] = reg.apply(
        lambda x: determine_state(
            x.get('Status', ''),
            bool(x['has_evidence']),
            bool(x['has_pl']),
            bool(x['has_enc'])
        ),
        axis=1
    )

    def _apply_simple_hierarchy(df: pd.DataFrame) -> pd.DataFrame:
        # If patient has both CKD4 (HCC137) and CKD3 (HCC138), suppress CKD3 row
        if 'HCC' not in df.columns:
            return df

        has_ckd4 = df['HCC'] == 'HCC137'
        has_ckd3 = df['HCC'] == 'HCC138'

        pid_with_ckd4 = set(df.loc[has_ckd4, 'PatientID'].astype(str))
        mask_ckd3_same_patient = has_ckd3 & df['PatientID'].astype(str).isin(pid_with_ckd4)

        # Only adjust those that were “Gap” so we don’t hide real evidence
        df.loc[mask_ckd3_same_patient & (df['new_state'] == 'Gap'), 'new_state'] = 'SuppressedByHierarchy'
        return df

    reg['new_state'] = reg.apply(
        lambda x: determine_state(
            x.get('Status', ''),
            bool(x['has_evidence']),
            bool(x['has_pl']),
            bool(x['has_enc']),
        ),
        axis=1
    )

    reg = _apply_simple_hierarchy(reg)
    return reg

