# Module 9 — team audit claims and change requests

Prepared October 26, 2026 for Wendy’s branch. This records Wendy’s audit claim and findings; it does not establish team adoption of the audited build. Supplemental app/evidence files listed below are currently local, not uploaded links.

## Claims

| Student | Proposed feature | Proposed number | Version | Status |
|---|---|---|---|---|
| Wendy Sun | Financial Simulator freight-input synchronization and invalid-price handling | Japan preset annual modeled operating profit; invoice-revenue duty base | Local initial build d5c07e004037 | Student reports manual freight check and conclusions; supplemental AI checks recorded; team coordination pending |

## Scope distinction and audited version

Ralph Jiang’s [claim at commit 5a61882](https://github.com/betakappa123/cpg-global-entry-strategy/blob/5a618828b51c075ba5d936d98fc78f9db9f02d3c/change-requests.md) covers the Financial Simulator’s domestic-comparison **verdict policy**, using `Ben` commit `0863abd521abd29b1199e5e6f0f69b5813f7acc1` and `BUILD_SPEC.md`.

Wendy claims **freight input-to-output synchronization and annual modeled profit / invoice-revenue duty-base calculation**. New evidence consists of an end-to-end browser freight-change check, captured card/chart updates, a separate Python Decimal computation, a nonzero 5% duty test, and blank-input handling. Wendy personally reports the freight check and $50,000 cost calculation; Codex executed the additional automated cases. This does not claim Ralph’s verdict counterexamples as Wendy’s work.

Wendy’s audited artifact is the new local build `d5c07e004037`, generated from `ONE_SHOT_PROMPT_FINAL_DATA_VERSION.md` and four CSVs at main commit `5395858895f742e81f41f7d2e725a0874fb22598`. HTML SHA-256: `57531d80b6d4ba6d3510e6c65616b35b96757672adbaa2367da35467ab6a73af`. It is **not the Ben implementation Ralph tested**. No claim is made that Wendy’s results reproduce or resolve defects in that older version. A common team release remains to be agreed.

## WS-09-01 — Financial input updates

- Requirement: one selected scenario must update paired controls, cards, charts and exclusive verdict; blank values must not leave stale output.
- Evidence: AI automated Japan reset, freight 0.80→1.80 USD/kg, reset plus 5% tariff, and blank price. Revenue stays $1,300,000 across numeric cases; profits $625,000 / $575,000 / $560,000 agree with separately calculated expectations. Blank price removes results and displays validation. No uncaught page errors.
- Reproduction/evidence: `module9-personal-audit/check_ui.cjs`, `module9-personal-audit/evidence/ui-observations.json`, four screenshots, and `module9-personal-audit/evidence/calculation-check.json`.
- Requested change: no code repair proposed for these tested cases; retain the reproducible regression evidence. Wendy reports personally changing freight, observing profit/margin/chart updates, and verifying the $50,000 cost difference. Her conclusion is limited to this tested freight scenario, not all application behavior.
- Status: Manual freight check reported by Wendy; additional cases automated. No arithmetic correction requested for the tested freight case; team review pending.

## WS-09-02 — Profit definition and duty base

- Requirement: annual finished-Coffee scenario; duties use invoice revenue; profit deducts production, freight, duties and marketing exactly once.
- Code: `module9-build-v1/src/models.js`, financial, lines 14–18 at build d5c07e004037.
- Evidence: default profit $625,000 matches separate Python Decimal computation. Nonzero tariff 5% gives duties $65,000 and profit $560,000, verifying the specified invoice-revenue base in the tested case.
- Student recommendation: verify Japanese buyer demand, willingness to pay the assumed $26/kg invoice price, and actual logistics costs before investment. Wendy views the modeled $380,000 advantage after higher freight as a reason for further investigation, not a guaranteed outcome.
- Additional AI-proposed diligence: no arithmetic repair proposed. Before commercial use, obtain documented customs-valuation/rate advice and cost/price quotations; revise disclosed assumptions or formulas only if that evidence requires it. This is a proposed diligence task, not proof of a code bug or a current legal requirement.
- Proposed responsible roles: finance lead and trade specialist; no assignment has been sent.
- Limitation: no independent verification of current commercial/legal assumptions; no tested result establishes an investment recommendation.
- Status: Automatic evidence complete; student interpretation recorded for the freight scenario and business limitations; team prioritization pending.
