# Module 9 Individual Audit

## Audit object: Financial Simulator verdict

- **Name:** Ralph Jiang
- **Team app:** CPG Global Entry Strategy Decision Platform - Yunnan Coffee
- **Feature audited:** Financial Simulator's modeled export-versus-domestic comparison and its exclusive strategic verdict.

## Context

- **Intended user:** VP of Global Strategy / Chief Growth Officer of a mid-tier, vertically integrated specialty coffee company in Yunnan, China; the CFO is a secondary user for this financial decision.
- **Intended decision:** Decide whether to allocate the next increment of sellable coffee volume to an overseas export scenario or to domestic Chinese markets. For this audit, the user compares export and domestic deployment of the same volume, then decides whether the export scenario clears the financial hurdles or needs revised terms.
- **Decision boundary:** The simulator provides a conditional planning scenario, not proof of commercial demand or authorization to invest.

### Why I selected this feature

The simulator supports the product's central allocation decision: whether the same volume of coffee should be sold overseas or domestically, and whether an export scenario clears the stated financial hurdles. Section 6 gives explicit inputs, formulas, and mutually exclusive verdict rules, so the feature can be checked with reproducible cases and clear expected outcomes.

## Requirement and audit method

The final-data prompt defines a contribution-style operating scenario for finished Coffee. For each scenario it calculates export profit and margin, domestic profit and margin at the same volume, profit delta, and margin spread in percentage points. It then requires exactly one verdict, in this order:

1. **MARGIN DILUTIVE / HOLD** if export profit is nonpositive, profit delta is nonpositive, or export margin is below 10%.
2. Otherwise, **ACCRETIVE OVERSEAS EXPANSION** only if export margin is at least 18% and margin spread is at least 5 pp.
3. Otherwise, **CONDITIONAL / FEASIBLE**, with the unmet hurdle explained.

I used the prompt's Japan default scenario and two price variations. The figures below were checked against the specified equations. The historical implementation's verdict strings were captured by the automated check that executes its original `recalculateSimulator()` function. The final-data prompt specifies the expected outcomes shown here; it does not establish that the historical implementation meets them.

## Inputs and results

All cases use Japan, 50 metric tonnes, $0.80/kg freight and insurance, 0% tariff, and $60,000 annual marketing. The domestic benchmark uses the prompt's $16.50/kg domestic selling price, $12.00/kg domestic cost, and $30,000 annual marketing:

```text
Q = 50 * 1,000 = 50,000 kg
Domestic revenue = 50,000 * $16.50 = $825,000
Domestic cost = 50,000 * $12.00 + $30,000 = $630,000
Domestic profit = $195,000
Domestic margin = $195,000 / $825,000 * 100 = 23.636364%
```

| Case | Export price | Export profit | Export margin | Profit delta vs. domestic | Margin spread | Historical app verdict | Final-prompt verdict |
|---|---:|---:|---:|---:|---:|---|---|
| Japan default | $26.00/kg | $625,000 | 48.076923% | +$430,000 | +24.440559 pp | Highly Accretive | ACCRETIVE OVERSEAS EXPANSION |
| A: underperforms domestic | $16.00/kg | $125,000 | 15.625000% | -$70,000 | -8.011364 pp | CONDITIONAL / FEASIBLE | MARGIN DILUTIVE / HOLD |
| B: misses the spread hurdle | $18.00/kg | $225,000 | 25.000000% | +$30,000 | +1.363636 pp | Highly Accretive | CONDITIONAL / FEASIBLE |

The default scenario clears all stated hurdles. Case A makes an export profit but earns $70,000 less than the same-volume domestic alternative, so the final prompt requires Hold. Case B is more profitable than domestic and exceeds the 18% export-margin threshold, but its spread is below 5 pp, so it must be Conditional rather than Accretive.

## Finding and recommendation

**Finding:** The historical implementation's verdict logic does not match the exclusive rules in the final-data prompt. It labels Case A Conditional despite a negative profit delta, and labels Case B Highly Accretive despite a margin spread of only 1.36 pp. These are implementation mismatches against the prompt, not conflicts within the final-data prompt's verdict rules.

The expected outcomes are also consistent with prompt acceptance check 9: scenarios with zero or negative profit delta must Hold, and the 10%, 18%, and +5 pp boundaries should be tested explicitly. The final-data prompt further requires the Japan default outputs listed in acceptance check 8. I recommend verifying the implementation against those exact rules and boundary cases when auditing the final-data build.

## My contribution and AI assistance

I checked the domestic benchmark against the specified inputs and formula: at 50 MT, domestic revenue is **$825,000**, cost is **$630,000**, profit is **$195,000**, and margin is **23.636364%**. I also reviewed the default and two price-variation cases to compare the historical app verdicts with the final-data prompt's required verdicts.

AI analysis recommends the **Financial Simulator's export-versus-domestic verdict** as my audit object. It is a focused, decision-facing feature with explicit formulas, ordered rules, and reproducible acceptance cases. The final-data prompt's verdict policy is clear, so the issue identified here is the historical implementation's mismatch with that policy, not an ambiguity in the prompt.

AI assistance was used to inspect the historical implementation, run the original-function check, and help organize the calculations and findings. I reviewed the evidence and conclusions for this audit. No manual browser test of a final-data dashboard is claimed.
