# Project Deliverable 2: One-shot Prompt

**Course:** DSO 576  
**Product:** CPG Global Entry Strategy Decision Platform — Yunnan Coffee  
**Team repository:** [betakappa123/cpg-global-entry-strategy](https://github.com/betakappa123/cpg-global-entry-strategy)  
**Required source data:** the four wide CSVs in the repository's Final Data Version/ directory. All long tables, the physical-volume subset, the market-channel merge, and validation evidence are outputs that the agent must generate. No complete data package or pre-generated analysis/validation file is required.

---

You are the lead analytics engineer, product designer, and frontend developer working in the team repository identified above. Build the complete product specified below, run it, and verify it. Deliver working files rather than only a plan, wireframe, or code snippets. This prompt and the four repository CSVs define the product without another specification, previous conversation, external data package, or validation document. The data preparation, analytical functions, and dashboard must all be implemented from these inputs. Inspect existing files and applicable repository instructions before editing. Preserve unrelated work and source data. Resolve ordinary implementation choices yourself; document material assumptions and genuine blockers.

## 1. Product purpose and decision workflow

Build a polished, responsive decision dashboard for the VP of Global Strategy / Chief Growth Officer of a mid-tier, vertically integrated specialty coffee company in Yunnan, China. The CFO, supply-chain and packaging leaders, and board are secondary users.

The anchor decision is whether to allocate the next increment of sellable coffee volume to international expansion or domestic Chinese tier 1/2 markets. If expansion is attractive, identify the destination, proposed product format, and retail channel to investigate first. Compare the observed focal markets Japan, Australia, United States, and Germany against China Domestic. Preserve South Korea and Singapore as explicit data-gap rows and optional financial scenarios, but exclude them from evidence-based market rankings because they are absent from the supplied source data. Recommendations are conditional planning outputs, not proof of commercial demand or authorization to invest.

Every main component must serve one of these workflows:

| User inputs | Evidence shown | Decision supported |
|---|---|---|
| Category, geography scope, and evaluation years | Physical market size, volume CAGR, comparable market table, readiness radar, and attractiveness chart | Shortlist markets for commercial diligence |
| Destination, category, packaging type/size, and proposed SKU | Measured packaging volumes, coverage-aware size comparisons, proposed SKU cards, and a disclosed channel-fit rubric | Select a format hypothesis and the evidence needed before a pilot |
| Destination, year, category, and proposed SKU | Nonoverlapping channel shares/volumes and a disclosed channel-fit rubric | Prioritize distributor and retail-channel interviews |
| Destination, volume, price, freight, tariff, and marketing | Landed cost, profit, margin, domestic comparison, and hurdle verdict | Renegotiate a scenario or advance it to diligence |
| Five strategic criterion weights | Normalized sub-scores, reranked markets, and roadmap tiers | Evaluate sensitivity to executive priorities |

Use English throughout the product. Explain that domestic growth alone does not establish the best allocation: price realization, costs, access, and risk also matter. Do not assume Japan must win; derive the recommendation from the specified data and model.

## 2. Delivery and technical constraints

The primary deliverable is dashboard.html at the repository root. It must open through a file:// URL and remain fully functional offline. Embed the prepared data, CSS, application JavaScript, and Chart.js library inside the final HTML. Do not use runtime fetch calls, CDNs, APIs, authentication, a database, or a required web server. Use HTML5, CSS, vanilla JavaScript, and Chart.js. A heatmap may use an accessible HTML table with colored cells instead of a plugin.

Separate reusable analysis, configuration, browser decision logic, and presentation. Provide:

- prepare_data.py: read the four source CSVs, validate schemas, generate the six analysis tables and local validation evidence, and preserve every source measurement/missing position.
- analysis.py: reusable market metrics, coverage and reconciliation logic, hierarchy-safe channel/packaging analysis, and chart-ready outputs from the generated tables.
- build_dashboard.py: run preparation, generated-data validation, analytical calculations, and deterministic HTML generation in one command.
- A separate editable configuration file containing the planning assumptions and their provenance/status.
- Separate JavaScript source for pure financial and MCDA functions and UI controllers; embed it during the build.
- Vendored Chart.js with its version and license recorded, meaningful automated checks, and README instructions for installation, build, and verification.

Reuse the repository's existing environment and lockfile when present. Otherwise provide a pinned requirements file for Python 3.10+ and pandas 2+. No XLS reader is needed for this CSV-only build. Avoid introducing a frontend framework or toolchain for this small static application. Support python build_dashboard.py --data-dir "Final Data Version", with that repository-relative directory as the default input location; use the repository's environment runner if applicable. This command must create missing generated directories/tables and checks before rendering. A missing generated file is work to perform, not a missing-input blocker. Do not replace an existing lockfile unnecessarily.

Treat Final Data Version/ and its four CSVs as read-only. Write application source, generated tables, generated validation evidence, and dashboard.html outside that directory. Implement the preparation yourself in this repository. Do not require a pre-existing source-processing script, manifest, hierarchy CSV, validation JSON, earlier data version, XLS workbook, or full CPG_Data_V3 package. No extra source data or xlrd is required. Network access may be used during development to obtain a pinned library, but the built dashboard must not depend on it. If a dependency is unavailable, report the actual blocker rather than claiming an offline build works.

## 3. Source data and required preparation

### 3.1 The only empirical inputs

Read these exact repository-relative UTF-8 CSVs, allowing an optional UTF-8 BOM. The folder name contains spaces; quote the directory in shell commands. An explicit --data-dir override may change the directory, but do not silently select a different data version or a sample. Only a missing/incompatible one of these four source files is an input blocker; derived files and checks must be generated.

| Required file in Final Data Version/ | Source rows | Non-year columns | Missing annual measurements |
|---|---:|---|---:|
| market_sizes_clean.csv | 72 | Geography, Geography_Level, Region, Category, Data Type, Unit, Original_Unit, Current Constant | 22 |
| retail_channels_clean.csv | 828 | Geography, Geography_Level, Region, Category, Outlet Type, Channel_Level, Parent_Channel, Channel_View, Data Type, Unit | 3,373 |
| pack_type_clean.csv | 530 | Geography, Geography_Level, Region, Category, Pack Type, Parent_Pack_Type, Pack_Level, Unit | 96 |
| pack_size_clean.csv | 7,209 | Geography, Geography_Level, Region, Category, Pack Type, Parent_Pack_Type, Pack_Level, Pack Size, Pack_Size_Value, Pack_Size_Unit, Is_Total_Size, Unit | 2,758 |

Each file also contains exactly the eleven annual columns 2015 through 2025. Read identifiers as metadata and annual cells as numeric or missing. Keep blanks missing, true numeric zeros zero, and all-missing source series intact. Preserve numeric precision. Reject unexpected nonnumeric tokens, nonfinite values, negative measurements, out-of-range shares, invalid boolean labels, duplicate business keys, and inconsistent metadata with file/key/field diagnostics. The '-' in market Current Constant is metadata, not a missing year measurement.

Source wide keys are: market = Geography, Category, Data Type, Unit, Current Constant; channels = Geography, Category, Outlet Type, Data Type; pack type = Geography, Category, Pack Type; pack size = Geography, Category, Pack Type, Pack Size. Add Year to obtain long-table keys. Validate that remaining geography/hierarchy/unit metadata agrees for each business key. Do not assume absent Packaging Class, packaging Data Type, or Market_Role columns are required: the packaging measure is retail/off-trade annual unit volume in million units; China is the domestic comparator in application logic.

### 3.2 Generate the analysis tables

Create the following CSVs under generated/dashboard_data/. These are program outputs, not files to locate on GitHub or receive from the user. Start from the four wide inputs even if stale generated files already exist; reuse a cache only after verifying it against current source hashes and transformation version.

| Generated file | Expected rows | Measurement field |
|---|---:|---|
| market_sizes_tidy.csv | 792 | Market_Value, a generic physical-or-monetary measure |
| market_volume_tidy.csv | 396 | Total_Market_Volume |
| retail_channels_tidy.csv | 9,108 | Channel_Share_Pct; Unit = % |
| market_channels_merged.csv | 9,108 | Share, market total, and derived channel physical volume |
| pack_type_tidy.csv | 5,830 | Unit_Volume_MUnits |
| pack_size_tidy.csv | 79,299 | Unit_Volume_MUnits |

Implement this sequence:

1. Melt only the eleven annual columns, retaining every non-year field and every missing measurement row. Parse Year as integer. Name the market measure Market_Value, the channel measure Channel_Share_Pct, and both packaging measures Unit_Volume_MUnits. Verify wide-to-long-to-wide round trips retain values, row identities, metadata, and missing locations. Do not aggregate, interpolate, or create a fully observed grid.
2. Select physical observations from the generated all-market table: Coffee / Retail Volume / Tonnes; RTD Coffee / Off-trade Volume / million litres. Rename Market_Value to Total_Market_Volume. This table must contain one record per Geography, Category, Data Type, Year: 396 records including eleven missing India RTD totals. Market_Value in the 792-row all-market table is not always money.
3. Generate the channel merge by left-joining shares to this physical subset on Geography, Category, Data Type, Year, with many-to-one validation and zero unmatched keys. Keep channel metadata, rename the share table's Unit to Channel_Share_Unit, and take the physical Unit from the market table. Validate metadata consistency. Compute Channel_Volume = Total_Market_Volume * Channel_Share_Pct / 100. A missing operand gives a missing result. Do not join monetary rows, duplicate channel records, or sum repeated market totals.
4. Preserve supplied Parent_Pack_Type, Pack_Level, original Pack Size labels, parsed Pack_Size_Value/Unit, and Is_Total_Size when reshaping packaging. Parse True/False explicitly, never by string truthiness, and validate that Is_Total_Size is True if and only if Pack Size equals Total. Require exactly one total-size row per geography/category/type. Total-size rows have blank parsed size/size-unit fields; other size values must be positive and agree with their g/ml labels. Packaging Class and packaging Data Type were constant fields removed before these inputs were uploaded; do not recreate them as independent observations.
5. Verify the 5,830 generated total-size observations match the corresponding packaging-type totals and missing positions one-to-one, using Geography, Category, Pack Type, Year. These are alternative representations of the same total, not additive measurements.

The 36 duplicate wide channel rows named Total have already been removed from the source; Retail Channels is retained as the root. Do not repeat that removal or expect 864 source rows. Unit = % in the share-only table; Unit in the merged table describes physical volume while Channel_Share_Unit = %. Retain Original_Unit and Current Constant for market traceability. The six generated views are not independent sources to concatenate.

### 3.3 Geography, missingness, and currency

The supplied data covers ten countries, seven regions, and World over 2015-2025. Country comparisons use Geography_Level = Country. Source country labels are China, India, Japan, Thailand, Australia, Brazil, USA, France, Germany, and United Kingdom. Keep USA as the join identifier and display United States through an explicit alias. Use the source Region field. Countries, regions, and World overlap: never add or rank them together, or label the sum of this country subset World.

Preserve eleven missing India RTD physical market observations and missing monetary observations; all its 253 merged channel rows have missing shares and channel volumes, not zeros. Brazil RTD e-commerce also remains missing. South Korea and Singapore have no source country observations. Across the generated tables expect 22 missing all-market measurements, 11 physical totals, 3,373 shares and derived channel volumes, 253 repeated merged market totals, 96 packaging-type measurements, and 2,758 packaging-size measurements. An all-missing aggregate remains unavailable; zeros count as observed. Serialize unavailable results as JSON null and show a reason, never NaN or a healthy-looking zero.

For monetary views select Coffee / Retail Value RSP or RTD Coffee / Off-trade Value RSP with Unit = USD million and Current Constant = Current Prices. The uploaded values are already converted to nominal USD million, with Original_Unit preserving original currencies/scales. Do not apply another FX conversion or refresh rates. Supplied provenance is annual World Bank PA.NUS.FCRF conversions, scaling million/billion and dividing by local currency per USD, stored to six decimals. That lineage is context, not a requirement to read a missing FX document or independently verify unavailable historical inputs. Four CSVs alone do not establish that historical conversion audit. Nominal USD growth can reflect price/FX effects and is not real demand growth. Country USD totals need not match source regional totals. Forecast/observation status is unspecified; use Source series labels.

### 3.4 Derive hierarchy and validation evidence

All hierarchy information needed here is already present in the four source CSVs. Derive distinct channel mappings from Outlet Type, Channel_Level, Parent_Channel, Channel_View, and packaging mappings from Pack Type, Pack_Level, Parent_Pack_Type. Require each label to have one consistent mapping. Check parent existence, acyclic paths, consecutive levels, and valid roots (Retail Channels and Total Packaging). The two packaging files must agree on the same 37-type mapping. Do not require a separate hierarchy CSV or original Excel indentation.

Generate generated/validation/packaging_hierarchy.csv from that mapping, plus reconciliation.csv, validation.json, and manifest.json. An optional channel hierarchy export is also useful. Compute hashes from the four input files before and after preparation and record unchanged input bytes, filenames, schemas, counts, missingness, transformation version, output hashes, and checks actually performed. Newly generated hashes identify this build and preservation; they do not prove a match to an unprovided historical manifest. Do not require SHA256.json or any pre-existing validation file.

Generate reconciliation records yourself:

- For channels and packaging type, group by Geography and Category, then each distinct referenced Parent_Channel or Parent_Pack_Type except the sentinel Not applicable. Include the root parents Retail Channels and Total Packaging when referenced by their children. Select exactly one corresponding parent row and its recorded direct children. Do not expand to every globally possible type or treat unlisted types as inserted zero children.
- For packaging size, group by Geography, Category, Pack Type. The parent is the single Is_Total_Size = True record; children are all recorded False records in that group. Exclude the total from its own detail.
- For each year let n be the count of recorded child series, including those whose annual value is missing. Complete means the parent is observed, n > 0, and every child value is observed. If complete, Child_Sum is the sum of direct children and Difference = Child_Sum - Parent_Value. Otherwise full Child_Sum and Difference are null and Status = incomplete. A separately named known-child subtotal may be shown, but cannot certify the whole distribution.
- Use the specified source-resolution rule Rounding_Bound = (n + 1) * 0.05 + 1e-9, in percentage points for channels or million units for packaging. Classify a complete group as within_rounding if abs(Difference) <= Rounding_Bound, otherwise unreconciled. This is a declared numeric-resolution rule; do not claim to have rechecked unavailable Excel formatting.
- Store kind, key, Year, Parent_Value, Child_Sum, Child_Count, Missing_Children, Difference, Rounding_Bound, Status. kind is retail_channels, pack_type, or pack_size; key identifies the geography/category/parent. Preserve actual missing parents and children. Expected recomputed status counts for the supplied snapshot are channels 952 within_rounding / 1,028 incomplete; packaging types 2,162 / 93; sizes 4,490 / 1,340, totaling 10,065 records. No out-of-bound complete group is expected. These are derived checks to calculate, not certificates to read or constants to paste into the UI.

Evaluate completeness on the full group before selecting Top 3, Top 8, or an individual size. Child-observation coverage = (Child_Count - Missing_Children) / Child_Count when Child_Count > 0; show parent availability separately. Displayed-subset coverage, annual period coverage, and a value share are distinct. A known selected size cannot hide missing siblings. Incomplete groups may show available bars/counts with coverage, but not complete pies/stacks or forced normalization. Other is allowed only as a verified known nonoverlapping remainder, never a missing-data bucket.

Channel_View = Overview selects offline versus e-commerce. Detail spans multiple depths and is not one additive set. For detail and Top 3 compare direct siblings of one parent, rank observed values only, and disclose observed n. Source shares refer to the entire compatible retail/off-trade market; filtering a parent does not change that denominator. Any within-parent percentage must be separately computed and labeled. Use the generated hierarchy for packaging sibling sets; never sum parents and descendants. These rules must be implemented from source metadata, not delegated to an absent validation artifact.

## 4. Reusable metrics and analytical boundaries

Implement pure functions that return structured values, validity reasons, denominators, units, and coverage. UI components must use one result rather than duplicate aggregation rules.

- **Market size:** the selected end-year physical or monetary value, labeled with country, category, measure, year, and unit. Never silently substitute the nearest available year.
- **Physical CAGR:** (end/start)^(1/(end_year-start_year))-1. Defaults 2015–2025 use ten intervals. Require end_year>start_year, positive start, and both endpoints; positive-to-zero gives -100%, missing endpoints or zero start give unavailable. A separately labeled nominal USD-value CAGR uses the same formula on compatible value records; it is not physical or inflation-adjusted growth.
- **YoY:** current/prior-1, with adjacent years, both present, and prior>0; otherwise unavailable. Missing intermediate years remain chart gaps.
- **Period coverage:** nonmissing annual observations / all years in the selected inclusive period. True zero counts as observed. A valid endpoint CAGR may coexist with partial period coverage; display both.
- **Country median:** median among the currently selected country scope with valid same-category, same-unit, same-metric, same-period observations. Exclude missing results and regional/global rows; disclose valid n and the benchmark set. An empty set gives unavailable.
- **Retail unit value:** Coffee USD/kg = value_USD_million * 1,000 / tonnes. RTD USD/litre = value_USD_million / million_litres. Require compatible positive volume. This is category-average retail unit value, not an observed specialty price or the scenario wholesale price.
- **Digital access:** the source Retail E-Commerce share and end-minus-start change in percentage points. It covers the full source e-commerce channel, not measured cross-border access or named-platform sales. Keep a missing series unavailable.
- **Packaging-type share:** selected type unit volume / matching geography/category/year Total Packaging unit volume * 100, or an explicitly labeled share within a selected parent. Validate a positive known denominator and the partition's coverage. Annual counts are million units, not tonnes, litres, or money.
- **Packaging-size share:** for all-format sizes select Pack Type=Total Packaging; for format-specific sizes select exactly that Pack Type. Match the Is_Total_Size=True denominator on geography/category/type/year, and rank only Is_Total_Size=False records. Keep source labels and parsed Pack_Size_Value/Unit. Total has blank parsed size fields; g and ml describe individual package size, not the annual count unit. Do not invent small/medium/large bins or convert grams to millilitres. All 5,830 size-total records match type totals, including 96 paired missing values.

For incomplete packaging partitions, individual known counts and ratios to a known denominator can be displayed with explicit partial-coverage labels, but not as a complete mix or definitive consumer-preference ranking. Packaging patterns do not identify whole-bean versus instant demand, Yunnan-brand preference, nitrogen-drip adoption, or validated shelf life. Source dimensions do not establish population, firm shares/HHI, tariffs, freight, exporter costs, or origin affinity. Exclude HHI/per-capita claims and keep financial/non-growth MCDA attributes as the disclosed assumptions below. Measured physical growth can be negative; do not retain an unsupported domestic +14.8% growth claim or force an East Asia winner.

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

South Korea and Singapore presets support financial what-if calculations only. Keep their observed market size, source channel mix, growth, and MCDA composite unavailable. Do not invent these measurements or borrow Japan's data to complete their rows.

China Domestic uses the domestic financial model below, a scenario tariff of zero, a planning transit time of 2 days, and a planner-assigned affinity of 75. These affinity scores are subjective inputs, not measured consumer sentiment. Store source/status/rationale alongside configuration entries; mark externally unverified seeds accordingly.

For channel fit, use the following transparent initial planning rubric if no documented team-approved scoring evidence exists. It is SKU/channel fit scoped to the selected destination, not an empirical country ranking:

| Proposed format | Specialty boutiques | Premium supermarkets | Convenience chains | Cross-border e-commerce |
|---|---:|---:|---:|---:|
| Specialty whole bean | 5 | 4 | 2 | 5 |
| Nitrogen-flushed drip bags | 4 | 4 | 4 | 5 |
| RTD cold brew cans | 3 | 4 | 5 | 2 |

Explain the 1–5 ordinal scale and qualitative rationale: boutique specialty fit, listing/distributor costs, grab-and-go suitability, shipping weight, and cold-chain requirements where applicable. Do not invent destination-specific differences or a numerical conversion from channel share to suitability. Source sales channels and rubric channels differ: Supermarkets does not isolate premium supermarkets; Food/drink/tobacco specialists does not isolate specialty-coffee boutiques; Retail E-Commerce does not isolate cross-border platforms. Keep observed source distributions and qualitative proposed routes visibly distinct rather than claiming exact segment measurements.

## 6. Financial model and exclusive verdict rules

This is a simplified annual contribution-style operating scenario for finished Coffee only. Keep the user-facing label Modeled operating profit/margin and disclose excluded corporate overhead, capex, financing, income tax, FX changes, working-capital timing, and unmodeled distributor/listing costs. It is not audited net income or a complete investment valuation. RTD remains available for market, packaging, and channel exploration and a proposed can-format card; do not apply roasted-coffee USD/kg economics to RTD litres or cans. Simulator costs, wholesale prices, tariffs, and budgets are planning assumptions, not exporter economics inferred from V3 retail values.

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

MCDA and its radar are a Coffee-only strategic screening model using the fixed 2015–2025 horizon. The observed eligible focal markets are China, Japan, Australia, USA (display United States), and Germany. Show South Korea and Singapore after the ranked rows with No source data / unranked. Other countries can be explored in data views but do not enter MCDA without a defined economic and affinity preset. Explain this scope when RTD exploration is selected. Use generated physical-volume CAGR and the planning presets above, with a common 50-tonne volume for financial comparability. Simulator edits are an independent scenario and do not silently change MCDA attributes. Weights change ranking; changing destination presets requires editing the disclosed configuration and rebuilding.

Let clip(x) limit a value to [0,100]. Calculate:

    growth_score = clip(100 * (CAGR_percentage + 5) / 15)
    margin_score = clip(100 * preset_modeled_margin_pct / 50)
    tariff_score = clip(100 * (1 - preset_tariff_pct / 35))
    logistics_score = clip(100 * (32 - preset_transit_days) / 30)
    affinity_score = planner_assigned_affinity
    composite = sum(score_j * weight_j) / sum(weight_j)

These are disclosed planning anchors, not industry standards: growth ranges from -5% CAGR (score zero) to +10% (score 100), margin from 0% to 50%, tariffs from 35% to 0%, and transit from 32 to 2 days. The growth mapping distinguishes observed contractions rather than collapsing all negative CAGRs to one score. Use the domestic model for China's margin score. Show raw metrics, normalized scores, and the normalization method. If a required criterion is missing, mark the country Insufficient data and leave it unranked; do not silently impute zero or redistribute weights across missing criteria. Affinity, tariff, logistics, and margin remain assumption-based components even when growth is measured.

Use five weight sliders from 5 to 50, step 1. Defaults: growth 25, margin 30, tariff/trade ease 20, logistics 15, affinity 10. Display both raw weights and their effective normalized percentages. Normalize mathematically by the current sum; do not force the sliders themselves to total 100. Reset restores these five values. The pure scoring function must support nonnegative test weights outside slider bounds and reject an all-zero weight vector.

Rank eligible markets by unrounded composite descending; break exact ties alphabetically by canonical display country name. Show one decimal only for display. Include China in the numerical ranking but always assign its roadmap label BASE: MAINTAIN & DEFEND. Assign contiguous ranks only to eligible rows; do not give South Korea or Singapore a numeric rank or treat their financial what-if verdict as market validation.

For each overseas market, use its preset financial verdict with these rules: HOLD if its financial verdict is HOLD; otherwise PHASE 1: PRIORITY ENTRY for composite >=80 with an accretive financial verdict; otherwise PHASE 2: CONDITIONAL ENTRY for composite >=65; otherwise PILOT: TEST BED for composite >=50; otherwise PHASE 3 / HOLD. Missing required data gives INSUFFICIENT DATA. These are screening labels, not investment approval. Never hard-code the winners or force the example scores from an earlier vision document.

## 8. Interface, views, and interaction contract

Create a premium specialty-coffee visual system: espresso backgrounds #0c0a09 and #141210; card surfaces rgba(26,22,19,0.85); subtle bronze borders; crema #d4a373, gold #e9c46a, copper #c27847, green #52b788, red #e76f51, and slate #457b9d. Use Outfit headings and Inter body text only if the font files can be bundled locally; otherwise use readable system sans-serif fallbacks. Use generous spacing, legible contrast, a 1440px maximum content width, a sticky header, and persistent six-tab navigation.

Default to Executive Scorecard, Japan's financial preset, Coffee, and 2015–2025. Provide the following views:

1. **Executive Scorecard:** Title Yunnan Coffee Global Entry; a brief decision statement; an evidence-dependent status banner; four KPI cards for selected-scenario margin spread, current top-ranked eligible overseas target, selected exploration market's endpoint physical volume, and selected scenario tariff. Label the source-volume card with market, category, year, and unit. Include the five-axis readiness radar for China, Japan, Australia, and United States; a per-kg unit-economics comparison for the same four markets; and the seven-focal-market evaluation table, with South Korea and Singapore explicitly unranked/missing. The table shows source volume, CAGR, retail e-commerce share, scenario margin, and screening status as separately identified measures. All figures and statuses come from the relevant model or data. Give a clear next action such as investigate a pilot, revise terms, or hold, including the key condition. If no eligible market clears the priority-entry rule, say so even when one has the highest score.
2. **Market Attractiveness:** Category, country-scope, start/end-year controls; physical-volume trends with gaps; a table of physical size, nominal USD value, category-average retail unit value, CAGR, YoY, and period coverage; a valid-country median benchmark; a growth-and-digital-access bubble chart; and evidence-dependent takeaways. Bubble x is physical CAGR, y is end-year Retail E-Commerce share (%), and area is end-year physical market volume. Scale radius with the square root of volume, use one category/unit at a time, and allow negative growth. Tooltips identify raw metrics and coverage. Omit unavailable points with reasons rather than moving them to zero. Regional/World benchmarks are a separate context view, never investable-country rankings. Do not add observed specialty-price, HHI, or per-capita panels.
3. **Product-Market Fit & Channels:** Exploration-market, category, endpoint-year, channel-parent, pack-type, pack-size, and proposed-format controls. Show the channel Overview, a direct-sibling drilldown and observed Top 3, e-commerce trends, packaging family/type trends, and scoped size counts/shares with reconciliation and coverage. Show original hierarchy labels in accessible source tables. Default pack type to Total Packaging for all-format sizes; a selected type narrows the denominator. Sort numeric sizes numerically in g or ml, exclude total-size rows from ranking, and label any top-eight chart as a subset with a complete table. Missing or incomplete data stays visible as partial/unavailable, with no fabricated Other or 100% normalization. Include the planning channel-fit heatmap and three proposed SKU cards: 250g valve-pouch whole bean with an SCA 84+ target; 10g nitrogen-flushed drip bag in a 10-pack carton; and 250ml RTD can with shelf-life/process validation needed. These are product hypotheses informed by category evidence, not source-certified quality, specialty demand, or margins.
4. **Financial Simulator:** Destination selector, all five paired inputs, reset-selected-destination button, live input labels, cost breakdown, revenue/profit/margin cards, same-volume domestic comparison, signed profit delta and margin spread, two-bar profit chart, and exclusive verdict box. Both bars share a dollar scale with a visible zero line and support losses. Use green when export profit exceeds domestic and red when it is lower; also identify the difference with text.
5. **MCDA Decision Matrix:** Five sliders, reset button, current effective weights, eligible ranked rows plus explicit unranked South Korea/Singapore rows, exposed raw metrics/sub-scores, normalization explanation, and roadmap labels. Update immediately with no reload. Include a plain-language note that rankings combine measured growth with illustrative economic and affinity assumptions.
6. **Risks & Objections:** Cards for domestic price competition, Yunnan origin credibility, trade-policy uncertainty, FX exposure, freshness/transit risk, channel fees, data limitations, and capex/working-capital gaps. Each gives the objection, available evidence versus assumption, mitigation, responsible business role, and validation gate. Include a conditional compliance roadmap covering product classification, origin/preferential documentation, food/import labeling, phytosanitary applicability, organic claims/JAS where applicable, and EUDR traceability where applicable. State each item's destination/product scope, verification status, and milestone before contracting or shipping. Do not label every item universally mandatory or assert current legal deadlines without an authoritative dated source.

Label the evaluation-table financial margins, cross-market per-kg economics, and MCDA financial attributes as fixed 50-tonne preset comparisons. The selected-scenario KPI cards and simulator charts use the live scenario inputs. Source-validation/coverage status, MCDA screening status, and the financial verdict are separate concepts and must have separate labels. Reuse the same financial function for both scopes, with their respective inputs; do not present a fixed-preset figure as a live edited scenario.

Interaction scope must be explicit:

- Market exploration controls in tabs 2 and 3 share category, start/end years, and selected exploration market. Update market, channel, packaging, coverage, and benchmark views plus the scorecard source figures. Default to Japan. Market figures use the canonical physical/value panel, not repeated joined channel or pack-size rows. MCDA stays on its labeled fixed Coffee horizon.
- Coffee allows whole bean or drip bags as the proposed format; RTD Coffee allows cold brew cans. Switching category selects its compatible default format (whole bean for Coffee, cans for RTD). Keep all three SKU cards visible for context, but base the active channel-fit interpretation on the compatible selected format and category.
- Channel-parent, pack-type, and pack-size controls are local evidence filters, populated from the source dimensions and generated tables. Reset an inapplicable pack type to Total Packaging after a market/category change, clear an invalid size choice, and show the missing/coverage state. Filtering a channel parent does not change full-market share denominators. Selecting a measured pack size does not silently alter assumed wholesale prices, production costs, or annual export volume.
- Country scopes are Observed Focal Markets (China, Japan, Australia, United States, Germany), Asia-Pacific & Australasia Countries (China, India, Japan, Thailand, Australia), and All Observed Countries (the ten listed countries). Default to Observed Focal Markets. This country grouping is distinct from the source's Asia Pacific regional aggregate. Keep World/regional aggregates in a separate benchmark selector. South Korea and Singapore remain visible as explicit missing focal-market rows and can be selected for scenario-only exploration; source panels then state that those countries are absent. Populate years from 2015–2025 source availability and require start year < end year. If a scope change excludes the selected observed market, select Japan when available, otherwise the first alphabetically displayed country in the scope, and announce the change. Missing selected observations remain unavailable, never interpolated.
- Selecting an overseas market with a defined preset in a table or tab 3 synchronizes the simulator destination. Markets without a financial preset can be explored without changing the current export scenario; clearly label that separate scope. Switching simulator destination resets price, freight, tariff, and marketing to its preset, preserves annual volume, and announces the reset. A destination reset button restores its full preset including 50-tonne volume. China is a comparator; selecting it in exploration preserves the export destination. Selecting South Korea or Singapore in the simulator shows a Scenario only: source market data unavailable notice and must not manufacture source charts or MCDA eligibility.
- Every simulator input updates its numeric partner, cards, cost chart, profit chart, scorecard selected-scenario figures, and financial verdict from one calculated result object. It does not alter source market data or MCDA weights.
- MCDA weight changes update the ranking table, scorecard top-target card, and screening summary. Radar values remain the same unweighted criterion sub-scores; weights change their contribution to the composite, not the underlying attributes. Show a separate financial verdict and MCDA roadmap status so differing scopes are understandable.
- Switching tabs preserves state and resizes the relevant Chart.js instances after the panel becomes visible. Avoid duplicate chart instances and event handlers. Reset MCDA affects only MCDA weights; reset scenario affects only the selected scenario.

Every chart needs an informative title, unit-bearing axes, useful tooltips, and a caption stating the decision question. Provide nearby accessible data tables or equivalent text summaries. Format currency consistently, volumes with their units, missing values as Not available, and actual zeros as zero. Sources/methodology and assumption disclosures must remain accessible in the offline file. Links to repository documents are optional convenience links, never the sole explanation of a metric.

Support 375px phone, 768px tablet, 1280px laptop, and 1920px desktop widths. Stack cards and charts on small screens. Wide tables may scroll within their own labeled containers; the window must not overflow horizontally. Use semantic landmarks, a single h1, associated labels, visible focus states, keyboard-operable sliders/number inputs, and accessible tabs with roles, aria-selected, aria-controls, arrow keys, Home/End, and predictable focus. Do not rely on flags, hover, or color alone. Respect reduced-motion preferences and avoid excessive live announcements during slider dragging.

## 9. Build order and acceptance checks

A clean checkout containing this prompt and only the four wide CSV inputs must be sufficient after installing the stated dependencies. Implement source ingestion, wide-to-long preparation, derived-table/hierarchy/reconciliation generation, reusable metrics, pure financial/MCDA functions, and then the interface and offline HTML. The normal build command performs this whole pipeline. Missing generated files must be created; do not stop to request the six analysis tables or validation artifacts from the user. A genuinely missing or incompatible source CSV must identify its exact expected path. Use temporary fixtures for negative tests and preserve all source inputs.

Required checks:

1. **Four-input clean build:** Starting without generated/dashboard_data/ or generated/validation/, python build_dashboard.py --data-dir "Final Data Version" generates all six analysis tables, local validation evidence, and dashboard.html. Require no CPG_Data_V3 directory, supplied tidy file, processing script, manifest, or external documentation. Verify the four input row/missing-cell counts and schemas stated in Section 3, their unique keys and year columns, and unchanged input hashes. A generated manifest records current input identity, not an unavailable historical certification.
2. **Derived tables and round trips:** Output row counts are all-market 792, physical 396, shares 9,108, merged channels 9,108, packaging type 5,830, and packaging size 79,299. Check wide-long-wide values and missing masks; zero must not turn into blank or vice versa. Missing counts are all-market 22, physical 11, shares/derived channel volume 3,373 each, repeated merged market totals 253, packaging type 96, and size 2,758. India RTD and Brazil RTD e-commerce remain unavailable. Strict JSON uses null, not NaN, and all-missing sums remain unavailable.
3. **Join and unit controls:** The physical market key is unique; the channel join is many-to-one with zero unmatched keys and no row multiplication. China Coffee 2025 Supermarkets uses 61,314.5 tonnes * 20.5% = 12,569.4725 tonnes; e-commerce 46.7% gives 28,633.8715 tonnes. Do not sum the repeated market total over channels. Shares' Unit = % is renamed Channel_Share_Unit in the merge; merged Unit is physical. Source volume shares are not observed channel revenue shares.
4. **Market metrics:** Coffee 2015-2025 physical CAGR is China -0.343139%, Japan -1.148602%, Australia +1.548341%, USA -0.619798%, Germany +0.590297%, within 0.00001 pp. Japan 2025 volume = 97,775.2 tonnes. Supplied nominal values are China Coffee 1,937.134306 and Japan Coffee 3,081.026242 USD million (tolerance 0.000001 USD million). Category-average retail unit values use the stated USD/kg conversion, not another FX conversion. A synthetic 100-to-200 ten-year series gives about 7.17735%; test missing endpoints, positive-to-zero, zero prior/start, YoY adjacency, coverage including true zero, and median valid n. Do not label nominal-value growth physical or inflation-adjusted growth.
5. **Generated hierarchy and reconciliation:** Derive the 37-type packaging mapping from both packaging inputs and require agreement. Independently recompute channel statuses 952 within_rounding / 1,028 incomplete, type 2,162 / 93, and size 4,490 / 1,340: 10,065 total group-year records. Check per-group child membership and n-based bounds. Do not read these outcomes from a supplied certificate, hard-code pass statuses, combine hierarchy depths, or certify a partial set merely because known children match the parent. An invalid hierarchy fixture fails clearly; a valid but incomplete group stays available with the correct coverage warning.
6. **Packaging benchmarks:** The 5,830 generated total-size records match type totals and missing positions one-to-one, including 96 paired missing totals. Japan Coffee 2025: total 746.9, Flexible Packaging 429.2, overall 80 g count 170.0 million units. Japan RTD: total 9,425.2, Metal 6,776.8, overall 190 ml count 3,282.6; its size sum 9,425.1 is within its computed bound. China Coffee: total 292.4, Paper-based Containers 121.7, overall 624 g count 71.6. Test boolean parsing, g/ml scope, and total exclusion from size ranking.
7. **Incomplete partition fixture:** China RTD 2025 Rigid Plastic has parent 645.0, HDPE 11.1, PET 633.9, and missing Thin Wall Plastic Containers. It remains incomplete, with null full child sum/difference, despite the observed children apparently summing to the parent. China's overall RTD size partition has missing 190 ml and 210 ml values; observed 180 ml count 427.9 can be shown with partial coverage, not as a complete preference distribution. Selecting just that known size or a Top 8 subset must not change the full group's incomplete status.
8. **Japan financial default:** At 50 tonnes, wholesale price $26.00/kg, freight $0.80/kg, tariff 0%, and marketing $60,000: revenue $1,300,000; production $575,000; freight $40,000; duties zero; landed COGS $615,000; total modeled cost $675,000; profit $625,000; margin 48.076923%. Domestic profit $195,000 and margin 23.636364%; profit delta +$430,000; spread +24.440559 pp. Verdict ACCRETIVE OVERSEAS EXPANSION. Tolerances $0.01 and 0.01 pp. These are model outputs, not source profitability.
9. **Downside and boundaries:** United States fixture: 50 tonnes, price $22.00/kg, freight $2.50/kg, tariff 25%, marketing $100,000 gives revenue $1,100,000, duties $275,000, total modeled cost $1,075,000, profit $25,000, margin 2.272727%, profit delta -$170,000, and HOLD. Test equality at zero delta, 10%/18% margin, and +5 pp spread. Higher freight/tariff/marketing lowers profit when other inputs stay fixed. Volume changes recalculate domestic fixed-cost allocation. Invalid/blank input shows validation rather than stale or NaN results.
10. **MCDA correctness:** With the specified presets and derived physical series, default computed order/scores are Australia 77.771045, Japan 77.265150, China 64.443253, Germany 56.015575, USA 32.871765 within 0.00001 points. Derive them; do not hard-code displays or winners. South Korea/Singapore remain unranked. Doubling weights to [50,60,40,30,20] leaves pure-function scores unchanged within 1e-9; UI bounds remain 5-50. Test deterministic ties, missing criteria, all-zero rejection, crossed-preference fixtures, reset, and unchanged raw radar attributes.
11. **Failure handling and preservation:** On temporary inputs test a missing source file/header/year, duplicate key, invalid numeric token, incompatible unit, malformed boolean, conflicting hierarchy mapping, or unmatched physical key for a channel row. Errors name file/key/field. Delete only temporary generated outputs in a disposable test setup to prove they are regenerated; never delete source inputs. Do not require a pre-existing manifest or validation document. Do not fabricate population, HHI, specialty prices, regulatory facts, or absent countries' metrics.
12. **Actual offline UI:** Open dashboard.html with networking disabled. Exercise six tabs, both categories, scope/period changes, sibling-channel and packaging drilldowns, incomplete data, India RTD, scenario-only countries, paired simulator controls, extremes, and independent resets. Check readable units/captions, coverage messages, source/model scope, preserved state, resize behavior, keyboard operation, four viewport widths, and zero uncaught errors or missing asset requests. Try Chromium and another available browser and report actual coverage.

Report actual checks and outcomes, including source hashes before/after, generated paths, and any discrepancy against the supplied snapshot. Do not alter inputs to hit expected counts or treat a polished screenshot/successful HTML build as proof of correct analytics.

## 10. Completion report

When finished, identify the files created/changed, the exact install/build/test commands run, where to open dashboard.html, and which acceptance checks passed. Disclose incomplete source partitions, unavailable evidence, illustrative presets, untested browser coverage, and actual blockers. Identify the four source files and their hashes, the input directory, and the analysis/validation artifacts generated by this build. Do not imply that unprovided packages or pre-existing validation documents were read. Update README with the same reproducible build instructions and assumptions. Do not claim external verification, current regulatory compliance, source validation, or a test pass that you did not perform. The final result should let an executive trace a market shortlist through product/channel choices to a transparent financial hurdle and a sensitivity-aware screening recommendation.
