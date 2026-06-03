# Experiment Design

## Hypothesis

Historical transactional business records can be transformed into a useful instruction dataset for fine-tuning a Small Language Model. If each transaction includes input attributes and a historical decision, the record can be rewritten as an instruction, a natural language case summary, and a structured response that reflects the historical decision.

## Business scenario

A lending company has historical loan applications. Each application includes applicant details, loan request details, credit score information, asset values, and the final business decision. The business wants to explore whether these historical decisions can be represented as instruction-following examples for a domain-specific assistant.

The assistant is not meant to replace credit policy or underwriting controls. In this demo, the assistant learns how to express historical decisions in a consistent format:

- decision
- reason
- recommended_action
- customer_message

## Why loan approval is a good proxy

Loan approval data is a practical proxy for historical transactional decision data because it has the same structure as many business workflows:

1. A transaction or request is submitted.
2. The record contains measurable attributes.
3. A business decision is made.
4. The decision can be explained in operational language.

This pattern also appears in insurance claims, customer support routing, fraud review, procurement approvals, account risk reviews, and eligibility checks.

## What this first step proves

This first step proves that a tabular dataset can be converted into a reproducible instruction-tuning format. It demonstrates the preparation layer only:

- Read a raw CSV.
- Validate expected fields.
- Normalize the target decision field.
- Generate natural language input summaries.
- Generate deterministic structured outputs.
- Split records into train and test JSONL files.

The historical decision always comes from `loan_status`. The deterministic rules only generate the supporting text fields and do not change the decision.

## What comes next

The next phase will use the generated JSONL files to fine-tune a small open model. A likely approach is parameter-efficient fine-tuning with LoRA or QLoRA so the demo can run with modest compute resources.

Future work may include:

- Selecting a small open model.
- Formatting the JSONL records for the selected training library.
- Running LoRA or QLoRA fine-tuning.
- Evaluating generated decisions and explanations against held-out records.
- Comparing baseline model responses with fine-tuned model responses.
- Adding safeguards that separate historical decision emulation from real credit decisioning.
