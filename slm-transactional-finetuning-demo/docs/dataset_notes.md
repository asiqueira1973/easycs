# Dataset Notes

## Original dataset columns

The raw loan approval CSV is expected to contain these columns:

| Column | Description |
| --- | --- |
| `loan_id` | Unique loan application identifier. |
| `no_of_dependents` | Number of applicant dependents. |
| `education` | Applicant education category. |
| `self_employed` | Whether the applicant is self-employed. |
| `income_annum` | Applicant annual income. |
| `loan_amount` | Requested loan amount. |
| `loan_term` | Requested loan term in months. |
| `cibil_score` | Applicant CIBIL credit score. |
| `residential_assets_value` | Value of residential assets. |
| `commercial_assets_value` | Value of commercial assets. |
| `luxury_assets_value` | Value of luxury assets. |
| `bank_asset_value` | Value of bank assets. |
| `loan_status` | Historical business decision. |

## Target column

The target column is `loan_status`. It represents the historical decision made by the lending process and should contain `Approved` or `Rejected`.

The preparation script maps this field to the generated output decision:

- `Approved` becomes `Decision: approve`
- `Rejected` becomes `Decision: reject`

The script does not override the historical decision. Rule-based logic is used only to create deterministic reason, recommended action, and customer message text.

## Input fields

The generated `input` field summarizes these transaction attributes in natural language:

- Number of dependents
- Education
- Self-employment status
- Annual income
- Requested loan amount
- Loan term
- CIBIL score
- Residential assets value
- Commercial assets value
- Luxury assets value
- Bank asset value

The `loan_id` is validated but not included in the natural language input because it is an identifier and does not describe the applicant's financial profile.

## Output format

Each JSONL record contains three top-level fields:

```json
{
  "instruction": "...",
  "input": "...",
  "output": "..."
}
```

The `output` value is a structured text block, not nested JSON:

```text
Decision: approve
Reason: The applicant has a strong credit profile, compatible income, and relevant asset values.
Recommended action: Proceed with loan approval.
Customer message: Your loan application was approved based on the analysis of your financial profile and credit history.
```

## Limitations

This public dataset is useful for demonstration, but it has limitations:

- It may not represent a real company's complete credit policy.
- It may omit important underwriting variables.
- It may include simplified or synthetic patterns.
- It should not be used for real credit decisions.
- It does not address fairness, compliance, adverse action notices, or regulated lending requirements.

For a production project, the dataset preparation process would need stronger governance, privacy review, compliance review, feature documentation, bias testing, and approval from business stakeholders.
