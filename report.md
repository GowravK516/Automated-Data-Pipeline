# Automated ETL Data Quality Report
* **Execution Timestamp (UTC):** `2026-11-02 11:12:20`
* **Pipeline Status:** `SUCCESS`

## Pipeline Metrics Summary
* **Raw Ingested Records:** `5350`
* **Cleaned & Processed Records:** `4650`
* **Records Dropped (Duplicates/Nulls/Errors):** `700`
* **Total Billed Revenue (INR):** `₹41,338,156.85`
* **Enterprise Tier Customers:** `2040` transactions

## Automated Transformation Verification
1. **Deduplication:** Removed redundant transaction IDs.
2. **Missing Value Imputation:** Filled missing transaction amounts using user-level median spending.
3. **Financial Feature Engineering:** Automatically computed 18% GST and categorized users into `Enterprise`, `Premiere`, and `Standard` tiers.
