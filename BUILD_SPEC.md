# BUILD_SPEC.md — CPG Global Entry Strategy Decision Platform

**Course:** DSO 576 — Decision-Support Analytics & CPG Global Entry Strategy  
**Deliverable:** Revised Vision & Build Specification (`BUILD_SPEC.md`)  
**Student Name:** Benjamin (Ru Yi) Cai (`betakappa123`)  
**Team Members:**
**Repository Branch:** `main` / `Ben`  
**Primary Artifact:** [`dashboard.html`](dashboard.html)  

---

## 1. Revised Vision & Context

### 1.1 Specific User Persona
The primary user of this decision-support platform is the **Vice President of Global Strategy / Chief Growth Officer** at a mid-tier specialty coffee enterprise originating from **Yunnan Province, China** (e.g., a vertically integrated estate group in Pu'er or Baoshan cultivating high-elevation Arabica, operating dry/wet mills, and running commercial roasting lines). 

Secondary stakeholders include the **Chief Financial Officer (CFO)**, who evaluates export capital expenditure, working capital cycles, and cross-border currency/tariff exposure; the **Head of Supply Chain & Packaging**, who evaluates shipping routes, packaging shelf life, and customs compliance; and the **Board of Directors**, who must formally approve capital allocation between domestic retail store expansion and overseas export routes.

### 1.2 Core Business Decision
The user faces a high-stakes capital allocation decision:  
**Should the Yunnan coffee enterprise expand into international overseas markets, or should it remain 100% focused on defending and expanding its market share within domestic Chinese tier 1 and tier 2 cities?**

If the strategic decision is to expand overseas, the platform guides three interlocking tactical decisions:
1. **Target Market Prioritization:** Which international geographies should be entered first (e.g., East Asian RCEP partners such as Japan and South Korea vs. traditional Western markets like the United States and Germany)?
2. **Product Format & Packaging Selection:** Which product category and packaging format will maximize margin and brand equity (specialty single-origin whole bean in valve pouches vs. single-serve nitrogen-flushed drip bags vs. ready-to-drink [RTD] canned cold brew)?
3. **Route-to-Market & Channel Selection:** Which off-trade retail channels (convenience chains, specialty grocery, supermarkets, or cross-border e-commerce) offer the lowest barrier to entry, manageable distributor fees, and sufficient volume velocity?

### 1.3 Why the Tool Improves Current Practice
* **The Status Quo:** Currently, CPG leadership relies on static, disconnected PDF market research reports (Euromonitor Passport, ICO statistical bulletins), ad-hoc international broker decks, and qualitative executive intuitions. This workflow suffers from severe deficiencies:
  * *Disparate Financial Metrics:* Raw Euromonitor market sizes report country retail values in local currencies without annual FX alignment (e.g., Japan reported in `JPY billion`, China in `CNY million`, Germany in `EUR million`), leading analysts into erroneous scale comparisons or tedious manual spreadsheet reconciliations.
  * *Volume-Value Disconnect:* Headline revenue figures obscure underlying physical volume consumption trends and per-capita realities.
  * *The "Domestic Growth Fallacy":* Executive teams observe rapid top-line coffee consumption growth in China (+14.8% CAGR) and instinctively assume domestic reinvestment is optimal, failing to model the destructive margin compression caused by domestic price wars (¥9.90 / $1.40 retail cup discounting by Luckin and Cotti Coffee, forcing green bean procurement margins down to 12.5%).
  * *Blindness to Trade Barriers:* Teams evaluate large foreign markets like the United States ($28.5B TAM) while overlooking 25% Section 301 punitive tariffs, elevated trans-Pacific ocean freight, and long shipping lead times (24–32 days) that degrade roast freshness.
* **The Platform Improvement:** This interactive decision engine unifies verified physical market volumes (Tonnes for coffee, Million Litres for RTD), 10-year historical and forecast CAGRs (2015–2025), granular channel volume distributions (9,108 observations), packaging format data, real-time landed-cost financial sensitivity modeling, and dynamic Multi-Criteria Decision Analysis (MCDA). It enables the CGO to test hypotheses in seconds, simulate landed margins under shifting tariffs and freight rates, and present an auditable, data-backed expansion roadmap to the Board.

### 1.4 Phase 1 Vision vs. Revised Vision Evolution
* **Phase 1 Conception (`project-start.md`):** The team initially scoped three isolated, competing candidate visions:
  * *Candidate Vision A:* Whether to expand overseas (country-level macro screening).
  * *Candidate Vision B:* Which retail channel to select in APAC (supermarkets vs. convenience vs. e-commerce).
  * *Candidate Vision C:* Which packaging format to adopt (bags vs. jars vs. cans).
* **The Revised Vision:** Through rigorous data inspection (`data-cleaning.md`) and stakeholder objection mapping (`objections.md`), the team recognized that treating these three questions in isolation leads to sub-optimal decisions. Choosing a country without knowing its channel structure leads to distribution failure; choosing a packaging format without knowing the target country's retail preference leads to unsellable inventory. 
* **The Integrated Synthesis:** The Revised Vision synthesizes all three candidate visions into an **integrated, multi-layered decision engine**:
  * **Anchor Decision (Vision A):** International Market Prioritization and Go/No-Go Hurdle Evaluation against a domestic China counterfactual.
  * **Execution Engines (Visions B & C):** Retail Channel Route-to-Market analysis and Packaging Format Suitability serve as the operational feasibility filters within each candidate market.
  * **Dynamic Financial & Governance Layer:** A real-time landed trade cost simulator and MCDA weighting engine that translates physical market data into net margin spreads ($/kg) and risk-weighted categorical roadmaps.

---

## 2. Core Use Cases

Each use case follows the standard decision-support interaction architecture:  
$$\text{User selects/inputs} \longrightarrow \text{Dashboard shows} \longrightarrow \text{User decides}$$

```
+--------------------------+       +--------------------------+       +--------------------------+
|   User Selects/Inputs    | ----> |     Dashboard Shows      | ----> |       User Decides       |
| (Filters, Sliders, Scens)|       | (Visuals, KPIs, Verdict) |       | (Capital, Market, Route) |
+--------------------------+       +--------------------------+       +--------------------------+
```

### Use Case 1: Cross-Market Attractiveness & Strategic Market Prioritization
* **User selects/inputs:** Target Product Category (`Coffee` vs. `RTD Coffee`), Evaluation Horizon (`2015–2025`), and Geographic Region (`Asia Pacific` vs. `Global Focal Markets`).
* **Dashboard shows:** 
  * The **Market Attractiveness Bubble Matrix** (X-axis: 10-year CAGR %; Y-axis: Average Retail Specialty Price in USD/kg; Bubble Size: Total Category Market Volume).
  * The **Multi-Vector Strategic Readiness Radar Chart**, comparing candidate markets across 5 dimensions: Market Volume Growth, Retail Price Realization, Tariff Favorability, Logistics Transit Speed, and Brand Origin Affinity.
  * The **Candidate Market Evaluation Matrix**, highlighting volume TAM, per-capita consumption (kg/capita/year), and initial strategic status badges (`PHASE 1: PRIORITY GO`, `PHASE 2: CONDITIONAL`, `PILOT: TEST BED`, `HIGH RISK: HOLD`).
* **User decides:** Which 2–3 priority markets (e.g., Japan and South Korea) warrant immediate commercial feasibility review and on-the-ground distributor interviews, and which markets (e.g., United States due to tariffs, Germany due to EUDR audit costs) should be relegated to Phase 3 or held.

### Use Case 2: Product Format & Packaging Strategy Alignment
* **User selects/inputs:** Selected Priority Market (e.g., `Japan`), Product Category (`Coffee`), and Packaging Class (`Total`).
* **Dashboard shows:** 
  * The historical unit volume evolution (million units) across packaging formats (Flexible Aluminium/Plastic, Stand-Up Pouches, Folding Cartons, Cans) from `DATA/clean/clean_pack_type_tidy.csv`.
  * The **Product-Market Fit Matrix**, displaying detailed specification cards for:
    1. *Specialty Whole Bean (Micro-Lot 250g valve pouch):* SCA 84+ score, pour-over cafe channel.
    2. *Single-Serve Nitrogen Drip Bags (10g filter pouch / 10-pack carton):* Ultrasonic sealed, office and premium retail channel.
    3. *RTD Cold Brew Cans (250ml slimline aluminium):* Grab-and-go convenience channel.
* **User decides:** Which physical SKU format to manufacture for export (e.g., committing capital to high-speed ultrasonic nitrogen drip-bag packaging lines, which match Japanese consumer daily brewing rituals and achieve 52–58% gross margins).

### Use Case 3: Route-to-Market & Retail Channel Prioritization
* **User selects/inputs:** Target Market (`Japan` vs. `China`), Product Category (`Coffee` vs. `RTD Coffee`), and Time Horizon (`2015–2025`).
* **Dashboard shows:** 
  * The **Derived Channel Volume Distribution** from `DATA/clean/clean_market_channels_merged.csv`, comparing physical volume (Tonnes / Million Litres) and percentage share across 23 off-trade retail channels (Supermarkets, Convenience Stores, E-Commerce, Hypermarkets, Discounters).
  * The **Channel Fit Heatmap**, rating channel suitability (1 to 5 scale) based on distributor margins, listing/slotting fees, cold-chain requirements, and Yunnan brand recognition.
* **User decides:** Which commercial channel partner to contract with (e.g., avoiding high-slotting-fee traditional supermarkets in Phase 1, prioritizing cross-border e-commerce [Rakuten / Amazon Japan] and specialty boutique grocers for whole bean, while reserving modern convenience chains [Lawson / 7-Eleven] for RTD cold brew).

### Use Case 4: Landed Margin Hurdle Rate & Financial Sensitivity Simulation
* **User selects/inputs:** Destination Country (`Japan`), Annual Export Volume slider (`10 to 300 MT`), Wholesale FOB Price slider (`$15 to $50/kg`), Ocean Freight & Insurance slider (`$0.30 to $3.50/kg`), Import Tariff slider (`0% to 35%`), and Destination Marketing Budget (`$10,000 to $250,000`).
* **Dashboard shows:** 
  * Live-calculated **Landed Cost Breakdown** (Green Bean Sourcing + Processing/Roasting + Packaging + Freight + Customs Duties + Destination Marketing).
  * Projected **Gross Revenue**, **Net Operating Profit ($)**, and **Net Operating Margin (%)**.
  * **Dynamic Counterfactual Comparison:** Direct comparison against the **Domestic China Benchmark** (selling the identical volume in Chinese tier 1/2 cities at $16.50/kg wholesale, incurring $12.00/kg cost and $30k marketing, yielding a 12.5% net margin).
  * **Dynamic Visual Bar Chart:** Side-by-side bar comparing Overseas Net Operating Profit vs. Domestic China Benchmark Profit.
  * **Dynamic Decision Banner:** Automated verdict callout (`ACCRETIVE OVERSEAS EXPANSION`, `CONDITIONAL / FEASIBLE`, or `MARGIN DILUTIVE / HOLD`).
* **User decides:** Whether the proposed export venture clears the corporate hurdle rate (minimum +5.0% net margin spread over domestic China sales), or whether FOB pricing, shipping terms, or destination marketing budgets must be renegotiated before contract signing.

### Use Case 5: Executive Risk-Weighting & Policy Sensitivity via MCDA
* **User selects/inputs:** Five strategic weighting sliders on the Multi-Criteria Decision Analysis engine:
  * *Market Growth Rate Weight (5% to 50%)*
  * *Profit Margin Potential Weight (5% to 50%)*
  * *Tariff & Trade Ease Weight (5% to 50%)*
  * *Logistics Proximity & Speed Weight (5% to 50%)*
  * *Specialty Origin Affinity Weight (5% to 50%)*
* **Dashboard shows:** 
  * Instant algorithmic re-weighting and dynamic re-sorting of candidate markets (Japan, South Korea, Australia, Singapore, China Domestic, United States, Germany).
  * Composite attractiveness index (0 to 100 scale), raw sub-scores, and dynamic roadmap tier badges (`Phase 1: Priority Entry`, `Phase 2: Specialty Whole Bean`, `Base: Maintain & Defend`, `Phase 3 / Hold`).
* **User decides:** How resilient the market expansion hierarchy is to shifting boardroom risk tolerances (e.g., verifying whether Japan and South Korea remain top-ranked whether leadership prioritizes immediate margin or long-term growth).

---

## 3. Feature-to-Use-Case Traceability Matrix

Every major section, visual, simulator, and table in the platform directly serves one or more core use cases:

| Section / Tab | Major Component / Visual | Primary Use Case Served | Specific Analytical Role |
|---|---|:---:|---|
| **Header** | Strategic Status Badge & Executive Verdict Banner | Use Case 1 & 4 | Immediate executive synthesis of recommended expansion posture and RCEP tariff dividend. |
| **Tab 1: Executive Scorecard** | 4 Top-Line KPI Cards (Margin Spread, Top Target, TAM, Tariff) | Use Case 1 & 4 | High-level baseline metrics comparing overseas opportunities to domestic status quo. |
| **Tab 1: Executive Scorecard** | Multi-Vector Strategic Readiness Radar Chart | Use Case 1 | Multi-dimensional benchmarking of candidate markets against China domestic baseline. |
| **Tab 1: Executive Scorecard** | Per-Kilogram Unit Economics Margin Breakdown Chart | Use Case 4 | Cost-waterfall visualization showing where margin is created or lost per kilogram. |
| **Tab 1: Executive Scorecard** | Candidate Market Evaluation Summary Table | Use Case 1 | Comprehensive comparison of volume, growth, tariffs, transit times, and recommendations. |
| **Tab 2: Market Attractiveness** | Market Attractiveness 3D Bubble Matrix | Use Case 1 | Scatter analysis evaluating physical market scale vs. growth rate vs. retail price realization. |
| **Tab 2: Market Attractiveness** | Strategic Takeaways Qualitative Deck | Use Case 1 & 5 | Contextual explanations of trade policy dividends, per-capita headroom, and regulatory moats. |
| **Tab 2: Market Attractiveness** | Brand Concentration & Market Saturation (HHI) Chart | Use Case 1 | Evaluates competitive intensity and incumbent dominance to identify whitespace. |
| **Tab 3: Product-Market Fit** | Product-Market Fit Specification Cards | Use Case 2 | Connects agricultural bean attributes to specific foreign consumption occasions and price tiers. |
| **Tab 3: Product-Market Fit** | Channel Fit Suitability Heatmap | Use Case 3 | Scores commercial channel feasibility across target geographies. |
| **Tab 3: Product-Market Fit** | Packaging Format Volume & Mix Breakdown | Use Case 2 | Analyzes Euromonitor packaging unit volume to guide format tooling investments. |
| **Tab 4: Financial Simulator** | Interactive Trade Parameter Slider Controls | Use Case 4 | Allows real-time user manipulation of volume, FOB price, freight, tariffs, and marketing. |
| **Tab 4: Financial Simulator** | Dynamic Landed Cost & Profit Output KPI Cards | Use Case 4 | Real-time calculation of revenue, landed COGS, net operating profit, and net margin %. |
| **Tab 4: Financial Simulator** | Dynamic Scenario Comparative Profit Bar Chart | Use Case 4 | Real-time visual comparison of overseas profit vs. domestic China counterfactual profit. |
| **Tab 4: Financial Simulator** | Algorithmic Decision Verdict Box | Use Case 4 | Dynamic conditional callout (Accretive / Conditional / Dilutive) based on margin spread. |
| **Tab 5: MCDA Decision Matrix** | 5 Strategic Weighting Sliders | Use Case 5 | Captures executive risk preference across growth, margin, tariffs, logistics, and brand affinity. |
| **Tab 5: MCDA Decision Matrix** | Dynamically Ranked Global Entry League Table | Use Case 5 | Real-time algorithmic re-scoring, normalization, and sorting of target countries. |
| **Tab 6: Risks & Objections** | Stakeholder Objection & Mitigation Cards | Governance | Direct refutation of stakeholder pushbacks identified during project scoping. |
| **Tab 6: Risks & Objections** | Regulatory Compliance Roadmap Table | Governance | Actionable customs, phytosanitary, JAS, and EUDR certification gate timelines. |

---

## 4. Dashboard Architecture & User Interface Specification

### 4.1 Visual Design System & Aesthetics
* **Theme:** Dark specialty coffee-house aesthetic engineered with high-contrast, premium data-visualization standards.
* **Palette Tokens:**
  * Base Background: Deep Espresso Charcoal (`#0c0a09`, `#141210`) with radial crema ambient gradients.
  * Surface & Cards: Glassmorphic translucent cards (`rgba(26, 22, 19, 0.85)`) with subtle bronze borders (`rgba(212, 163, 115, 0.15)`).
  * Brand Accents: Crema Tan (`#d4a373`), Amber Gold (`#e9c46a`), Roast Copper (`#c27847`), Emerald Green (`#52b788`), Crimson Alert (`#e76f51`), Oceanic Slate (`#457b9d`).
* **Typography:** Modern Google Fonts pairing: **Outfit** for geometric, high-impact headings and numerical KPI callouts; **Inter** for clean, readable tabular and body data.
* **Layout Structure:** 1440px centered max-width responsive grid; fluid multi-column cards; sticky header; persistent tab navigation bar.

```
+--------------------------------------------------------------------------------------------------+
| HEADER: Brand Eyebrow | Title: Yunnan Coffee Global Entry | Executive Status Badge (CONDITIONAL)  |
+--------------------------------------------------------------------------------------------------+
| NAV TABS: [1. Scorecard] [2. Attractiveness] [3. Product-Market] [4. Simulator] [5. MCDA] [6. Risks]|
+--------------------------------------------------------------------------------------------------+
| STARTING VIEW (TAB 1):                                                                           |
| +----------------------------------------------------------------------------------------------+ |
| | DECISION BANNER: Pursue Phased Expansion (Japan & South Korea First) vs. Defend Domestic     | |
| +----------------------------------------------------------------------------------------------+ |
| | KPI 1: Margin Spread (+9.3%) | KPI 2: Top Target (Japan) | KPI 3: TAM ($15.5B) | KPI 4: Tariff (0%)|
| +----------------------------------------------------------------------------------------------+ |
| | VISUAL 1: Multi-Vector Radar Chart           | VISUAL 2: Per-Kg Economics Margin Waterfall   | |
| +----------------------------------------------------------------------------------------------+ |
| | TABLE 1: Candidate Market Evaluation Matrix (China Baseline, Japan, Korea, Australia, USA)  | |
| +----------------------------------------------------------------------------------------------+ |
+--------------------------------------------------------------------------------------------------+
| FOOTER: DSO Strategic Framework | Course Role Alignment Links (Objectives, Data Fit, Objections) |
+--------------------------------------------------------------------------------------------------+
```

### 4.2 Starting View Specification
When the user accesses the platform, the starting view is **Tab 1: Executive Scorecard**:
* **Top Status Badge:** Displays `CONDITIONAL GO • EAST ASIA FIRST`, signaling the baseline evidence-based recommendation.
* **Executive Decision Banner:** States the central strategic trade-off: China's domestic demand is expanding rapidly (+14.8% CAGR) but domestic price wars compress producer margins to 12.5%; entering RCEP-partner markets unlocks 21–24% net margins with 0% tariffs and 4–6 day shipping.
* **Top KPI Grid:**
  1. *Overseas Net Margin Premium:* `+9.3%` spread (21.8% target APAC avg vs. 12.5% China domestic).
  2. *Top Expansion Target:* `Japan` (Composite score 86.4 / 100; lead format: single-serve drip bags).
  3. *Addressable Phase 1 TAM:* `$15.5 B` (Japan $9.4B + South Korea $6.1B retail coffee).
  4. *RCEP Tariff Barrier:* `0% - 2%` (0% on green bean, preferential tariff on roasted coffee).
* **Two Primary Visuals:** Multi-Vector Strategic Readiness Radar Chart side-by-side with Per-Kilogram Unit Economics Margin Breakdown.
* **Executive Summary Matrix:** Tabular benchmark comparing China against Japan, South Korea, Australia, Singapore, USA, and Germany.

### 4.3 Major Sections & Tabs
1. **Tab 1: Executive Scorecard:** Core strategic synthesis, high-level KPIs, unit economics waterfall, and high-level market evaluation matrix.
2. **Tab 2: Market Attractiveness Deep Dive:** Euromonitor physical market volume distributions, 10-year historical/forecast CAGRs, 3D bubble chart, per-capita consumption analysis, and market concentration (HHI) analysis.
3. **Tab 3: Product-Market Fit & Channels:** Yunnan agricultural specialty profiling (Catimor, Typica, Anaerobic processing), packaging unit volume trends from Euromonitor packaging data, SKU specification cards, and off-trade channel route-to-market heatmap.
4. **Tab 4: Financial Simulator:** Fully interactive landed cost trade simulator with two-way data-bound sliders, live recalculation of gross revenue, landed COGS, net operating profit, margin spread against domestic sales, dynamic profit comparison bar chart, and algorithmic verdict banner.
5. **Tab 5: MCDA Decision Matrix:** Five interactive strategic criteria sliders, real-time recalculation of composite multi-criteria scores, dynamic re-sorting, and categorical roadmap tier assignment.
6. **Tab 6: Strategic Risks & Objections:** Stakeholder pushback resolution cards (addressing domestic growth myths, Yunnan commodity stigma, geopolitical tariffs, and FX volatility) and regulatory compliance milestone roadmap (RCEP Form RCEP, Phytosanitary, JAS, EUDR).

### 4.4 Key Interactive Behaviors
* **Tab Navigation:** Clicking any tab button activates the corresponding panel with smooth fade-in animations and automatically triggers `Chart.js.resize()` to maintain crisp canvas dimensions.
* **Financial Simulator Controls:** Adjusting volume (10–300 MT), FOB price ($15–$50/kg), freight ($0.30–$3.50/kg), tariff (0–35%), or marketing ($10k–$250k) dynamically updates all numerical labels, recalculates landed COGS, re-computes net profit and margin spread, updates the comparative bar chart, and dynamically alters the verdict box styling (Green / Amber / Red).
* **Preset Destination Sync:** Selecting a country dropdown option in the simulator automatically sets realistic baseline presets for that country (e.g., selecting `Japan` sets Tariff to 0%, Freight to $0.80, and Price to $26.00; selecting `United States` sets Tariff to 25%, Freight to $2.20, and Price to $28.00).
* **MCDA Weighting Sliders:** Adjusting any of the five strategic weight sliders triggers instant mathematical re-normalization, re-scores all 7 candidate territories, and re-renders the league table in descending order with animated position badges.
* **Reset Defaults Button:** Reverts MCDA weights instantly to the baseline calibrated corporate posture (25% Growth, 30% Margin, 20% Tariff, 15% Logistics, 10% Affinity).

---

## 5. Metric & Visual Specifications

This section defines the formal logic, data sources, calculation rules, and boundary conditions for every important metric and visualization.  
*(Note: In accordance with specification standards, no Python/JS function implementations are embedded here; descriptions specify required analytical behaviors, equations, and data relationships).*

### 5.1 Metric Specifications

#### Metric M1: 10-Year Category Market Volume CAGR (2015–2025)
* **Question Answered:** Which international markets exhibit sustained, long-term physical volume expansion rather than short-term transient spikes?
* **Source Data & Columns:** `DATA/clean/clean_market_sizes_tidy.csv` (Columns: `Geography`, `Category`, `Data Type`, `Unit`, `Year`, `Total_Market_Volume`).
* **Calculation & Aggregation:**
  $$\text{CAGR}_{2015-2025} = \left( \frac{\text{Total\_Market\_Volume}_{2025}}{\text{Total\_Market\_Volume}_{2015}} \right)^{\frac{1}{2025 - 2015}} - 1$$
  * *Unit Handling:* Computed separately for `Coffee` (`Tonnes`) and `RTD Coffee` (`million litres`).
  * *Missing Data / Edge Cases:* For `India | RTD Coffee`, volume is unobserved (`NaN`) across all years. The engine must check `isna()`; if either baseline or endpoint is missing, return `NaN` and exclude India from RTD averages to prevent division-by-zero or false 0% reporting.
* **Relevant Filters:** `Category == 'Coffee'` or `'RTD Coffee'`; `Data Type == 'Retail Volume'` or `'Off-trade Volume'`; `Year \in [2015, 2025]`.

#### Metric M2: Derived Physical Retail Channel Volume
* **Question Answered:** Exactly how much physical coffee volume (in Tonnes or Litres) flows through each specific retail channel in each target country?
* **Source Data & Columns:** `DATA/clean/clean_market_channels_merged.csv` (Columns: `Geography`, `Category`, `Outlet Type`, `Year`, `Channel_Share_Pct`, `Total_Market_Volume`, `Unit`, `Channel_Volume`).
* **Calculation & Aggregation:**
  $$\text{Channel\_Volume} = \text{Total\_Market\_Volume} \times \left( \frac{\text{Channel\_Share\_Pct}}{100.0} \right)$$
  * *Denominator Check:* `Channel_Share_Pct` represents percentage of off-trade retail volume. Redundant semantic total rows (`Outlet Type == 'Total'`) were audited and dropped during data cleaning to eliminate double counting. Sub-channels (e.g., Supermarkets, Convenience, E-Commerce) sum cleanly to `Retail Offline + Retail E-Commerce`.
* **Relevant Filters:** `Geography \in [Candidate Countries]`, `Category \in ['Coffee', 'RTD Coffee']`, `Year \in [2015..2025]`, `Outlet Type \neq 'Retail Channels'` (when analyzing channel distribution).

#### Metric M3: Packaging Format Unit Volume & Mix Percentage
* **Question Answered:** Which packaging containers dominate off-trade coffee retail sales in the target market, and which formats are expanding most rapidly?
* **Source Data & Columns:** `DATA/clean/clean_pack_type_tidy.csv` (Columns: `Geography`, `Category`, `Packaging Class`, `Pack Type`, `Year`, `Unit_Volume_MUnits`).
* **Calculation & Aggregation:**
  $$\text{Pack\_Format\_Share}_{i, t} = \frac{\text{Unit\_Volume\_MUnits}_{i, t}}{\sum_{k \in \text{All Pack Types}} \text{Unit\_Volume\_MUnits}_{k, t}} \times 100$$
  * *Text Standardization Rule:* Ingested tables have undergone whitespace stripping (`'PET Jars '` standardized to `'PET Jars'`). Total Packaging rows are isolated from granular format rows.
* **Relevant Filters:** `Geography == Target Market`, `Category == 'Coffee'`, `Packaging Class == 'Total'`, `Pack Type \neq 'Total Packaging'`.

#### Metric M4: Landed Export Cost, Net Profit, and Net Margin %
* **Question Answered:** What is the net operating margin and total annual dollar profit of exporting a specified volume of Yunnan coffee to a target destination under current tariffs and freight rates?
* **Source Data & Inputs:** User slider inputs ($V$, $P_{\text{FOB}}$, $C_{\text{freight}}$, $R_{\text{tariff}}$, $B_{\text{mkt}}$) coupled with firm cost baselines:
  * Green bean sourcing cost = $\$7.50 / \text{kg}$
  * Processing, roasting & packaging cost = $\$4.00 / \text{kg}$
  * Base Production Cost per kg ($C_{\text{prod}}$) = $\$11.50 / \text{kg}$
* **Calculation & Aggregation:**
  $$\text{Volume (kg)} = V_{\text{MT}} \times 1,000$$
  $$\text{Total Gross Revenue} = \text{Volume (kg)} \times P_{\text{FOB}}$$
  $$\text{Base Production Cost} = \text{Volume (kg)} \times \$11.50$$
  $$\text{Total Freight \& Insurance} = \text{Volume (kg)} \times C_{\text{freight}}$$
  $$\text{Total Customs Duties} = \text{Total Gross Revenue} \times \left( \frac{R_{\text{tariff}}}{100} \right)$$
  $$\text{Total Landed \& Operating Costs} = \text{Base Production Cost} + \text{Total Freight} + \text{Total Duties} + B_{\text{mkt}}$$
  $$\text{Net Operating Profit} = \text{Total Gross Revenue} - \text{Total Landed \& Operating Costs}$$
  $$\text{Net Operating Margin \%} = \left( \frac{\text{Net Operating Profit}}{\text{Total Gross Revenue}} \right) \times 100$$
* **Relevant Filters:** Filtered by target country trade regime (RCEP, FTA, ChAFTA, Sec 301, EU MFN).

#### Metric M5: Domestic China Counterfactual Benchmark Margin Spread
* **Question Answered:** Does exporting to the selected foreign market generate more operating profit than deploying the identical coffee volume in domestic Chinese tier 1/2 cities?
* **Source Data & Inputs:** Domestic China commercial operational baseline:
  * Domestic wholesale selling price = $\$16.50 / \text{kg}$ (¥118/kg RMB equivalent)
  * Domestic production, roasting & domestic logistics cost = $\$12.00 / \text{kg}$
  * Domestic marketing & channel listing allowance = $\$30,000$ fixed
* **Calculation & Aggregation:**
  $$\text{Domestic Revenue} = \text{Volume (kg)} \times \$16.50$$
  $$\text{Domestic Operating Costs} = (\text{Volume (kg)} \times \$12.00) + \$30,000$$
  $$\text{Domestic Net Profit} = \text{Domestic Revenue} - \text{Domestic Operating Costs}$$
  $$\text{Domestic Net Margin \%} = \left( \frac{\text{Domestic Net Profit}}{\text{Domestic Revenue}} \right) \times 100$$
  $$\Delta \text{Profit (Profit Premium)} = \text{Net Operating Profit}_{\text{Export}} - \text{Domestic Net Profit}$$
  $$\Delta \text{Margin (Margin Spread)} = \text{Net Operating Margin \%}_{\text{Export}} - \text{Domestic Net Margin \%}$$
* **Hurdle Logic:**
  * If $\text{Net Margin} \ge 18\%$ and $\Delta \text{Profit} > 0$: Decision is **`ACCRETIVE OVERSEAS EXPANSION`**.
  * If $\text{Net Margin} \ge 10\%$ and $\text{Net Profit} > 0$: Decision is **`CONDITIONAL / FEASIBLE`**.
  * If $\text{Net Margin} < 10\%$ or $\Delta \text{Profit} \le 0$: Decision is **`MARGIN DILUTIVE / HOLD`**.

#### Metric M6: Composite MCDA Attractiveness Index (0–100 Scale)
* **Question Answered:** Taking into account growth, margin, trade barriers, shipping times, and origin affinity, how do candidate markets rank algorithmically?
* **Source Data & Columns:** Standardized country attribute matrix across 5 normalized sub-scores ($S_{\text{growth}}$, $S_{\text{margin}}$, $S_{\text{tariff}}$, $S_{\text{logistics}}$, $S_{\text{affinity}}$) $\in [0, 100]$.
* **Calculation & Aggregation:**
  $$\text{Composite Score} = \frac{\sum_{j=1}^{5} \left( S_{i, j} \times W_j \right)}{\sum_{j=1}^{5} W_j}$$
  * *Weight Normalization Rule:* The denominator dynamically sums the 5 user-controlled slider weights ($W_j$), ensuring scale invariance even if weights do not sum precisely to 100.
  * *Sorting:* Candidate rows are sorted descending by $\text{Composite Score}$.

---

### 5.2 Visual Specifications

#### Visual V1: Multi-Vector Strategic Readiness (Radar Chart)
* **Question Answered:** How do candidate export markets compare against each other and against China's domestic benchmark across five strategic feasibility pillars?
* **Visual Type:** Multi-dataset Radar Chart (`Chart.js`).
* **Axes (5 Dimensions):**
  1. *Market Growth Potential:* Normalized 5-year CAGR.
  2. *Margin Realization:* Price realization vs. domestic baseline.
  3. *Tariff & Trade Ease:* Inverted duty rate (0% tariff = 100 score).
  4. *Logistics Transit Proximity:* Inverted transit time (2–4 days = 95+ score; 24+ days = 40 score).
  5. *Specialty Origin Affinity:* Consumer openness to single-origin Asian specialty coffee.
* **Datasets:** China Domestic Benchmark (Fill: Slate Blue), Japan (Fill: Emerald Green), South Korea (Fill: Crema Gold), USA (Fill: Crimson Alert).
* **Interactions:** Hover tooltips displaying exact dimension scores; legend click to toggle individual market series.

#### Visual V2: Per-Kilogram Unit Economics Margin Breakdown (Stacked Horizontal Bar Chart)
* **Question Answered:** In each target market, what proportion of the retail price is absorbed by green bean sourcing, processing/roasting, freight, tariffs, distributor margins, and retained producer net profit?
* **Visual Type:** Stacked Horizontal Bar Chart (`Chart.js`).
* **Source Data:** Economic model linking wholesale FOB price, import tariffs, freight, and standard distributor cut (28% in modern retail).
* **Categories Displayed:** China Domestic, Japan (RCEP), South Korea (FTA), Australia (ChAFTA), USA (Sec 301).
* **Segments (Left to Right):** Green Bean Cost ($7.50) + Roasting/Packaging ($4.00) + Ocean Freight ($0.80–$2.20) + Import Tariff ($0.00–$7.00) + Distributor Margin ($5.00–$12.00) + Producer Retained Profit.

#### Visual V3: Market Attractiveness 3D Bubble Matrix
* **Question Answered:** Where are the sweet spots globally combining high growth, high specialty retail prices, and large addressable physical volume?
* **Visual Type:** Bubble Scatter Chart (`Chart.js`).
* **Coordinate Mapping:**
  * **X-Axis:** 5-Year Physical Volume CAGR % (Range: 0% to +16%).
  * **Y-Axis:** Average Specialty Retail Price in USD/kg (Range: $15/kg to $50/kg).
  * **Bubble Radius ($R$):** Total Market Volume TAM (Tonnes / Litres scaled proportionally).
  * **Color Palette:** Green (Priority RCEP), Gold (Conditional Phase 2), Ruby (High Risk / Tariffs), Blue (Domestic China).
* **Interactions:** Hover tooltip displaying Country Name, Exact CAGR %, Specialty Price ($/kg), Total Volume TAM, and Recommended Phase.

#### Visual V4: Retail Channel Fit Heatmap
* **Question Answered:** Which retail channels in each country offer the highest strategic fit for Yunnan coffee products?
* **Visual Type:** Color-graded categorical matrix / Bar grouping.
* **Dimensions:** Rows: Countries (Japan, South Korea, Australia, USA, China); Columns: Outlet Types (Specialty Boutiques, Premium Supermarkets, Convenience Chains, Cross-Border E-Commerce).
* **Scoring Metric:** 1 (Poor Fit / High Barrier) to 5 (Optimal Route).

#### Visual V5: Live Scenario Comparative Profit Bar Chart
* **Question Answered:** Under the specific slider values selected right now, does this export shipment make more or less annual net profit than selling in China?
* **Visual Type:** Dual-column comparative Bar Chart (`Chart.js`).
* **Categories:** `Export Route to Selected Destination` vs. `Domestic China Benchmark`.
* **Dynamic Styling:** Bar color dynamically switches to **Emerald Green** when overseas profit exceeds domestic profit, and switches to **Crimson Red** when overseas profit is lower than domestic profit.

#### Visual V6: Dynamic Algorithmic Candidate Ranking Table
* **Question Answered:** What is the precise order of priority for market entry under current executive weightings?
* **Visual Type:** Interactive Data Table.
* **Columns:** Rank Badge (`#1` to `#7`), Country & Flag, Composite Score, Growth Score, Margin Score, Tariff Ease, Logistics Speed, Specialty Affinity, Roadmap Status Badge.
* **Dynamic Behavior:** Re-sorts instantaneously in JavaScript upon any slider event with zero page reloads.

---

## 6. Build Order & Decoupled Architecture

### 6.1 Architectural Decoupling Rule
To ensure rigorous testing and prevent monolithic regression bugs, the platform is structured into **six strictly decoupled architectural layers**. Each layer has defined inputs, outputs, and independent validation tests.

```
+--------------------------------------------------------------------------------------------------+
| LAYER 6: Governance, Objections & Certification Roadmap (tab-pane-6)                             |
+--------------------------------------------------------------------------------------------------+
| LAYER 5: Decision Engines (Financial Trade Simulator & MCDA Algorithm) (tab-pane-4, 5)           |
+--------------------------------------------------------------------------------------------------+
| LAYER 4: Visualization & Chart.js Controllers (Radar, Bubble, Margin, Channel, SimBar)           |
+--------------------------------------------------------------------------------------------------+
| LAYER 3: UI Framework, Design Tokens & Responsive Glassmorphism Grid                             |
+--------------------------------------------------------------------------------------------------+
| LAYER 2: Analytical Calculation & Aggregation Engine (Volume derivations, CAGR, Currency logic)   |
+--------------------------------------------------------------------------------------------------+
| LAYER 1: Clean Data Ingestion Layer (DATA/clean/ CSVs, Schema validation, Boundary audits)       |
+--------------------------------------------------------------------------------------------------+
```

### 6.2 Sequential Build Order

#### Stage 1: Data Ingestion & Sanitization Layer (`DATA/clean/`)
* **Objective:** Establish verified, clean tabular foundations free of header metadata, trailing spaces, duplicate totals, and corrupted types.
* **Dependencies:** Python 3.10+, `pandas >= 2.0`, `xlrd >= 2.0.1`.
* **Outputs Generated:**
  1. `clean_market_sizes_tidy.csv` (792 tidy rows; 0 duplicate keys).
  2. `clean_retail_channels_tidy.csv` (9,108 tidy rows; redundant 'Total' removed).
  3. `clean_market_channels_merged.csv` (9,108 relational merged rows; physical volume calculated).
  4. `clean_pack_type_tidy.csv` (5,830 rows; standardized packaging text).
* **Decoupled Verification:** Run standalone verification script `clean_data.py` or inspect `sample/cleaned_sample_50.csv`. Confirm zero unmatched merge keys and zero failed numeric conversions.

#### Stage 2: Analytical Aggregation Engine & Mathematical Modeling
* **Objective:** Formulate core aggregation metrics and baseline parameters outside of UI code.
* **Key Operations:**
  * Vectorized 10-year CAGR calculations across geographies and categories.
  * Relational channel volume derivation: $\text{Total Volume} \times (\text{Share} / 100)$.
  * Financial model formulation: Landed COGS, tariff duties, freight impact, and China domestic baseline parameters.
  * MCDA normalization engine: Scaling raw metrics into $[0, 100]$ interval.
* **Decoupled Verification:** Validate output calculations against spreadsheet audit benchmarks (Section 7).

#### Stage 3: UI Framework & Design System Token Implementation
* **Objective:** Construct the semantic HTML5 structure, responsive layout grid, and CSS design tokens in `dashboard.html`.
* **Key Components:**
  * Custom CSS variables for coffee-themed dark palette (`--brand-crema`, `--brand-copper`, `--bg-card`).
  * Responsive container (1440px max-width, fluid grid, sticky header).
  * Tab navigation bar with accessible `role="tab"`, `aria-selected`, and keyboard navigation support.
  * Standardized KPI card components, badge pills, and responsive table containers.
* **Decoupled Verification:** Inspect page layout across viewports (1920px desktop, 1200px laptop, 768px tablet) ensuring zero horizontal overflow and proper semantic hierarchy.

#### Stage 4: Core Visualizations & Chart.js Controllers
* **Objective:** Instantiate all analytical visual charts using Chart.js with responsive canvas bindings.
* **Key Visuals Built:**
  1. `radarChart`: 5-axis readiness radar for candidate markets.
  2. `marginChart`: Stacked horizontal bar chart for per-kg unit economics.
  3. `bubbleChart`: 3D bubble chart for market attractiveness (Growth vs. Price vs. Volume).
  4. `concentrationChart`: Incumbent market share and HHI index.
  5. `channelFitChart`: Horizontal grouped bar chart for retail channel fit.
  6. `simComparisonChart`: Dynamic comparative profit bar chart in the financial simulator.
* **Decoupled Verification:** Verify chart rendering, tooltip data precision, axis labeling, and resize triggers on window resize and tab switch events.

#### Stage 5: Interactive Simulation & Reactive State Engines
* **Objective:** Implement two-way data-bound interactive simulation logic in vanilla JavaScript.
* **Key Modules:**
  * `recalculateSimulator()`: Listens to input events across 5 trade sliders; computes landed COGS, profit, and margin; updates UI numerical readouts; dynamically toggles verdict card states.
  * Country selector synchronization: Updates slider defaults when the target country changes.
  * `updateMCDA()`: Listens to 5 criteria sliders; re-calculates composite weighted scores; re-sorts candidate array; dynamically regenerates table DOM elements.
* **Decoupled Verification:** Test boundary values on all sliders (min, max, step increments) ensuring zero `NaN` outputs and correct verdict class toggles.

#### Stage 6: Governance, Objections & Strategic Roadmap Layer
* **Objective:** Embed strategic safeguards, stakeholder objection refutations, and regulatory compliance gates into Tab 6.
* **Key Elements:**
  * Structured risk cards addressing domestic growth, origin pedigree stigma, US tariffs, and foreign exchange risk.
  * Compliance milestone table mapping mandatory trade documentation (RCEP Form RCEP, Phytosanitary inspection, JAS Organic, EUDR GPS mapping).
* **Decoupled Verification:** Cross-reference risk statements against `objections.md` and regulatory requirements against official customs guidelines.

---

## 7. Concrete Acceptance Checks & Quality Gates

The following test cases define explicit, verifiable acceptance criteria. Each check specifies test inputs, expected behavior, verification method, and tolerances.

### Acceptance Check AC-1: Data Ingestion & Unobserved Value Integrity (India RTD Case)
* **Target Component:** Clean Data Pipeline (`DATA/clean/clean_market_sizes_tidy.csv` & `clean_market_channels_merged.csv`).
* **Input Condition:** Filter records for `Geography == 'India'`, `Category == 'RTD Coffee'`, `Years \in [2015..2025]`.
* **Expected Output:**
  * `Total_Market_Volume` must strictly be `NaN` / empty string in CSV (NOT converted to `0.0`).
  * `clean_market_channels_merged.csv` must report `Channel_Volume` as `NaN` / empty string.
  * Regional aggregation functions must ignore India RTD without failing or skewing Asia-Pacific averages.
* **Verification Command:**
  ```powershell
  python -c "import pandas as pd; df=pd.read_csv('DATA/clean/clean_market_sizes_tidy.csv'); india_rtd=df[(df['Geography']=='India')&(df['Category']=='RTD Coffee')]; assert india_rtd['Total_Market_Volume'].isna().all(), 'FAIL: India RTD not NaN'; print('PASS: India RTD unobserved integrity verified.')"
  ```
* **Tolerance:** Exactly 11 out of 11 records must be `NaN`.

### Acceptance Check AC-2: Semantic Total De-Duplication in Retail Channels
* **Target Component:** Retail Channel Cleaning Engine (`clean_retail_channels_tidy.csv`).
* **Input Condition:** In raw `Retail channels.xls`, both `Outlet Type == 'Retail Channels'` and `Outlet Type == 'Total'` were present for every geography/category/year.
* **Expected Output:**
  * Exactly 396 redundant tidy rows corresponding to `Outlet Type == 'Total'` must be removed.
  * Total tidy rows in `clean_retail_channels_tidy.csv` must equal **exactly 9,108 rows** (down from 9,504 raw melted rows).
  * For any geography/category/year, the sum of non-redundant individual channels must reconcile to `Retail Channels` (100.0%) within 0.1% rounding tolerance.
* **Verification Command:**
  ```powershell
  python -c "import pandas as pd; df=pd.read_csv('DATA/clean/clean_retail_channels_tidy.csv'); assert len(df)==9108, f'FAIL: Expected 9108, got {len(df)}'; assert not (df['Outlet Type']=='Total').any(), 'FAIL: Total still present'; print('PASS: Channel duplicate removal verified.')"
  ```
* **Tolerance:** Exactly 0 rows with `Outlet Type == 'Total'` permitted.

### Acceptance Check AC-3: Relational Merge Key Completeness & Volume Preservation
* **Target Component:** Multi-Table Relational Merge (`clean_market_channels_merged.csv`).
* **Input Condition:** Ingest `clean_market_sizes_tidy.csv` (Volume records) and `clean_retail_channels_tidy.csv`. Merge on `['Geography', 'Category', 'Year']`.
* **Expected Output:**
  * Unmatched keys on left or right: **0**.
  * Total rows generated: **Exactly 9,108 rows**.
  * Hand-calculated record verification: China Coffee 2025 Supermarkets (`Channel_Share_Pct = 20.5%`, `Total_Market_Volume = 61,314.5 Tonnes`):
    $$\text{Channel\_Volume} = 61,314.5 \times 0.205 = 12,569.4725 \text{ Tonnes}$$
* **Verification Command:**
  ```powershell
  python -c "import pandas as pd; df=pd.read_csv('DATA/clean/clean_market_channels_merged.csv'); r=df[(df['Geography']=='China')&(df['Category']=='Coffee')&(df['Outlet Type']=='Supermarkets')&(df['Year']==2025)].iloc[0]; assert abs(r['Channel_Volume'] - 12569.4725) < 0.01, f'FAIL: {r[\"Channel_Volume\"]}'; print('PASS: Merge volume derivation verified.')"
  ```
* **Tolerance:** Discrepancy $< 0.01$ Tonnes.

### Acceptance Check AC-4: Interactive Financial Simulator Calculation & Hurdle Logic
* **Target Component:** Financial Simulator Engine (`dashboard.html` -> `recalculateSimulator()`).
* **Test Case A (Accretive Scenario — Japan Default):**
  * Inputs: Target Country = Japan, Volume = 50 MT (50,000 kg), FOB Price = $26.00/kg, Freight = $0.80/kg, Tariff = 0%, Marketing = $60,000.
  * Expected Mathematical Outputs:
    * Gross Revenue = $50,000 \times 26.00 = \$1,300,000$
    * Base Production Cost = $50,000 \times 11.50 = \$575,000$
    * Total Freight = $50,000 \times 0.80 = \$40,000$
    * Total Tariff Duties = $0
    * Total Landed Costs = $\$575,000 + \$40,000 + \$0 + \$60,000 = \$675,000$
    * Net Operating Profit = $\$1,300,000 - \$675,000 = \$625,000$
    * Net Operating Margin % = $(\$625,000 / \$1,300,000) \times 100 = 48.1\%$
    * Domestic China Profit = $(50,000 \times 16.50) - (50,000 \times 12.00 + 30,000) = \$825,000 - \$630,000 = \$195,000$ (Margin: 23.6%)
    * Profit Delta ($\Delta \text{Profit}$) = $\$625,000 - \$195,000 = +\$430,000$
    * Verdict Title: `STRATEGIC VERDICT: HIGHLY ACCRETIVE EXPORT TO JAPAN`
* **Test Case B (Dilutive Scenario — US Punitive Tariff Barrier):**
  * Inputs: Target Country = United States, Volume = 50 MT, FOB Price = $22.00/kg, Freight = $2.50/kg, Tariff = 25%, Marketing = $100,000.
  * Expected Outputs:
    * Gross Revenue = $\$1,100,000$
    * Duties = $\$1,100,000 \times 0.25 = \$275,000$
    * Landed Costs = $\$575,000 + \$125,000 + \$275,000 + \$100,000 = \$1,075,000$
    * Net Operating Profit = $\$25,000$ (Net Margin: 2.27%)
    * Profit Delta vs. Domestic ($195k) = $-\$170,000$
    * Verdict Title: `STRATEGIC VERDICT: MARGIN DILUTIVE / HOLD`
* **Tolerance:** Dollar values exact to nearest integer; margins exact to $\pm 0.1\%$.

### Acceptance Check AC-5: MCDA Normalization & Dynamic Ranking Stability
* **Target Component:** MCDA Scoring Engine (`dashboard.html` -> `updateMCDA()`).
* **Test Case A (Default Baseline Weights):**
  * Weights: Growth = 25, Margin = 30, Tariff = 20, Logistics = 15, Affinity = 10 (Sum = 100).
  * Expected Top 2 Ranks:
    * Rank 1: **Japan** (Composite Score: **86.4**)
    * Rank 2: **South Korea** (Composite Score: **86.0**)
  * Expected Lowest Ranks:
    * Rank 6: **United States** (Composite Score: **57.7**)
    * Rank 7: **Germany** (Composite Score: **50.5**)
* **Test Case B (Scale Invariance Check):**
  * Double all slider weights: Growth = 50, Margin = 60, Tariff = 40, Logistics = 30, Affinity = 20 (Sum = 200).
  * Expected Behavior: Composite scores must remain **100% identical** ($86.4, 86.0, \dots$) because the algorithm divides by the dynamic sum of weights ($\sum W_j$).
* **Tolerance:** Composite score deviation $< 0.05$ points.

### Acceptance Check AC-6: Cross-Browser Responsive Rendering & Accessibility
* **Target Component:** Web Interface (`dashboard.html`).
* **Checks:**
  1. *W3C Semantic Validation:* Verify presence of `<h1>`, `<header>`, `<main>`, `<section>`, `<footer>`, and valid `ARIA` attributes (`role="tab"`, `role="tabpanel"`, `aria-selected`).
  2. *Responsive Layout:* Viewport testing at 375px (mobile), 768px (tablet), 1280px (laptop), and 1920px (desktop) — zero broken layouts or horizontal window scrollbars.
  3. *Console Audit:* Zero uncaught JavaScript runtime errors or 404 network request failures upon initial load and tab navigation.
* **Tolerance:** 0 console errors permitted.

---

## 8. Summary of Code Base & File Organization

The analytical logic and user interface are strictly separated across the repository structure:

```
cpg-global-entry-strategy/
├── BUILD_SPEC.md                      # [THIS FILE] Revised vision, use cases & build specification
├── README.md                          # Repository overview, team roster, submission metadata
├── dashboard.html                     # Complete interactive decision-support platform (Layers 3-6)
├── clean_data.py                      # Standalone automated data cleaning pipeline (Layers 1-2)
├── Datacleaner.ipynb                  # Interactive Jupyter cleaning inspection notebook
├── requirements.txt                   # Environment dependencies (pandas, xlrd, numpy)
├── DATA/
│   ├── Market Sizes.xls               # Raw Euromonitor category market volumes & values
│   ├── Retail channels.xls            # Raw Euromonitor channel percentage shares
│   ├── Pack type.xls                  # Raw Euromonitor packaging container format unit volumes
│   ├── Pack Size.xls                  # Raw Euromonitor packaging capacity unit volumes
│   └── clean/
│       ├── clean_market_sizes_tidy.csv          # Standardized tidy market size panel
│       ├── clean_market_sizes_wide.csv          # Clean numeric wide format
│       ├── clean_retail_channels_tidy.csv       # Tidy channel shares (Total removed)
│       ├── clean_retail_channels_wide.csv       # Clean numeric channel wide format
│       ├── clean_market_channels_merged.csv     # Relational physical channel volume dataset
│       └── clean_pack_type_tidy.csv             # Standardized packaging container format panel
└── sample/
    └── cleaned_sample_50.csv          # Representative 50-row audit sample for grading verification
```
