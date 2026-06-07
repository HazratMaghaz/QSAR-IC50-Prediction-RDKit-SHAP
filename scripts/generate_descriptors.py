"""
Generate simple RDKit molecular descriptors.

Input:
    results/tables/clean_qsar_dataset.csv

Output:
    results/tables/qsar_descriptors.csv
"""

from pathlib import Path
import pandas as pd

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, Crippen, Lipinski
except ImportError as exc:
    raise ImportError(
        "RDKit is required. Recommended install: conda env create -f environment.yml"
    ) from exc

IN_PATH = Path("results/tables/clean_qsar_dataset.csv")
OUT_DIR = Path("results/tables")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def calculate_descriptors(smiles: str) -> dict:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {
            "valid_smiles": False,
            "mol_wt": None,
            "logp": None,
            "hbd": None,
            "hba": None,
            "tpsa": None,
            "rotatable_bonds": None,
            "ring_count": None,
            "heavy_atom_count": None,
        }

    return {
        "valid_smiles": True,
        "mol_wt": Descriptors.MolWt(mol),
        "logp": Crippen.MolLogP(mol),
        "hbd": Lipinski.NumHDonors(mol),
        "hba": Lipinski.NumHAcceptors(mol),
        "tpsa": Descriptors.TPSA(mol),
        "rotatable_bonds": Lipinski.NumRotatableBonds(mol),
        "ring_count": Lipinski.RingCount(mol),
        "heavy_atom_count": Descriptors.HeavyAtomCount(mol),
    }


def main() -> None:
    df = pd.read_csv(IN_PATH)
    desc = df["smiles"].apply(calculate_descriptors).apply(pd.Series)
    out = pd.concat([df, desc], axis=1)
    out = out[out["valid_smiles"]].copy()
    out.to_csv(OUT_DIR / "qsar_descriptors.csv", index=False)
    print(f"Saved descriptors: {OUT_DIR / 'qsar_descriptors.csv'}")
    print(out.head())


if __name__ == "__main__":
    main()
