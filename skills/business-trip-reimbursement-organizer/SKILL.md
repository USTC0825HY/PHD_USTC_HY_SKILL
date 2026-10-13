---
name: business-trip-reimbursement-organizer
description: Organize, rename, audit, and reconcile business-trip reimbursement materials such as approvals, rail or air tickets, hotel invoices, insurance, and payment evidence. Use when files must be grouped by trip, checked for completeness, or independently totaled; do not use for accounting policy advice unrelated to the supplied materials.
---

# Business Trip Reimbursement Organizer

Organize reimbursement evidence into traceable trip folders and prove that claimed totals match the source documents.

Before classifying files, naming them, or declaring a trip complete, read [references/default-rules-and-naming.md](references/default-rules-and-naming.md). Apply its defaults only after honoring explicit user requirements and any designated reference directory.

## Task Boundaries

- Audit or review requests are read-only: inspect and report discrepancies without renaming files, updating notes, or moving originals. Organization or correction requests authorize only the requested changes, subject to environment permissions.
- Keep submission-material totals separate from personal receivable calculations. Only calculate personal receivables when requested; use the reference's personal defaults and never insert allowances into reimbursement documents or folder totals.

## Workflow

1. Resolve the actual directory with read-only checks. If the supplied path is absent, inspect only nearby plausible directories and report the resolved path; do not create a substitute path.
2. Inventory recursively on every review, including newly added files. On Windows, prefer `scripts/inventory-reimbursement.ps1`; elsewhere collect equivalent relative paths, types, sizes, modification times, and hashes. Existing filenames, folder totals, and missing-item notes are records to verify, not sources of truth.
3. Inspect document contents rather than trusting filenames:
   - Extract PDF text for dates, routes, invoice totals, ticket prices, refund fees, order numbers, policy numbers, and hotel stay dates.
   - Render PDF pages when layout or validity matters. Treat a file as invalid when it is not a real readable PDF even if its extension is `.pdf`.
   - Visually inspect images for visible dates, routes, merchants, paid amounts, and refunds.
4. Build an evidence table keyed by trip and expense. Link related files with travel dates, routes, order numbers, policy numbers, amounts, and traveler identity. Do not guess across conflicting evidence.
5. Apply the effective completeness rules and naming patterns from the reference. For each confirmed insurance purchase, actively find both its invoice and matching policy across the current inventory; inspect policy number, insured traveler, flight, coverage dates, and premium. Report missing, unusable, or mismatched evidence, and do not mark insurance complete from an invoice alone. Unknown insurance purchase status is not itself a missing policy.
6. Independently recalculate item, category, trip, and grand totals from primary expense evidence using exact decimal arithmetic. Use payment records as corroboration, not as an additional expense. Compare each calculated total with `金额计算.txt` and the folder suffix, reporting actual differences even when prior notes assert zero.
7. Before mutation, preflight every exact source and destination, collision, duplicate hash, and resolved target path. Moving or renaming requires the user's task authorization and any environment permission required at execution time.
8. Preserve source content. Do not delete originals by default. Isolate byte-identical duplicates under `_重复文件` and corrupt, expired, or unusable files under `_异常文件`; exclude both areas from completeness and amount calculations unless the user explicitly says otherwise.
9. After authorized organization, inventory again, confirm the root has no loose files (or explain unresolved ones), verify counts and original hashes, re-open or render moved PDFs, and recompute all totals. For read-only audits, report updated conclusions in the response and identify stale notes without changing them.

## Amount Reconciliation

- Prefer invoice `价税合计`, railway `票价`, or invoiced `退票费` as primary amounts.
- Do not count invoices, payment screenshots, order pages, policies, and boarding passes as separate expenses when they document the same purchase.
- If an airline invoice already contains a change or refund fee, do not add the same fee again from a screenshot.
- When payment and refund evidence is supplied, verify `支付 - 退款 = 对应发票合计`, explaining any service item excluded from reimbursement. Its absence is not an airline-material deficiency under the personal defaults.
- Require hotel payment evidence to equal the hotel invoice total under the default rules.
- Show the arithmetic for every trip and the grand total. Report a numeric difference even when it is zero.

## Personal Receivable Calculation

When requested, separately calculate invoice totals, personally paid expenses, non-personally paid expenses, and allowances. Confirm payer attribution from explicit user statements or evidence; agent booking does not prove agent payment. If the payer is ambiguous, report conditional totals or ask rather than silently excluding airfare.

Read the personal calculation defaults in the reference for the allowance rate and day counting. Personal receivable equals personally paid reimbursable expenses plus allowance; state assumptions and show the arithmetic. Display this calculation in the conversation only by default. Create a separate personal calculation file only when explicitly requested, never folding it into `金额计算.txt`, trip-folder suffixes, or submission materials.

## Completion Report

For each trip, report:

- completeness status and missing or conflicting evidence;
- expense categories and explicit arithmetic;
- calculated total, recorded total, and difference;
- duplicates or abnormal files excluded from the result.

Lead with whether the materials are complete and whether all amounts reconcile. Never claim completion based only on filenames or folder totals.
