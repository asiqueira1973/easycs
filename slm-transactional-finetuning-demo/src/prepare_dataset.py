"""Prepare loan approval transactions as an instruction-tuning JSONL dataset."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Iterable

import pandas as pd
from sklearn.model_selection import train_test_split

INSTRUCTION = "Analyze the loan application based on the company's historical credit decisions."

EXPECTED_COLUMNS = [
    "loan_id",
    "no_of_dependents",
    "education",
    "self_employed",
    "income_annum",
    "loan_amount",
    "loan_term",
    "cibil_score",
    "residential_assets_value",
    "commercial_assets_value",
    "luxury_assets_value",
    "bank_asset_value",
    "loan_status",
]

ASSET_COLUMNS = [
    "residential_assets_value",
    "commercial_assets_value",
    "luxury_assets_value",
    "bank_asset_value",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert loan approval CSV rows into instruction-tuning JSONL files."
    )
    parser.add_argument(
        "--input",
        default="data/raw/loan_approval_dataset.csv",
        help="Path to the raw loan approval CSV file.",
    )
    parser.add_argument(
        "--output-dir",
        default="data/processed",
        help="Directory where train, test, and sample JSONL files will be written.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Fraction of rows to place in the test split.",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=20,
        help="Number of rows to write to sample.jsonl.",
    )
    return parser.parse_args()


def validate_columns(dataframe: pd.DataFrame) -> None:
    missing_columns = [column for column in EXPECTED_COLUMNS if column not in dataframe.columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        expected = ", ".join(EXPECTED_COLUMNS)
        raise ValueError(
            f"Missing required columns: {missing}. Expected columns are: {expected}"
        )


def load_dataset(input_path: Path) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    dataframe = pd.read_csv(input_path)
    dataframe.columns = dataframe.columns.str.strip()
    validate_columns(dataframe)
    dataframe["loan_status"] = dataframe["loan_status"].astype(str).str.strip()
    return dataframe


def format_input(row: pd.Series) -> str:
    return (
        f"Applicant has {row['no_of_dependents']} dependents, is {row['education']}, "
        f"self-employed status is {row['self_employed']}, annual income is {row['income_annum']}, "
        f"requested loan amount is {row['loan_amount']}, loan term is {row['loan_term']} months, "
        f"CIBIL score is {row['cibil_score']}, residential assets value is "
        f"{row['residential_assets_value']}, commercial assets value is "
        f"{row['commercial_assets_value']}, luxury assets value is {row['luxury_assets_value']}, "
        f"and bank asset value is {row['bank_asset_value']}."
    )


def as_number(value: object) -> float:
    return float(pd.to_numeric(value, errors="coerce"))


def build_reason(row: pd.Series, decision: str) -> str:
    cibil_score = as_number(row["cibil_score"])
    income_annum = as_number(row["income_annum"])
    loan_amount = as_number(row["loan_amount"])
    total_assets = sum(as_number(row[column]) for column in ASSET_COLUMNS)
    loan_to_income = loan_amount / income_annum if income_annum else float("inf")

    strengths = []
    risks = []

    if cibil_score >= 700:
        strengths.append("a strong credit profile")
    elif cibil_score >= 600:
        strengths.append("an acceptable credit profile")
    else:
        risks.append("a weak credit profile")

    if loan_to_income <= 3:
        strengths.append("a loan amount that is compatible with annual income")
    else:
        risks.append("a high loan amount compared with annual income")

    if total_assets >= loan_amount:
        strengths.append("asset values that provide meaningful financial support")
    else:
        risks.append("asset values that are limited relative to the requested loan")

    if decision == "approve":
        if strengths:
            return f"The applicant has {join_phrases(strengths)}."
        return "The historical decision approved this application based on the available financial profile."

    if risks:
        return f"The application shows {join_phrases(risks)}."
    return "The historical decision rejected this application after reviewing the available financial profile."


def join_phrases(phrases: list[str]) -> str:
    if len(phrases) == 1:
        return phrases[0]
    if len(phrases) == 2:
        return f"{phrases[0]} and {phrases[1]}"
    return f"{', '.join(phrases[:-1])}, and {phrases[-1]}"


def normalize_decision(loan_status: object) -> str:
    status = str(loan_status).strip().lower()
    if status == "approved":
        return "approve"
    if status == "rejected":
        return "reject"
    raise ValueError(
        f"Unsupported loan_status value: {loan_status!r}. Expected Approved or Rejected."
    )


def build_output(row: pd.Series) -> str:
    decision = normalize_decision(row["loan_status"])
    reason = build_reason(row, decision)

    if decision == "approve":
        recommended_action = "Proceed with loan approval."
        customer_message = (
            "Your loan application was approved based on the analysis of your financial "
            "profile and credit history."
        )
    else:
        recommended_action = "Do not approve the loan at this time; ask the applicant to improve risk factors."
        customer_message = (
            "Your loan application was not approved at this time based on the analysis "
            "of your financial profile and credit history."
        )

    return (
        f"Decision: {decision}\n"
        f"Reason: {reason}\n"
        f"Recommended action: {recommended_action}\n"
        f"Customer message: {customer_message}"
    )


def row_to_example(row: pd.Series) -> dict[str, str]:
    return {
        "instruction": INSTRUCTION,
        "input": format_input(row),
        "output": build_output(row),
    }


def write_jsonl(records: Iterable[dict[str, str]], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def prepare_dataset(input_path: Path, output_dir: Path, test_size: float, sample_size: int) -> None:
    dataframe = load_dataset(input_path)
    logging.info("Rows loaded: %s", len(dataframe))

    examples = [row_to_example(row) for _, row in dataframe.iterrows()]
    train_examples, test_examples = train_test_split(
        examples,
        test_size=test_size,
        random_state=42,
        shuffle=True,
    )
    sample_examples = examples[:sample_size]

    output_dir.mkdir(parents=True, exist_ok=True)
    train_path = output_dir / "train.jsonl"
    test_path = output_dir / "test.jsonl"
    sample_path = output_dir / "sample.jsonl"

    write_jsonl(train_examples, train_path)
    write_jsonl(test_examples, test_path)
    write_jsonl(sample_examples, sample_path)

    logging.info("Train split size: %s", len(train_examples))
    logging.info("Test split size: %s", len(test_examples))
    logging.info("Wrote train file: %s", train_path)
    logging.info("Wrote test file: %s", test_path)
    logging.info("Wrote sample file: %s", sample_path)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    try:
        prepare_dataset(
            input_path=Path(args.input),
            output_dir=Path(args.output_dir),
            test_size=args.test_size,
            sample_size=args.sample_size,
        )
    except Exception as error:
        raise SystemExit(f"ERROR: {error}") from error


if __name__ == "__main__":
    main()
