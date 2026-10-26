# Team Change Requests

## Audit claim

| Auditor | Audit reference | Implementation checked | Audit object | Evidence |
|---|---|---|---|---|
| Ralph Jiang | `ONE_SHOT_PROMPT_FINAL_DATA_VERSION.md`, Section 6 and acceptance checks 8–9 | Historical `dashboard.html` from local `Ben` commit `0863abd521abd29b1199e5e6f0f69b5813f7acc1` | Financial Simulator verdict for export versus same-volume domestic deployment | Domestic benchmark recalculation at 50 MT and three simulator cases, including two verdict mismatches. |

The intended user is the VP of Global Strategy / Chief Growth Officer of a mid-tier, vertically integrated specialty coffee company in Yunnan, China; the CFO is a secondary user. The decision is whether to allocate the next increment of sellable coffee volume to an overseas export scenario or to domestic Chinese markets, using the same volume to compare options and determine whether the export scenario clears its financial hurdles or needs revised terms. The simulator is a conditional planning tool, not proof of commercial demand or authorization to invest.

This request concerns one feature only. The domestic-margin calculation is supporting evidence for the simulator verdict, not a separate number audit. The final-data prompt defines the verdict policy clearly; the finding is that the historical implementation checked here does not match it. This audit does not claim to have tested a dashboard generated to satisfy the final-data prompt. No teammate's source was changed.

## CR-M9-RJ-01 - Align the Financial Simulator verdict with the final-data rules

- **Status:** Open; implementation alignment requested.
- **Reported by:** Ralph Jiang; inspection and automated function execution assisted by AI.
- **Requirement:** `ONE_SHOT_PROMPT_FINAL_DATA_VERSION.md`, Section 6, specifies this ordered, mutually exclusive policy:
  1. **MARGIN DILUTIVE / HOLD** if export profit <= 0, profit delta <= 0, or export margin < 10%.
  2. Otherwise, **ACCRETIVE OVERSEAS EXPANSION** only if export margin >= 18% and margin spread >= 5 pp.
  3. Otherwise, **CONDITIONAL / FEASIBLE**, with the unmet hurdle explained.
- **Historical implementation checked:** `dashboard.html` from the pinned `Ben` commit; its `recalculateSimulator()` calculates profit delta and margin spread, but its verdict branches do not consistently apply the final-data prompt's rules. The app is JavaScript. Any Python snippet in the individual audit is an equivalent illustration, not the implementation.
- **Shared inputs:** Japan, 50 MT annual volume, freight and insurance $0.80/kg, tariff 0%, and annual marketing $60,000. Domestic revenue is $825,000, cost is $630,000, profit is $195,000, and margin is 23.636364%.
- **Reproduction cases and comparison:**

| Case | Export price | Export profit | Export margin | Profit delta vs. domestic | Margin spread | Historical app verdict | Required final-prompt verdict |
|---|---:|---:|---:|---:|---:|---|---|
| Japan default | $26.00/kg | $625,000 | 48.076923% | +$430,000 | +24.440559 pp | Highly Accretive | ACCRETIVE OVERSEAS EXPANSION |
| A: underperforms domestic | $16.00/kg | $125,000 | 15.625000% | -$70,000 | -8.011364 pp | CONDITIONAL / FEASIBLE | MARGIN DILUTIVE / HOLD |
| B: misses the spread hurdle | $18.00/kg | $225,000 | 25.000000% | +$30,000 | +1.363636 pp | Highly Accretive | CONDITIONAL / FEASIBLE |

- **Finding:** Case A earns less than the same-volume domestic alternative but receives a Conditional / Feasible verdict. Case B exceeds domestic profit and the 18% export-margin threshold, but misses the 5 pp spread hurdle and receives a Highly Accretive verdict. Both contradict the final-data rules.
- **Requested change:** Update the simulator implementation, verdict text, and tests to match Section 6 exactly. Display the selected destination and triggering values, preserve exactly one verdict, and explain the unmet hurdle for Conditional / Feasible. This is implementation alignment, not a request to redefine the prompt's policy.
- **Acceptance criteria:** The Japan default matches acceptance check 8 within its stated tolerances. Case A returns MARGIN DILUTIVE / HOLD; Case B returns CONDITIONAL / FEASIBLE; the baseline returns ACCRETIVE OVERSEAS EXPANSION. Add boundary tests at zero profit delta and at the 10% margin, 18% margin, and +5 pp spread thresholds, plus tests immediately below and above them, as required by acceptance check 9.
- **Verification limits:** The automated check executes the original function from the pinned historical Git object and captures its outputs. It does not verify a final-data dashboard's rendering, event wiring, or offline browser behavior.

## Reproduce the historical implementation check

With Node.js and Git installed, run from this repository:

```powershell
node audit_checks/module09_audit.mjs
```

The script reads the fixed Git commit and does not modify application code or require a branch checkout. No changes have been committed or pushed.
