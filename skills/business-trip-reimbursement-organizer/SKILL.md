---
name: business-trip-reimbursement-organizer
description: Organize, rename, audit, and reconcile business-trip reimbursement materials such as approvals, rail or air tickets, hotel invoices, insurance, and payment evidence. Use when files must be grouped by trip, checked for completeness, or independently totaled; do not use for accounting policy advice unrelated to the supplied materials.
---

# Business Trip Reimbursement Organizer

Organize reimbursement evidence into traceable trip folders and prove that claimed totals match the source documents.

Before classifying files, naming them, or declaring a trip complete, read [references/default-rules-and-naming.md](references/default-rules-and-naming.md). Apply its defaults only after honoring explicit user requirements and any designated reference directory.

## Workflow

1. Resolve the actual directory with read-only checks. If the supplied path is absent, inspect only nearby plausible directories and report the resolved path; do not create a substitute path.
2. Inventory recursively before changing anything. On Windows, prefer `scripts/inventory-reimbursement.ps1`; elsewhere collect equivalent relative paths, types, sizes, modification times, and hashes.
3. Inspect document contents rather than trusting filenames:
   - Extract PDF text for dates, routes, invoice totals, ticket prices, refund fees, order numbers, policy numbers, and hotel stay dates.
   - Render PDF pages when layout or validity matters. Treat a file as invalid when it is not a real readable PDF even if its extension is `.pdf`.
   - Visually inspect images for visible dates, routes, merchants, paid amounts, and refunds.
4. Build an evidence table keyed by trip and expense. Link related files with travel dates, routes, order numbers, policy numbers, amounts, and traveler identity. Do not guess across conflicting evidence.
5. Apply the effective completeness rules and naming patterns from the reference. Mark conditional materials, such as insurance evidence, required only when the underlying purchase exists.
6. Recalculate each trip from primary expense evidence. Use payment records as corroboration, not as an additional expense. Compare the independent total with `金额计算.txt` and the folder suffix.
7. Before mutation, preflight every exact source and destination, collision, duplicate hash, and resolved target path. Moving or renaming requires the user's task authorization and any environment permission required at execution time.
8. Preserve source content. Do not delete originals by default. Isolate byte-identical duplicates under `_重复文件` and corrupt, expired, or unusable files under `_异常文件`; exclude both areas from completeness and amount calculations unless the user explicitly says otherwise.
9. After organization, inventory again, confirm the root has no loose files, verify counts and hashes, re-open or render moved PDFs, and recompute all totals.

## Amount Reconciliation

- Prefer invoice `价税合计`, railway `票价`, or invoiced `退票费` as primary amounts.
- Do not count invoices, payment screenshots, order pages, policies, and boarding passes as separate expenses when they document the same purchase.
- If an airline invoice already contains a change or refund fee, do not add the same fee again from a screenshot.
- For payment and refund evidence, verify `支付 - 退款 = 对应发票合计`, explaining any service item excluded from reimbursement.
- Require hotel payment evidence to equal the hotel invoice total under the default rules.
- Show the arithmetic for every trip and the grand total. Report a numeric difference even when it is zero.

## Completion Report

For each trip, report:

- completeness status and missing or conflicting evidence;
- expense categories and explicit arithmetic;
- calculated total, recorded total, and difference;
- duplicates or abnormal files excluded from the result.

Lead with whether the materials are complete and whether all amounts reconcile. Never claim completion based only on filenames or folder totals.
