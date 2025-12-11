import pandas as pd
from modelsync.engine.reconcile import reconcile
from modelsync.engine.state_machine import determine_state
from modelsync.engine.export import export_outputs


def main():
    reg = pd.read_csv("data/registry.csv")
    pl  = pd.read_csv("data/problem_list.csv")
    enc = pd.read_csv("data/encounters.csv")

    reconciled = reconcile(reg, pl, enc)
    export_outputs(reconciled, "output")

    print("\n=== Quick summary ===")
    print(reconciled['new_state'].value_counts())
    print("\nBy provider:")
    print(reconciled.groupby('ProviderNPI')['new_state'].value_counts().unstack(fill_value=0))


if __name__ == "__main__":
    main()
