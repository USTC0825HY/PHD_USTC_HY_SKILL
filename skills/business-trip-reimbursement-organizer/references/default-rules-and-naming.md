# Default Rules and Naming

Use these as personal defaults. Effective priority is:

1. The user's explicit instructions for the current task.
2. A reference directory the user explicitly designates.
3. The defaults below.

Do not silently promote a pattern observed in one trip into a universal requirement.

## Completeness Defaults

| Category | Required evidence | Notes |
|---|---|---|
| Every trip | Approved travel form and `金额计算.txt` | Dates and traveler should agree with the trip folder. |
| High-speed rail | Railway electronic passenger-ticket invoice | No boarding or travel certificate is required by default. Count invoiced refund fees separately. |
| Air travel | Air-ticket invoice and boarding credential only | Match traveler, flight date, route, flight number, and ticket number when available. Order details and transaction records are not required. |
| Air insurance | Insurance invoice and corresponding policy | Both are required for every confirmed purchase; match policy number, insured traveler, flight, coverage dates, and premium. |
| Canceled air travel | Invoiced refund fee, when claiming that fee | No boarding credential is required for a canceled flight. Exclude refunded original fare and do not require order/payment/refund details by default. |
| Hotel | Hotel invoice and payment screenshot | Amounts must match. A hotel folio or water bill is not required by default. |

Supporting screenshots corroborate a primary invoice. Their displayed totals must not be added again.

## Insurance and Re-review

- An insurance invoice, a policy, an explicit user statement, or an identified insurance purchase in supplied evidence establishes a purchase to reconcile. Search the entire fresh inventory for the counterpart, including generically named newly supplied files; do not rely on a filename containing `保险单`.
- Invoice without policy: report missing policy. Policy without invoice: report missing insurance invoice. Unreadable/expired-link files do not satisfy either requirement. A past coverage period matching the completed trip is normal, not an invalid policy.
- Match invoice policy number and premium to the policy, then match insured traveler and flight/coverage dates to the trip. Missing identifiers or contradictory fields are unverified or mismatched evidence, not complete insurance. A generic insurance invoice filename or shared order label alone cannot prove coverage.
- Do not demand policies for flights with no established insurance purchase. State unknown status only when relevant.
- On every re-review, rescan current contents and replace stale conclusions in the report. Modify old checklists only when the user requests an authorized correction or organization task.

## Naming Patterns

- Trip directory: `YYYYMMDD_YYYYMMDD_总额元`
- Approval: `YYYYMMDD_YYYYMMDD_出差审批单.jpg`
- Rail ticket: `高铁_MMDD出发站_到达站_金额元.pdf`
- Rail refund fee: `高铁退票费_MMDD出发站_到达站_金额元.pdf`
- Air-ticket invoice: `机票_MMDD出发地_到达地.pdf`
- Insurance invoice: `保险_MMDD出发地_到达地.pdf`
- Insurance policy: `保险单_MMDD出发地_到达地.pdf`
- Boarding credential: `电子登机凭证_MMDD出发地_到达地.pdf`
- Order screenshot: `订单详情_MMDD出发地_到达地_支付金额元[_退款金额元].jpg`
- Transaction screenshot: `交易记录_MMDD出发地_到达地_支付金额元[_退款金额元].jpg`
- Hotel invoice: `酒店发票_YYYYMMDD_YYYYMMDD_金额.pdf`
- Hotel payment: `酒店付款_YYYYMMDD_YYYYMMDD_金额元.jpg`

Preserve the original extension when it matches the real format. If a supposed PDF is plain text or otherwise invalid, isolate it under `_异常文件` with a name that states the failure. Never overwrite a colliding destination without resolving whether it is an identical duplicate or a distinct document.

## Classification and Arithmetic

- Prefer service or travel dates over download, screenshot, or invoice-issuance dates when assigning a trip.
- Match air invoices and boarding credentials by traveler, flight date, route, flight number, and ticket number when available. Match insurance separately by policy number and coverage; use supplied order numbers as optional corroboration only.
- Match hotel files by stay interval, traveler, merchant, and amount.
- Use decimal arithmetic to two places; do not use binary floating-point approximations for money.
- A trip total is the sum of reimbursable primary amounts: transport invoices and invoiced fees, insurance invoices, hotel invoices, and any other explicitly allowed category.
- Compare that sum with both `金额计算.txt` and the numeric suffix of the trip directory.
- Exclude files under `_重复文件` and `_异常文件` from amount and completeness checks when a valid in-trip replacement exists.
- Independently sum each primary amount once, then category totals, trip totals, and the grand total. Report `recorded - calculated` differences for notes and folder suffixes; never assume a saved equation is correct.
- Keep invoice completeness, payment verification, and expense eligibility distinct. For example, a service-fee invoice without a route can have an uncertain trip association without making otherwise complete airfare require order details.

## Personal Calculation Defaults (Not Submission Materials)

- Apply these only when the user requests a personal receivable estimate. Distinguish all invoice expenses from personally paid expenses and confirmed payments by an agent, employer, or another payer.
- Agent booking alone does not identify the payer. Exclude costs from the personal amount only when non-personal payment is explicit; disclose unresolved attribution or ask if it materially changes the result.
- Personal allowance default: CNY 180.00 per calendar day, including both departure and return dates. Sum unique dates across the trip intervals so overlapping days are not paid twice. The user can override the rate or counting rule for an individual task.
- `个人应收金额 = 个人垫付报销费用 + 出差补贴`. Insurance policies, boarding credentials, and payment screenshots are not additional expenses.
- Show personal calculations in the conversation by default. Allowance and personal receivables must not enter submission `金额计算.txt`, trip-folder amount suffixes, or other reimbursement submission materials. Save a separate personal-calculation file only at the user's explicit request.
- During audit-only tasks, identify wrong folder or note amounts without changing them; correction/organization tasks may update those records within authorized scope.
