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
| Air travel | Air-ticket invoice, boarding credential, order details, and transaction record | If the user supplies a different institutional rule, follow it. |
| Air insurance | Insurance invoice and policy | Required only when insurance was purchased. Match order or policy number and flight date. |
| Hotel | Hotel invoice and payment screenshot | Amounts must match. A hotel folio or water bill is not required by default. |

Supporting screenshots corroborate a primary invoice. Their displayed totals must not be added again.

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
- Match connected air files by flight date and route, then confirm with order and policy numbers.
- Match hotel files by stay interval, traveler, merchant, and amount.
- Use decimal arithmetic to two places; do not use binary floating-point approximations for money.
- A trip total is the sum of reimbursable primary amounts: transport invoices and invoiced fees, insurance invoices, hotel invoices, and any other explicitly allowed category.
- Compare that sum with both `金额计算.txt` and the numeric suffix of the trip directory.
- Exclude files under `_重复文件` and `_异常文件` from amount and completeness checks when a valid in-trip replacement exists.
