# Project Deliverable 2: One-shot Prompt

**Course:** DSO 576  
**Product:** CPG Global Entry Strategy Decision Platform — Yunnan Coffee  
**Team repository:** [betakappa123/cpg-global-entry-strategy](https://github.com/betakappa123/cpg-global-entry-strategy)

---

You are the lead analytics engineer, product designer, and frontend developer working in the team repository identified above. Build the complete product specified below, run it, and verify it. Deliver working files rather than only a plan, wireframe, or code snippets. This prompt defines the product without requiring another specification, previous conversation, or proprietary report beyond the repository's bundled data. Inspect existing files and applicable repository instructions before editing. Preserve unrelated work and source data. Resolve ordinary implementation choices yourself; document material assumptions and genuine blockers.

## 1. Product purpose and decision workflow

Build a polished, responsive decision dashboard for the VP of Global Strategy / Chief Growth Officer of a mid-tier, vertically integrated specialty coffee company in Yunnan, China. The CFO, supply-chain and packaging leaders, and board are secondary users.

The anchor decision is whether to allocate the next increment of sellable coffee volume to international expansion or domestic Chinese tier 1/2 markets. If expansion is attractive, identify the destination, product format, and retail channel to investigate first. Compare Japan, South Korea, Australia, Singapore, United States, and Germany against China Domestic. Recommendations are conditional planning outputs, not proof of commercial demand or authorization to invest.

Every main component must serve one of these workflows:

| User inputs | Evidence shown | Decision supported |
|---|---|---|
| Category, geography scope, and evaluation years | Physical market size, volume CAGR, comparable market table, readiness radar, and attractiveness chart | Shortlist markets for commercial diligence |
| Destination, category, and packaging class | Packaging unit-volume history and mix, plus three SKU specification cards | Select a format for a manufacturing/export pilot |
| Destination, year, category, and proposed SKU | Nonoverlapping channel shares/volumes and a disclosed channel-fit rubric | Prioritize distributor and retail-channel interviews |
| Destination, volume, price, freight, tariff, and marketing | Landed cost, profit, margin, domestic comparison, and hurdle verdict | Renegotiate a scenario or advance it to diligence |
| Five strategic criterion weights | Normalized sub-scores, reranked markets, and roadmap tiers | Evaluate sensitivity to executive priorities |

Use English throughout the product. Explain that domestic growth alone does not establish the best allocation: price realization, costs, access, and risk also matter. Do not assume Japan must win; derive the recommendation from the specified data and model.

## 2. Delivery and technical constraints

The primary deliverable is dashboard.html at the repository root. It must open through a file:// URL and remain fully functional offline. Embed the prepared data, CSS, application JavaScript, and Chart.js library inside the final HTML. Do not use runtime fetch calls, CDNs, APIs, authentication, a database, or a required web server. Use HTML5, CSS, vanilla JavaScript, and Chart.js. A heatmap may use an accessible HTML table with colored cells instead of a plugin.

Separate reusable analysis, configuration, browser decision logic, and presentation. Provide:

- analysis.py: CSV ingestion, schema validation, hierarchy handling, reusable market/channel/packaging calculations, and chart-ready outputs.
- build_dashboard.py: deterministic generation of dashboard.html from validated data and configuration.
- A separate editable configuration file containing the planning assumptions and their provenance/status.
- Separate JavaScript source for pure financial and MCDA functions and UI controllers; embed it during the build.
- Vendored Chart.js with its version and license recorded, meaningful automated checks, and README instructions for installation, build, and verification.

Reuse the repository's existing environment and lockfile when present. Otherwise provide a pinned requirements file for Python 3.10+, pandas 2+, and xlrd 2+ only if reading the legacy XLS files. Avoid introducing a frontend framework or toolchain for this small static application. The documented build command must include python build_dashboard.py; use the repository's environment runner if applicable. Do not replace an existing lockfile unnecessarily.

Do not modify raw XLS files, invent missing observations, overwrite unrelated notebooks, or silently change validated clean inputs to make tests pass. Existing cleaning code can be reused after verification. Network access may be used during development to obtain a pinned library, but the built dashboard must not depend on it. If a dependency is unavailable, report the actual blocker rather than claiming an offline build works.

## 3. Data contract and validation

Use the bundled Euromonitor-derived files under DATA/clean/ as the analytical source of truth. Record the input branch and commit. The team's working branches may include main and Ben; locate the data-bearing checkout without discarding local changes. If clean outputs are absent but raw workbooks exist under DATA/, reuse or implement a reproducible cleaning process and retain audit outputs. If neither is available, identify the missing files as a blocker; never replace licensed source data with invented observations.

| File | Required fields and interpretation |
|---|---|
| clean_market_sizes_tidy.csv | Geography, Category, Data Type, Unit, Year, Total_Market_Volume; inspect additional fields to distinguish volume from value observations |
| clean_retail_channels_tidy.csv | Geography, Category, Outlet Type, Year, Channel_Share_Pct; shares describe the matching off-trade volume basis |
| clean_market_channels_merged.csv | Geography, Category, Outlet Type, Year, Channel_Share_Pct, Total_Market_Volume, Unit, Channel_Volume |
| clean_pack_type_tidy.csv | Geography, Category, Packaging Class, Pack Type, Year, Unit_Volume_MUnits |

Expected source workbooks are DATA/Market Sizes.xls, DATA/Retail channels.xls, DATA/Pack type.xls, and DATA/Pack Size.xls. Pack Size.xls is optional supporting context; do not add an undefined pack-size analysis.

Inspect actual schemas rather than assuming column positions. Trim headers and categorical whitespace, normalize country aliases such as South Korea and United States explicitly, and preserve a documented mapping to original names. Parse years as integers and measurements as numeric. Recognized missing tokens remain missing; unexpected text in numeric fields is a validation error. Do not convert blanks to zero.

Select one compatible physical-volume series per geography/category/year before joining channels. Coffee uses tonnes; RTD Coffee uses million litres. Retail Volume and Off-trade Volume must map to the correct category's channel denominator. Exclude retail-value rows, currencies, and incompatible units. If competing volume rows remain after filtering, stop with an actionable ambiguity error rather than averaging or summing them. Validate a many-to-one channel-to-market join and zero unmatched keys. Missing source measurements are different from unmatched join keys.

Validate required columns, unique analytical keys, nonnegative observed volumes, shares within 0–100, compatible units, and computed channel-volume consistency. Reject duplicate keys, invalid numeric tokens, and inconsistent joins with the file, key/row, field, and suggested correction. Optional missing evidence should disable the affected metric rather than crash the whole interface. A missing required input must fail the build clearly.

For the supplied snapshot, expected row counts are 792 market-size rows, 9,108 cleaned channel rows, 9,108 merged rows, and 5,830 packaging rows. The channel cleaning removed 396 redundant rows labeled Total from 9,504 melted rows. Report actual versus expected counts. Investigate discrepancies and fail the snapshot audit when unexplained; never create or discard observations merely to match a count. Duplicate analytical keys and invalid joins are always errors.

The India / RTD Coffee series is unobserved for all 11 years from 2015 through 2025. Preserve missing Total_Market_Volume and Channel_Volume, and display Not available. A missing value must never become zero growth, zero demand, or a fabricated chart point. Aggregates with no valid observations remain missing; disclose the coverage of partial aggregates.

## 4. Analytical definitions and evidence boundaries

### Market size and growth

Use physical volume for cross-country market comparisons. For selected start year a and end year b:

    CAGR = (Volume_b / Volume_a)^(1 / (b - a)) - 1

The default is 2015–2025: ten annual intervals. Use this horizon consistently across labels and charts, including the radar's growth dimension. Require b > a, a positive starting volume, and both endpoints present. A zero ending volume with a positive start gives -100%; a missing endpoint or nonpositive start gives Not available with a reason. Do not interpolate an endpoint or silently substitute another year. Include negative growth in chart ranges.

Distinguish observed and forecast years if the source provides that metadata. If it does not, state that the observation/forecast split is unspecified; do not label all rows historical or invent a cutoff. Regional growth summaries, if shown, must name their method and eligible market coverage. Do not average Coffee and RTD quantities.

### Retail channels

    Channel_Volume = Total_Market_Volume * Channel_Share_Pct / 100

Reconcile the premerged result to this calculation. Channel hierarchy matters: removing Total does not make every remaining row additive. Retail Channels, Retail Offline, and other parents can overlap with their children. Build an explicit hierarchy or mapping from the supplied outlet labels. For each distribution chart choose either a complete parent level or mutually exclusive leaf channels, never both. Reconcile chosen shares to 100% within 0.1 percentage points and explain incomplete coverage. Do not renormalize unexplained gaps. Display available parent/child detail as a drilldown or indented table without adding them twice.

### Packaging

Filter geography, category, year, and one Packaging Class before calculating:

    Format_share_pct = Format_unit_volume / sum(nonoverlapping format unit volumes) * 100

Exclude Total Packaging and overlapping parent rows from the denominator. Reconcile against the corresponding total where available. Use million units for packaging, never tonnes or litres. Keep missing values as gaps; a zero denominator produces Not available. A packaging sales mix is evidence about formats, not proof that consumers prefer a proposed Yunnan SKU.

### Supplementary metrics

Do not fabricate population, brand shares, specialty prices, FX rates, or a monetary TAM. If the repository supplies these with a clear source and reference year, implement the following; otherwise show a concise unavailable state and the missing evidence:

- Per-capita Coffee consumption = tonnes * 1,000 / population, in kg/person/year. RTD = million litres * 1,000,000 / population, in litres/person/year. Require matching country/year population.
- Monetary TAM requires compatible category/year/value basis, correct local-currency scaling, and a documented same-year FX rate. It is category retail market size, not the company's obtainable revenue. Never add unconverted JPY billion to CNY million or EUR million.
- Competition HHI = sum of squared firm percentage shares, range 0–10,000, for a defined country/category/year with complete compatible coverage. Aggregate brands under common ownership first. If only brand shares are available, label their squared-share sum a brand concentration proxy rather than firm HHI. Do not treat a pooled Other bucket as one firm or derive brand concentration from channel shares. With incomplete evidence, show a partial concentration measure with its limitation or mark HHI unavailable.
- An observed specialty retail price must have a defensible source and unit. Category retail value divided by total volume is a category average, not a specialty price; a wholesale planning price is not a retail price.

The original example headlines $15.5B TAM, 12.5% domestic margin, +9.3% margin spread, and MCDA scores 86.4/86.0 are not acceptance targets. Compute actual outputs; do not reverse-engineer data or sub-scores to reproduce them.

## 5. Explicit planning configuration

Keep dataset measurements, calculated metrics, and planning assumptions visibly distinct. The following are illustrative defaults supplied by this prompt to make scenarios reproducible. They are not verified current tariffs, transit commitments, consumer research, or sales forecasts. Mark them Scenario assumption in the interface and configuration. Use country and product applicability notes, and never describe a zero-duty preset as a guaranteed RCEP entitlement.

All export scenarios initially use 50 metric tonnes of finished, sellable roasted coffee per year. Costs are already per finished kg; do not apply an invented green-to-roasted conversion. The following table defines the six overseas presets:

| Destination | Wholesale invoice USD/kg | Freight + insurance USD/kg | Scenario tariff % | Annual marketing USD | Transit days | Planner-assigned origin affinity /100 |
|---|---:|---:|---:|---:|---:|---:|
| Japan | 26.00 | 0.80 | 0 | 60,000 | 5 | 85 |
| South Korea | 26.00 | 0.70 | 0 | 60,000 | 4 | 85 |
| Australia | 28.00 | 1.20 | 0 | 80,000 | 12 | 75 |
| Singapore | 25.00 | 0.60 | 0 | 50,000 | 5 | 80 |
| United States | 28.00 | 2.20 | 25 | 100,000 | 28 | 65 |
| Germany | 27.00 | 2.00 | 5 | 100,000 | 30 | 60 |

China Domestic uses the domestic financial model below, a scenario tariff of zero, a planning transit time of 2 days, and a planner-assigned affinity of 75. These affinity scores are subjective inputs, not measured consumer sentiment. Store source/status/rationale alongside configuration entries; mark externally unverified seeds accordingly.

For channel fit, use the following transparent initial planning rubric if no documented team-approved scoring evidence exists. It is SKU/channel fit scoped to the selected destination, not an empirical country ranking:

| Proposed format | Specialty boutiques | Premium supermarkets | Convenience chains | Cross-border e-commerce |
|---|---:|---:|---:|---:|
| Specialty whole bean | 5 | 4 | 2 | 5 |
| Nitrogen-flushed drip bags | 4 | 4 | 4 | 5 |
| RTD cold brew cans | 3 | 4 | 5 | 2 |

Explain the 1–5 ordinal scale and qualitative rationale: boutique specialty fit, listing/distributor costs, grab-and-go suitability, shipping weight, and cold-chain requirements where applicable. Do not invent destination-specific differences or a numerical conversion from channel share to suitability. Source sales channels and rubric channels may differ; show any mapping explicitly.

## 6. Financial model and exclusive verdict rules

This is a simplified annual contribution-style operating scenario for finished Coffee only. Keep the user-facing label Modeled operating profit/margin and disclose excluded corporate overhead, capex, financing, income tax, FX changes, working-capital timing, and unmodeled distributor/listing costs. It is not audited net income or a complete investment valuation. RTD remains available for market, packaging, and channel exploration; do not apply roasted-coffee USD/kg economics to RTD litres or cans.

Use Wholesale invoice price (USD/kg), not a misleading FOB accounting label. The scenario assumes the modeled seller bears the specified freight, duties, and marketing. Duties use invoice revenue as a simplified base; actual customs valuation and Incoterms require separate diligence.

Provide synchronized range sliders and numeric inputs:

| Input | Minimum | Maximum | Step | Japan default |
|---|---:|---:|---:|---:|
| Annual finished export volume, metric tonnes | 10 | 300 | 1 | 50 |
| Wholesale invoice price, USD/kg | 15 | 50 | 0.50 | 26 |
| Freight and insurance, USD/kg | 0.30 | 3.50 | 0.10 | 0.80 |
| Tariff rate, % | 0 | 35 | 0.50 | 0 |
| Annual destination marketing, USD | 10,000 | 250,000 | 5,000 | 60,000 |

Use these equations without rounding intermediate values:

    Q = volume_metric_tonnes * 1,000
    revenue = Q * price
    sourcing = Q * 7.50
    processing_roasting_packaging = Q * 4.00
    production_cost = sourcing + processing_roasting_packaging
    freight_cost = Q * freight_per_kg
    duties = revenue * tariff_pct / 100
    landed_COGS = production_cost + freight_cost + duties
    total_modeled_cost = landed_COGS + marketing_budget
    export_profit = revenue - total_modeled_cost
    export_margin_pct = 100 * export_profit / revenue

    domestic_revenue = Q * 16.50
    domestic_cost = Q * 12.00 + 30,000
    domestic_profit = domestic_revenue - domestic_cost
    domestic_margin_pct = 100 * domestic_profit / domestic_revenue
    profit_delta = export_profit - domestic_profit
    margin_spread_pp = export_margin_pct - domestic_margin_pct

Domestic profit and margin change with volume; they are not fixed at 12.5%. Display a margin difference in percentage points, not as a relative percentage increase. Preserve negative profit and negative margins.

Apply the following ordered rules, producing exactly one verdict:

1. MARGIN DILUTIVE / HOLD if export_profit <= 0, profit_delta <= 0, or export_margin_pct < 10.
2. Otherwise ACCRETIVE OVERSEAS EXPANSION if export_margin_pct >= 18 and margin_spread_pp >= 5.
3. Otherwise CONDITIONAL / FEASIBLE. Explain the unmet hurdle, including a spread below +5 pp or margin below 18%.

Show the selected destination and triggering values in the verdict. A positive modeled profit alone does not qualify as accretive. Display dollars and margins from unrounded calculations. A per-kg economics chart must use this same wholesale basis, including marketing/Q. Do not subtract a second 28% distributor margin. Domestic per-kg cost is 12.00 plus 30,000/Q; do not invent a sourcing/processing split for that 12.00.

## 7. Reproducible MCDA and roadmap

MCDA and its radar are a Coffee-only strategic screening model using the fixed 2015–2025 horizon and the seven focal markets. Explain this scope when RTD exploration is selected. Use actual volume CAGR and the planning presets above, with a common 50-tonne volume for financial comparability. Simulator edits are an independent scenario and do not silently change MCDA attributes. Weights change ranking; changing destination presets requires editing the disclosed configuration and rebuilding.

Let clip(x) limit a value to [0,100]. Calculate:

    growth_score = clip(100 * CAGR_percentage / 15)
    margin_score = clip(100 * preset_modeled_margin_pct / 50)
    tariff_score = clip(100 * (1 - preset_tariff_pct / 35))
    logistics_score = clip(100 * (32 - preset_transit_days) / 30)
    affinity_score = planner_assigned_affinity
    composite = sum(score_j * weight_j) / sum(weight_j)

These are disclosed planning anchors, not industry standards: 15% CAGR, 50% modeled margin, 0–35% tariffs, and 2–32 days transit. Use the domestic model for China's margin score. Show raw metrics, normalized scores, and the normalization method. If a required criterion is missing, mark the country Insufficient data and leave it unranked; do not silently impute zero or redistribute weights across missing criteria.

Use five weight sliders from 5 to 50, step 1. Defaults: growth 25, margin 30, tariff/trade ease 20, logistics 15, affinity 10. Display both raw weights and their effective normalized percentages. Normalize mathematically by the current sum; do not force the sliders themselves to total 100. Reset restores these five values. The pure scoring function must support nonnegative test weights outside slider bounds and reject an all-zero weight vector.

Rank eligible markets by unrounded composite descending; break exact ties alphabetically by canonical country name. Show one decimal only for display. Include China in the numerical ranking but always assign its roadmap label BASE: MAINTAIN & DEFEND.

For each overseas market, use its preset financial verdict with these rules: HOLD if its financial verdict is HOLD; otherwise PHASE 1: PRIORITY ENTRY for composite >=80 with an accretive financial verdict; otherwise PHASE 2: CONDITIONAL ENTRY for composite >=65; otherwise PILOT: TEST BED for composite >=50; otherwise PHASE 3 / HOLD. Missing required data gives INSUFFICIENT DATA. These are screening labels, not investment approval. Never hard-code the winners or force the example scores from an earlier vision document.

## 8. Interface, views, and interaction contract

Create a premium specialty-coffee visual system: espresso backgrounds #0c0a09 and #141210; card surfaces rgba(26,22,19,0.85); subtle bronze borders; crema #d4a373, gold #e9c46a, copper #c27847, green #52b788, red #e76f51, and slate #457b9d. Use Outfit headings and Inter body text only if the font files can be bundled locally; otherwise use readable system sans-serif fallbacks. Use generous spacing, legible contrast, a 1440px maximum content width, a sticky header, and persistent six-tab navigation.

Default to Executive Scorecard, Japan's financial preset, Coffee, and 2015–2025. Provide the following views:

1. **Executive Scorecard:** Title Yunnan Coffee Global Entry; a brief decision statement; an evidence-dependent status banner; four KPI cards for selected-scenario margin spread, current top-ranked overseas target, combined Japan/South Korea endpoint physical market size, and selected scenario tariff. Label the volume card's category, year, unit, and full-category scope; show monetary TAM only with valid monetary evidence. Include the shared five-axis readiness radar for China, Japan, South Korea, and United States; a per-kg unit-economics comparison for China, Japan, South Korea, Australia, and United States; and the seven-market evaluation table. All figures and status messages must come from the relevant model or data, with scenario/screening scope visible. Give a clear next action such as investigate a pilot, revise terms, or hold, including the key condition.
2. **Market Attractiveness:** Category, region, start-year, and end-year controls; a cross-market growth/volume table; an attractiveness bubble chart; per-capita and concentration panels; and concise takeaways tied to current evidence. The preferred bubble view uses CAGR on x, sourced category-compatible specialty retail price on y (USD/kg for Coffee; USD/litre for RTD), and endpoint category volume as bubble area. It is a two-axis chart encoding three variables. Scale radius with the square root of volume, compare one category/unit at a time, and use nonclipping axes. If compatible specialty prices are absent, show an explanatory notice and a useful fallback scatter of CAGR versus endpoint physical market volume; do not substitute wholesale assumptions while labeling them observed retail prices. HHI and per-capita panels have honest unavailable states when evidence is absent.
3. **Product-Market Fit & Channels:** Destination, category, endpoint-year, packaging-class, and proposed-format controls. Show packaging volume history and mix; nonoverlapping channel share and physical-volume views; a matching source table; the channel-fit heatmap; and three SKU cards. Whole bean: proposed 250g valve pouch, SCA 84+ quality target, specialty brewing occasion. Drip bags: proposed 10g nitrogen-flushed filter pouch, 10-pack carton, office/home premium convenience occasion. RTD: proposed 250ml slim aluminium can and grab-and-go occasion, with process/shelf-life validation required. Treat quality, shelf life, certification, and gross-margin targets as design hypotheses unless supported by actual evidence. Discuss Yunnan origin and cultivation/processing options without asserting every lot has a particular variety, score, or certification.
4. **Financial Simulator:** Destination selector, all five paired inputs, reset-selected-destination button, live input labels, cost breakdown, revenue/profit/margin cards, same-volume domestic comparison, signed profit delta and margin spread, two-bar profit chart, and exclusive verdict box. Both bars share a dollar scale with a visible zero line and support losses. Use green when export profit exceeds domestic and red when it is lower; also identify the difference with text.
5. **MCDA Decision Matrix:** Five sliders, reset button, current effective weights, ranked table, exposed raw metrics/sub-scores, normalization explanation, and roadmap labels. Update immediately with no reload. Include a plain-language note that rankings combine measured growth with illustrative economic and affinity assumptions.
6. **Risks & Objections:** Cards for domestic price competition, Yunnan origin credibility, trade-policy uncertainty, FX exposure, freshness/transit risk, channel fees, data limitations, and capex/working-capital gaps. Each gives the objection, available evidence versus assumption, mitigation, responsible business role, and validation gate. Include a conditional compliance roadmap covering product classification, origin/preferential documentation, food/import labeling, phytosanitary applicability, organic claims/JAS where applicable, and EUDR traceability where applicable. State each item's destination/product scope, verification status, and milestone before contracting or shipping. Do not label every item universally mandatory or assert current legal deadlines without an authoritative dated source.

Interaction scope must be explicit:

- Market exploration controls in tab 2 and category/year controls in tab 3 share category and endpoint-year state; changes update both views and the scorecard's physical-market table/volume card. The start year controls market CAGR. MCDA remains on its clearly labeled fixed Coffee horizon.
- Coffee allows whole bean or drip bags as the proposed format; RTD Coffee allows cold brew cans. Switching category selects its compatible default format (whole bean for Coffee, cans for RTD). Keep all three SKU cards visible for context, but base the active channel-fit interpretation on the compatible selected format and category.
- Global Focal Markets means the seven focal countries. Asia Pacific means China, Japan, South Korea, Australia, Singapore, and India where present. India may appear in exploration but does not enter the seven-country MCDA. Populate year and packaging-class options from available data; show missing selected endpoints rather than fabricating them.
- Selecting an overseas market in a table or tab 3 synchronizes the simulator destination. Switching destination resets price, freight, tariff, and marketing to that destination's preset, preserves annual volume, and announces the reset. A destination reset button restores its full preset including 50-tonne volume. China is a comparator, not an overseas destination; selecting China in exploration does not replace the export destination.
- Every simulator input updates its numeric partner, cards, cost chart, profit chart, scorecard selected-scenario figures, and financial verdict from one calculated result object. It does not alter source market data or MCDA weights.
- MCDA weight changes update the ranking table, scorecard top-target card, and screening summary. Radar values remain the same unweighted criterion sub-scores; weights change their contribution to the composite, not the underlying attributes. Show a separate financial verdict and MCDA roadmap status so differing scopes are understandable.
- Switching tabs preserves state and resizes the relevant Chart.js instances after the panel becomes visible. Avoid duplicate chart instances and event handlers. Reset MCDA affects only MCDA weights; reset scenario affects only the selected scenario.

Every chart needs an informative title, unit-bearing axes, useful tooltips, and a caption stating the decision question. Provide nearby accessible data tables or equivalent text summaries. Format currency consistently, volumes with their units, missing values as Not available, and actual zeros as zero. Sources/methodology and assumption disclosures must remain accessible in the offline file. Links to repository documents are optional convenience links, never the sole explanation of a metric.

Support 375px phone, 768px tablet, 1280px laptop, and 1920px desktop widths. Stack cards and charts on small screens. Wide tables may scroll within their own labeled containers; the window must not overflow horizontally. Use semantic landmarks, a single h1, associated labels, visible focus states, keyboard-operable sliders/number inputs, and accessible tabs with roles, aria-selected, aria-controls, arrow keys, Home/End, and predictable focus. Do not rely on flags, hover, or color alone. Respect reduced-motion preferences and avoid excessive live announcements during slider dragging.

## 9. Build sequence and acceptance checks

First inspect and audit the input files. Then implement reusable data calculations and planning configuration, followed by pure financial/MCDA functions, the HTML shell, charts, interactions, and responsive/accessibility refinements. Run the build and test the actual generated file. Fix discrepancies before reporting completion.

Include meaningful automated checks for the following and record observed results:

1. **Data integrity:** Snapshot counts are audited; analytical keys are unique; channel joins are many-to-one with zero unmatched keys; volumes and units are compatible. India RTD has all 11 expected missing market values and missing channel volumes. Missing-only aggregates stay missing.
2. **Hand calculation:** China / Coffee / Supermarkets / 2025 has source volume 61,314.5 tonnes and share 20.5%, yielding 12,569.4725 tonnes within 0.01. Inspect the matching source record; report a changed-snapshot discrepancy rather than replacing its value.
3. **Hierarchy correctness:** One selected market/category/year distribution reconciles to 100% within 0.1 percentage points with no parent/child double counting. Packaging shares use one class and exclude totals. Tests exercise at least one nested channel example.
4. **CAGR boundaries:** Ten-year growth uses ten intervals; a synthetic 100-to-200 series over ten years gives approximately 7.17735%. Missing endpoints return missing, positive-to-zero returns -100%, and a zero starting value is explicitly unavailable. Temporary fixtures must not modify bundled data.
5. **Japan financial default:** 50 tonnes, price 26.00, freight 0.80, tariff 0%, marketing 60,000 produce revenue 1,300,000; production cost 575,000; freight 40,000; duties zero; landed COGS 615,000; total modeled cost 675,000; export profit 625,000; export margin 48.076923%; domestic profit 195,000; domestic margin 23.636364%; profit delta +430,000; and margin spread +24.440559 pp. Verdict: ACCRETIVE OVERSEAS EXPANSION. Dollars match within $0.01 and margins within 0.01 pp before display rounding.
6. **United States downside fixture:** 50 tonnes, price 22.00, freight 2.50, tariff 25%, marketing 100,000 produce revenue 1,100,000; duties 275,000; landed COGS 975,000; total modeled cost 1,075,000; profit 25,000; margin 2.272727%; and profit delta -170,000. Verdict: MARGIN DILUTIVE / HOLD. This fixture is intentionally different from the United States preset.
7. **Verdict boundaries:** Test equality at zero profit delta, 10% margin, 18% margin, and +5 pp spread. Test a profitable export case with negative profit delta. Confirm exactly one verdict and that the +5 pp hurdle is enforced.
8. **Financial sensitivity:** At fixed remaining inputs, higher freight/tariff/marketing reduces export profit; increased volume recomputes both the export model and domestic fixed-cost allocation. Invalid/blank numeric input produces a clear validation state rather than NaN or stale-looking results.
9. **MCDA correctness:** Check a manually calculated score from the disclosed sub-scores. Defaults and doubled weights [50,60,40,30,20] yield identical scores within 1e-9 in the pure function; the UI remains bounded at 5–50. Test deterministic ties, missing criteria, all-zero rejection, changed rankings under changed priorities using a synthetic crossed-preference fixture, and exact restoration after reset. All eligible scores remain in [0,100], and weight changes do not alter raw radar attributes.
10. **Failure handling:** Temporary copies with a missing required column, duplicate analytical key, invalid numeric token, incompatible unit, or unmatched channel key fail with actionable diagnostics. Do not alter source data. Unsupported HHI/population/price evidence yields the designed unavailable state, not invented values.
11. **UI and offline behavior:** Open dashboard.html directly with networking disabled. Exercise all six tabs, both categories, country switching, each paired input, slider extremes, and both reset buttons. Confirm correct dependent updates, state preservation, visible loss handling, chart resizing, and no uncaught JavaScript errors or missing asset requests. Verify readability at the four specified widths and keyboard navigation. Attempt Chromium and another available browser; report which were actually tested.

Keep analysis functions pure where practical and return structured values rather than only printing. Use one financial function and one scoring function across the corresponding UI components so cards, charts, and verdicts cannot drift. Protect raw files during negative tests. Do not treat a polished screenshot or a passing build alone as proof of correct analytics.

## 10. Completion report

When finished, identify the files created/changed, the exact install/build/test commands run, where to open dashboard.html, and which acceptance checks passed. Disclose remaining unavailable evidence, illustrative presets, untested browser coverage, and actual blockers. Update README with the same reproducible build instructions and assumptions. Do not claim external verification, current regulatory compliance, source validation, or a test pass that you did not perform. The final result should let an executive trace a market shortlist through product/channel choices to a transparent financial hurdle and a sensitivity-aware screening recommendation.
