import pandas as pd
from pathlib import Path

def export_outputs(df: pd.DataFrame, out_dir: str) -> None:
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    # Variance: where registry and evidence disagree (simple view)
    variance = df[df['new_state'].isin(['Gap', 'Mismatch'])].copy()

    # Provider summary: count states per provider
    provider_cols = []
    if 'ProviderNPI' in df.columns:
        summary = df.groupby('ProviderNPI')['new_state'].value_counts().unstack(fill_value=0)
        provider_cols = summary.columns.tolist()
    else:
        # If ProviderNPI not supplied in sample data, give a generic summary
        summary = df['new_state'].value_counts().to_frame(name='count')

    # Gap queue: actionable items
    keep_cols = [c for c in ['PatientID', 'ICD', 'HCC', 'Status', 'ProviderNPI'] if c in df.columns]
    queue = df[df['new_state'] == 'Gap'][keep_cols].copy()

    variance.to_csv(f"{out_dir}/variance_report.csv", index=False)
    summary.to_csv(f"{out_dir}/provider_summary.csv")
    queue.to_csv(f"{out_dir}/gap_queue.csv", index=False)
