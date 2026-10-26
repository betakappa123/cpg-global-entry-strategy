# Team Change Requests

## Audit claim

| Auditor | Audited app version | Audit object | Evidence |
|---|---|---|---|
| Ralph Jiang | Primary reference: current `BUILD_SPEC.md`; supporting app: `Ben`, commit `0863abd521abd29b1199e5e6f0f69b5813f7acc1` | Financial Simulator verdict for export versus same-volume domestic deployment | Domestic benchmark recalculation at 50 MT and three simulator cases, including two verdict counterexamples. |

The audit focuses on one feature: whether the simulator's strategic verdict correctly reflects the domestic-comparison requirements in Use Case 4 and M5. The domestic-margin calculation is included as supporting evidence for that feature, not as a separate number audit. No teammate's source was changed.

## CR-M9-RJ-01 - Unify and enforce the domestic-comparison verdict policy

- **Status:** Open; proposed change for team review.
- **Reported by:** Ralph Jiang; inspection and automated function execution assisted by AI.
- **User and decision:** VP of Global Strategy and CFO comparing export versus domestic deployment of the same coffee volume.
- **Requirement:** Use Case 4 requires an export margin advantage of at least 5.0 percentage points over the same-volume domestic alternative. M5's verdict rules overlap, and the Accretive rule does not include this 5-point hurdle.
- **Implementation checked:** `dashboard.html` from the pinned `Ben` commit; `recalculateSimulator()` calculates the profit difference and margin spread, but the verdict branches do not consistently use both. The application is JavaScript; the Python snippet in the individual audit is only an equivalent illustration.
- **Shared inputs:** Japan, 50 MT annual volume, freight and insurance $0.80/kg, 0% tariff, and annual marketing $60,000. Domestic revenue is $825,000, cost is $630,000, profit is $195,000, and margin is 23.636364% (23.6%).
- **Reproduction cases and observed verdicts:**

| Case | Export price | Export profit | Export margin | Profit vs. domestic | Margin spread | Observed verdict |
|---|---:|---:|---:|---:|---:|---|
| Baseline | $26.00/kg | $625,000 | 48.076923% | +$430,000 | +24.440559 pp | Highly Accretive |
| A: below domestic | $16.00/kg | $125,000 | 15.625000% | -$70,000 | -8.011364 pp | Conditional / Feasible |
| B: below 5-point hurdle | $18.00/kg | $225,000 | 25.000000% | +$30,000 | +1.363636 pp | Highly Accretive |

- **Finding:** Case A earns less than the domestic alternative but receives a positive Conditional / Feasible verdict. Case B exceeds domestic profit but misses the 5-point margin hurdle and still receives the strongest positive verdict.
- **Requested change:** Resolve the conflict between Use Case 4 and M5 by defining one ordered, mutually exclusive policy, then align the specification, implementation, verdict explanation, and tests. Candidate policy for team approval:
  1. Hold if export margin is below 10% or export profit does not exceed same-volume domestic profit.
  2. Label Highly Accretive only if export margin is at least 18% and the margin spread is at least 5.0 percentage points.
  3. Otherwise label Conditional and state which hurdle is unmet.
- **Acceptance criteria:** Under the approved policy, Case A must Hold, Case B must not be labeled Highly Accretive, and the baseline must continue to clear the hurdle. Add tests immediately below, at, and above each approved threshold, including a zero profit difference. Do not treat the proposed policy above as already approved.
- **Verification limits:** The automated check executes the original function from the pinned Git object and captures its outputs. It verifies the calculation and verdict function, not browser rendering, event wiring, CDN loading, or a manual end-to-end browser session.

## Reproduce the audit

With Node.js and Git installed, run from this repository:

```powershell
node audit_checks/module09_audit.mjs
```

The script uses the fixed Git commit and does not modify application code or require a branch checkout. No changes have been committed or pushed.
