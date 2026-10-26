# Module 9 Individual Audit

## Audit object: Financial Simulator decision verdict

- **Name:** Ralph Jiang
- **Team app:** CPG Global Entry Strategy Decision Platform - Yunnan Coffee
- **Feature selected:** Financial Simulator's comparison of an export scenario with selling the same volume domestically, including the resulting strategic verdict.
- **Primary reference:** `BUILD_SPEC.md`, Use Case 4, Metric M5, and Acceptance Check AC-4.
- **Implementation evidence:** `dashboard.html` from local `Ben` commit `0863abd521abd29b1199e5e6f0f69b5813f7acc1`. The specification blob is identical on local `main` and `Ben`. No branch was switched and no teammate's source was changed.

### Why this is the audit object

This is a complete, decision-facing feature: a user enters scenario assumptions and receives a recommendation about where to allocate the same coffee volume. Its requirements can be checked against explicit inputs, formulas, and output verdicts. The test cases below show that the current verdict can conflict with the domestic-comparison requirement, making this a more focused and actionable audit object than auditing an isolated number claim.

## Requirement and finding

Use Case 4 requires an export scenario to exceed the same-volume domestic margin by at least **5 percentage points**. M5 defines domestic profit and margin, but its verdict rules overlap: a profitable export with at least 10% margin can be Conditional, while a nonpositive profit difference versus domestic can also be Hold. The Accretive rule does not include the 5-point hurdle.

In the audited implementation, `recalculateSimulator()` calculates the export-versus-domestic profit difference and margin spread, but its verdict branches do not consistently use both. The Python below is an equivalent illustration of the audited decision logic; the app itself is implemented in JavaScript:

```python
if net_margin >= 18 and profit_delta > 0:
    verdict = "HIGHLY ACCRETIVE EXPORT"
elif net_margin >= 10 and net_profit > 0:
    verdict = "CONDITIONAL / FEASIBLE"
else:
    verdict = "MARGIN DILUTIVE / HOLD"
```

Thus, the calculation can show a scenario that fails the domestic-comparison hurdle while the verdict still presents it as positive.

## Inputs and checked results

All cases use Japan, 50 MT annual volume, $0.80/kg freight and insurance, 0% tariff, and $60,000 annual marketing. I checked the domestic benchmark from the M5 formula:

```text
Domestic revenue = 50,000 kg * $16.50/kg = $825,000
Domestic cost = 50,000 kg * $12.00/kg + $30,000 = $630,000
Domestic profit = $195,000
Domestic margin = $195,000 / $825,000 = 23.636364% (23.6%)
```

| Case | Export price | Export profit | Export margin | Profit vs. domestic | Margin spread | Actual verdict |
|---|---:|---:|---:|---:|---:|---|
| Baseline | $26.00/kg | $625,000 | 48.076923% | +$430,000 | +24.440559 pp | Highly Accretive |
| A: below domestic | $16.00/kg | $125,000 | 15.625000% | -$70,000 | -8.011364 pp | Conditional / Feasible |
| B: below 5-point hurdle | $18.00/kg | $225,000 | 25.000000% | +$30,000 | +1.363636 pp | Highly Accretive |

The baseline clears the stated hurdle. Case A earns a profit but yields $70,000 less than the domestic alternative and is still labeled Conditional / Feasible. Case B beats domestic profit, but its margin advantage is only 1.36 percentage points; it receives the strongest positive verdict despite failing Use Case 4's 5-point requirement.

The automated check ran the original `recalculateSimulator()` function from the pinned Git object in Node.js and captured its output strings. This verifies the calculation and verdict function, not browser rendering, event wiring, CDN loading, or a manual end-to-end browser session.

## Conclusion and requested change

**Finding:** The Financial Simulator verdict is not a reliable indication that the export option meets the specified domestic-comparison hurdle.

Request `CR-M9-RJ-01`: align Use Case 4 and M5, specify one ordered and mutually exclusive verdict policy, and update the implementation and tests accordingly. A candidate policy for the team to approve is:

1. Hold if export margin is below 10% or export profit does not exceed same-volume domestic profit.
2. Label Highly Accretive only if export margin is at least 18% **and** margin spread is at least 5.0 percentage points.
3. Otherwise label Conditional and clearly state which hurdle is unmet.

This is a proposed policy, not a claim that the current specification already defines these exclusive rules.

## My contribution and AI assistance

I checked the domestic benchmark against the M5 inputs and formula: at 50 MT, domestic revenue is **$825,000**, cost is **$630,000**, profit is **$195,000**, and margin is **23.6%**. I also reviewed the three simulator cases above, focusing on whether the actual verdict agrees with the same-volume profit comparison and the 5-percentage-point requirement.

AI analysis recommends that I use the **Financial Simulator's domestic-comparison verdict** as my audit object. It is one bounded feature with a clear user decision, an explicit requirement, reproducible scenarios, and observable outputs. The 12.5% domestic-margin statement is a separate specification inconsistency; I did not select it as a second audit object.

AI assistance was used to inspect the pinned implementation, run the reproducible function check, and help organize the evidence and recommendation. The calculations and conclusions should be reviewed by me before submission. No personal manual browser test is claimed.
