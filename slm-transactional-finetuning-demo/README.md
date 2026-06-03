# SLM Transactional Fine-Tuning Demo

## Project goal

This project demonstrates how historical transactional business data can be converted into an instruction dataset for fine-tuning a Small Language Model (SLM). The first version focuses only on repository setup and dataset preparation. It does not fine-tune a model.

The demo uses historical loan applications as a proxy for business decision records. Each row describes an applicant, a loan request, and the company's historical decision. The preparation script transforms each row into a JSONL record with an `instruction`, natural language `input`, and structured text `output`.

## Dataset description

The expected raw dataset is a CSV file named `loan_approval_dataset.csv`. Each row represents one historical loan application.

Expected columns:

- `loan_id`
- `no_of_dependents`
- `education`
- `self_employed`
- `income_annum`
- `loan_amount`
- `loan_term`
- `cibil_score`
- `residential_assets_value`
- `commercial_assets_value`
- `luxury_assets_value`
- `bank_asset_value`
- `loan_status`

The target field is `loan_status`, which should contain the historical business decision: `Approved` or `Rejected`. The generated training output always follows this historical decision and never overrides it with new model logic.

## Setup instructions

From this directory, create and activate a Python environment, then install the minimum dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The only required Python packages are:

- `pandas`
- `scikit-learn`

## Place the CSV in `data/raw/`

Create the raw data directory if needed and copy the source CSV into it:

```bash
mkdir -p data/raw
cp /path/to/loan_approval_dataset.csv data/raw/loan_approval_dataset.csv
```

The default script path expects:

```text
data/raw/loan_approval_dataset.csv
```

## Run the preparation script

Use the command-line interface:

```bash
python src/prepare_dataset.py --input data/raw/loan_approval_dataset.csv --output-dir data/processed --test-size 0.2 --sample-size 20
```

The script will:

1. Read the CSV.
2. Strip whitespace from column names.
3. Validate that all required columns exist.
4. Normalize `loan_status` values by stripping spaces.
5. Convert each row into an instruction-tuning example.
6. Split examples into train and test files with a fixed random seed.
7. Write a small sample file for quick inspection.

## Generated files

The script writes these files:

- `data/processed/train.jsonl`
- `data/processed/test.jsonl`
- `data/processed/sample.jsonl`

Each JSONL line has this structure:

```json
{
  "instruction": "Analyze the loan application based on the company's historical credit decisions.",
  "input": "Applicant has 2 dependents, is Graduate, self-employed status is No, annual income is 9600000, requested loan amount is 29900000, loan term is 12 months, CIBIL score is 778, residential assets value is 2400000, commercial assets value is 17600000, luxury assets value is 22700000, and bank asset value is 8000000.",
  "output": "Decision: approve\nReason: The applicant has a strong credit profile, a high income relative to the requested loan, and relevant asset values.\nRecommended action: Proceed with loan approval.\nCustomer message: Your loan application was approved based on the analysis of your financial profile and credit history."
}
```

The `output` field is structured text rather than JSON. It contains:

- Decision
- Reason
- Recommended action
- Customer message

## Reproducibility

The train/test split uses `random_state=42`, so the generated files are deterministic when the same input CSV and command-line arguments are used.

## What this first step proves

This first setup proves that a tabular transactional decision dataset can be converted into instruction-following examples without adding fine-tuning frameworks or model infrastructure. Later steps can use the generated JSONL files for LoRA or QLoRA fine-tuning of a small open model.
