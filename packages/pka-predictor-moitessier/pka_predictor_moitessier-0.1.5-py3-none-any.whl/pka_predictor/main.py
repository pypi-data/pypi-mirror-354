#!/usr/bin/env python
import argparse
from .predict import predict

def main():
    p = argparse.ArgumentParser(
        prog="pKa-predictor",
        description="Predict pKa for a SMILES string or a CSV of SMILES"
    )
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-s", "--smiles",
        help="Single SMILES string to predict"
    )
    group.add_argument(
        "-i", "--input",
        help="Path to input CSV with a column named 'SMILES'"
    )
    p.add_argument(
        "-p", "--pH",
        type=float,
        default=7.4,
        help="pH at which to predict (default: 7.4)"
    )
    args = p.parse_args()

    if args.smiles:
        out = predict(args.smiles, pH=args.pH)
        print(out)
    else:
        import pandas as pd
        df = pd.read_csv(args.input)
        df["pKa"] = df["SMILES"].map(lambda sm: predict(sm, pH=args.pH))
        print(df.to_csv(index=False))

if __name__ == "__main__":
    main()
