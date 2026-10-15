# BUILD_SPEC.md — CPG Global Entry Strategy Decision Platform

**Course:** DSO 576 — Decision-Support Analytics & CPG Global Entry Strategy  
**Deliverable:** Revised Vision & Build Specification (`BUILD_SPEC.md`)  
**Student Name:** Benjamin (Ru Yi) Cai (`betakappa123`)  
**Team Members:** Wendy S (`WendyS-28`) & Benjamin Cai (`betakappa123`)  
**Repository Branch:** `main`  
**Primary Artifact:** [`dashboard.html`](dashboard.html)  
**Data Scope Constraint:** Strictly 100% grounded in local repository datasets (`DATA/` & `DATA/clean/`) without external unverified dependencies.

---

## 1. Revised Vision & Context

### 1.1 Specific User Persona
The primary user is the **Commercial Strategy Director / VP of Global Expansion** at a specialty coffee enterprise originating from **Yunnan Province, China** (e.g., an integrated Arabica estate and roastery in Pu'er or Baoshan operating commercial green bean milling, roasting lines, and packaging facilities).

Secondary stakeholders include the **Head of Sales & Distribution** (evaluating retail partner channels and modern trade access), the **Director of Packaging & Production Engineering** (allocating capital between pouch packing lines, canning equipment, and carton forming), and the **Executive Leadership Team** (evaluating whether to allocate capital toward overseas export expansion vs. defending domestic Chinese retail share).

### 1.2 Core Business Decision
The user faces a concrete strategic question:  
**Which international markets, retail channels, product categories, and packaging formats offer the highest physical volume potential and sustained growth velocity for a Yunnan coffee enterprise looking to expand beyond domestic China?**

The decision decomposes into four empirical choices fully supported by the local data:
1. **Target Market Prioritization (Vision A):** Which overseas markets exhibit large physical volume scale and structural growth velocity for Coffee and RTD Coffee, vs. markets that are contracting or stagnant?
2. **Category Portfolio Selection:** Should the firm lead international expansion with packaged roast & ground coffee (`Coffee`, in Tonnes) or ready-to-drink liquid coffee (`RTD Coffee`, in Million Litres)?
3. **Retail Route-to-Market Selection (Vision B):** Which specific off-trade retail channels (e.g., Convenience Stores, Supermarkets, Retail E-Commerce, Hypermarkets, Discounters) command the largest physical volume throughput and fastest adoption in each destination market?
4. **Packaging Format & Size Strategy (Vision C):** Which container formats (e.g., Stand-Up Pouches, Flexible Aluminium/Plastic, Glass Jars, Beverage Cans) and capacity sizes (e.g., single-serve $\le 10\text{g}$, retail $100\text{g} - 250\text{g}$, bulk $> 500\text{g}$, or $250\text{ml}$) represent the dominant consumer purchasing unit in each target country?

### 1.3 Why the Tool Improves Current Practice
* **The Status Quo:** Currently, CPG commercial teams analyze export markets using disconnected, static spreadsheet exports and fragmented trade reports:
  * *Disparate Currency Metrics:* Raw Euromonitor exports report country retail values in local currencies without annual FX alignment (e.g., Japan in `JPY billion`, China in `CNY million`, Germany in `EUR million`), causing severe scale distortions when non-technical managers compare country rows.
  * *Disconnection Between Volume and Channels:* Market sizing reports state total national volume, but channel share reports only state percentages. Commercial teams struggle to quickly quantify the *physical volume* flowing through a specific channel (e.g., knowing that Supermarkets represent 46.4% of Japan's coffee market does not immediately tell an executive how many physical Tonnes that represents relative to China's e-commerce volume).
  * *Packaging Format Blindness:* Product teams frequently design packaging (e.g., rigid glass jars or bulk bags) without verifying whether the target market's off-trade retail volume has already shifted to stand-up pouches or single-serve packs.
* **The Platform Improvement:** The platform integrates physical market volumes (`Tonnes` and `million litres`), 11-year historical and forecast CAGRs (2015–2025), derived channel physical volumes (9,108 observations across 23 outlet types), 37 packaging container formats (5,830 observations), and granular capacity size breakdowns into a single interactive decision engine. It eliminates currency distortions by prioritizing physical volume consumption and directly computes channel throughput to guide route-to-market contracts.

### 1.4 Phase 1 Vision vs. Revised Vision Evolution
* **Phase 1 Conception (`project-start.md`):** Initially scoped three separate, disconnected candidate visions:
  * *Candidate Vision A:* Whether to expand overseas (macro country evaluation).
  * *Candidate Vision B:* Which retail channel to select in APAC (channel comparison).
  * *Candidate Vision C:* Which packaging format to adopt (packaging format comparison).
* **The Revised Vision (100% Local Data Grounded):** The three candidate visions are synthesized into an **integrated, sequential commercial go-to-market pipeline** powered entirely by the four local datasets in `DATA/clean/`:
  * **Step 1 (Macro Screening — Vision A):** Filter candidate countries by physical volume scale and 10-year volume CAGR from [clean_market_sizes_tidy.csv](DATA/clean/clean_market_sizes_tidy.csv).
  * **Step 2 (Category Balance):** Compare growth divergence between Coffee (Tonnes) and RTD Coffee (Million Litres).
  * **Step 3 (Channel Execution — Vision B):** Identify the primary volume-driving retail channel using derived `Channel_Volume` from [clean_market_channels_merged.csv](DATA/clean/clean_market_channels_merged.csv).
  * **Step 4 (Packaging Strategy — Vision C):** Select container format and pack capacity using [clean_pack_type_tidy.csv](DATA/clean/clean_pack_type_tidy.csv) and [Pack Size.xls](DATA/Pack%20Size.xls).

---

## 2. Core Use Cases

Each use case adheres strictly to the decision-support interaction pattern:  
$$\text{User selects/inputs} \longrightarrow \text{Dashboard shows} \longrightarrow \text{User decides}$$

```
+--------------------------+       +--------------------------+       +--------------------------+
|   User Selects/Inputs    | ----> |     Dashboard Shows      | ----> |       User Decides       |
| (Filters, Dropdowns)     |       | (Empirical Metrics/Charts|       | (Market, Channel, Format)|
+--------------------------+       +--------------------------+       +--------------------------+
```

### Use Case 1: Cross-Country Market Volume & Growth Prioritization
* **User selects/inputs:** Product Category (`Coffee` vs. `RTD Coffee`), Time Horizon (`2015–2025` or `2020–2025`), and Geographic Comparison Group (e.g., `Asia Pacific`, `Western Europe`, `North America`, or focal countries).
* **Dashboard shows:**
  * **Market Volume & Growth Scatter Matrix:** (X-axis: 10-Year Volume CAGR %; Y-axis: Absolute Volume Change in Tonnes / Litres; Bubble Size: 2025 Total Market Volume).
  * **Market Prioritization Scorecard:** Table reporting 2015 Volume, 2020 Volume, 2025 Forecast Volume, 10-year CAGR %, and Growth Velocity Tier (`High Growth Expansion`, `Mature Stable Scale`, `Contracting / Low Priority`).
* **User decides:** Which overseas target markets have expanding volume demand (e.g., Thailand coffee at +2.85% CAGR and Asia Pacific at +1.90% CAGR) vs. markets experiencing structural volume contraction (e.g., USA coffee at -0.62% CAGR).

### Use Case 2: Category Mix & Expansion Velocity (Packaged Coffee vs. RTD Coffee)
* **User selects/inputs:** Target Geography (e.g., `China`, `Japan`, `Thailand`, `Australia`, `USA`, `Germany`).
* **Dashboard shows:**
  * **Category Volume Trajectory Line Chart:** Tracing Coffee (Tonnes) and RTD Coffee (Million Litres) from 2015 to 2025.
  * **Comparative Category Metrics:** 10-Year CAGR of Coffee vs. 10-Year CAGR of RTD Coffee.
  * **Category Dominance Ratio:** Relative scale and growth divergence between packaged coffee and ready-to-drink coffee.
* **User decides:** Whether to enter the destination market with packaged roast & ground coffee, liquid RTD coffee, or a dual-category launch (e.g., recognizing that Japan is the dominant RTD market with 2,846.4M Litres, while Australia exhibits massive RTD growth at +17.14% CAGR).

### Use Case 3: Off-Trade Retail Channel Route-to-Market Selection
* **User selects/inputs:** Target Geography (e.g., `Japan` vs. `China`), Product Category (`Coffee` vs. `RTD Coffee`), and Year (`2015` vs. `2020` vs. `2025`).
* **Dashboard shows:**
  * **Derived Physical Channel Volume Bar Chart:** Absolute volume (Tonnes / Litres) flowing through each of the 23 retail outlet types from [clean_market_channels_merged.csv](DATA/clean/clean_market_channels_merged.csv).
  * **Channel Share Shift Waterfall:** 10-year percentage point change in volume share ($\Delta \text{Share}_{\text{pts}} = \text{Share}_{2025} - \text{Share}_{2015}$).
  * **Retail Channel Cluster Breakdown:** Volume grouped into Modern Grocery (Supermarkets, Hypermarkets, Discounters), Convenience Retailers, Retail E-Commerce, and Traditional Grocers.
* **User decides:** Which retail channel partner to prioritize for commercial distribution contracts (e.g., contracting with Japanese convenience store chains like Lawson/7-Eleven which account for 620.5M Litres of RTD, vs. focusing on Retail E-Commerce in China which grew from 10.8% to 46.7% volume share).

### Use Case 4: Packaging Container Format Prioritization
* **User selects/inputs:** Target Geography (e.g., `China`, `Japan`, `Western Europe`), Product Category (`Coffee` vs. `RTD Coffee`), and Year (`2015–2025`).
* **Dashboard shows:**
  * **Packaging Container Mix Breakdown:** Unit volume (Million Units) and percentage share across container formats (Flexible Packaging, Stand-Up Pouches, Glass Jars, Metal Tins, Beverage Cans, PET Jars, Liquid Cartons) from [clean_pack_type_tidy.csv](DATA/clean/clean_pack_type_tidy.csv).
  * **10-Year Packaging Format Growth Leaderboard:** Fastest expanding container formats by unit volume CAGR.
  * **Packaging Mix Donut Chart:** Visual distribution of packaging formats in the selected market.
* **User decides:** Which packaging machinery and container inventory to invest capital in for export runs (e.g., investing in Stand-Up Pouches and Flexible Aluminium/Plastic for packaged coffee, which represent over 70% of global packaging units).

### Use Case 5: Pack Size & SKU Capacity Optimization
* **User selects/inputs:** Target Geography (e.g., `China`, `Japan`, `USA`), Category (`Coffee`), and Packaging Type (`Flexible Packaging`, `Stand-Up Pouches`, or `Total Packaging`).
* **Dashboard shows:**
  * **Granular Pack Capacity Distribution:** Unit volume (Million Units) across standard gram capacities (`10g`, `100g`, `250g`, `500g`, `1000g`) from [Pack Size.xls](DATA/Pack%20Size.xls).
  * **Dominant Pack Size Leaderboard:** Identifying the #1 and #2 most purchased package sizes by consumers in that market.
* **User decides:** Exactly what gram weight capacity SKU to manufacture for export (e.g., producing 10g single-serve sachets vs. 250g retail bags vs. 1kg bulk bags) to align with observed shopper buying patterns.

### Use Case 6: Empirical Multi-Dimensional Attractiveness Index (EMAI)
* **User selects/inputs:** Five strategic weighting sliders on the empirical multi-dimensional scoring engine:
  * *Market Scale Weight ($w_{\text{scale}}$, 0% to 40%)* — 2025 Physical Market Volume
  * *Volume Growth Velocity Weight ($w_{\text{growth}}$, 0% to 40%)* — 10-Year Volume CAGR
  * *Digital Channel Readiness Weight ($w_{\text{digital}}$, 0% to 30%)* — 2025 Retail E-Commerce Volume Share
  * *Channel Diversification Weight ($w_{\text{channel}}$, 0% to 30%)* — Inverse Channel Herfindahl Concentration
  * *Packaging Modernity Weight ($w_{\text{pack}}$, 0% to 30%)* — Stand-Up Pouch & Modern Format Share
* **Dashboard shows:**
  * Instant algorithmic re-weighting and dynamic ranking of all 10 focal countries based **strictly on empirical local data**.
  * Composite attractiveness index (0 to 100 scale), raw empirical sub-scores, and dynamic roadmap tier badges (`Phase 1: Priority Expansion`, `Phase 2: Targeted Entry`, `Base: Domestic Core`, `Phase 3: Watchlist`).
* **User decides:** How target market rankings re-order under shifting commercial strategies (e.g., prioritizing rapid volume growth vs. targeting mature, high-scale markets with advanced e-commerce infrastructure).

---

## 3. Feature-to-Use-Case Traceability Matrix

Every feature, section, chart, and table in the platform is directly powered by local data and maps to an explicit use case:

| Section / Tab | Component / Visual | Primary Use Case | Exact Local Data Source |
|---|---|:---:|---|
| **Header** | Strategic Status Badge & Category Mode Selector | Use Case 1 & 2 | User toggle between `Coffee` and `RTD Coffee` across [clean_market_sizes_tidy.csv](DATA/clean/clean_market_sizes_tidy.csv). |
| **Tab 1: Market Prioritization** | 4 Summary KPI Cards (World TAM, Fast Growth Leader, Digital Shift Leader, Top Pack Format) | Use Case 1 | Aggregations over [clean_market_sizes_tidy.csv](DATA/clean/clean_market_sizes_tidy.csv), [clean_retail_channels_tidy.csv](DATA/clean/clean_retail_channels_tidy.csv), and [clean_pack_type_tidy.csv](DATA/clean/clean_pack_type_tidy.csv). |
| **Tab 1: Market Prioritization** | Market Volume & Growth Scatter Matrix (Bubble Chart) | Use Case 1 | X: 10-Yr CAGR, Y: Volume Delta, Size: 2025 Volume from [clean_market_sizes_tidy.csv](DATA/clean/clean_market_sizes_tidy.csv). |
| **Tab 1: Market Prioritization** | Country Prioritization Scorecard Table | Use Case 1 | Tabular 2015, 2020, 2025 volume and CAGR across 18 geographies from [clean_market_sizes_tidy.csv](DATA/clean/clean_market_sizes_tidy.csv). |
| **Tab 2: Category Dynamics** | Coffee vs. RTD Coffee 11-Year Trajectory Line Chart | Use Case 2 | Time-series volume (2015–2025) comparing categories from [clean_market_sizes_tidy.csv](DATA/clean/clean_market_sizes_tidy.csv). |
| **Tab 2: Category Dynamics** | Category Growth Divergence Bar Chart | Use Case 2 | Side-by-side 10-year CAGR for Coffee vs. RTD Coffee across focal markets. |
| **Tab 2: Category Dynamics** | Category Dominance Ratio Table | Use Case 2 | Ratio of RTD Litres to Coffee Tonnes per geography. |
| **Tab 3: Channel Route-to-Market** | Derived Physical Channel Volume Bar Chart | Use Case 3 | Derived physical volume (Tonnes / Litres) per outlet type from [clean_market_channels_merged.csv](DATA/clean/clean_market_channels_merged.csv). |
| **Tab 3: Channel Route-to-Market** | 11-Year Channel Shift Trajectory Stacked Area Chart | Use Case 3 | Annual channel percentage shares (2015–2025) from [clean_retail_channels_tidy.csv](DATA/clean/clean_retail_channels_tidy.csv). |
| **Tab 3: Channel Route-to-Market** | Channel Cluster Distribution Matrix (Modern vs. Digital vs. Traditional) | Use Case 3 | Sum of channel volumes across grouped outlet types from [clean_market_channels_merged.csv](DATA/clean/clean_market_channels_merged.csv). |
| **Tab 4: Packaging Formats** | Packaging Container Format Unit Volume Bar Chart | Use Case 4 | Unit volume (Million Units) across 37 pack types from [clean_pack_type_tidy.csv](DATA/clean/clean_pack_type_tidy.csv). |
| **Tab 4: Packaging Formats** | 10-Year Packaging Growth Leaderboard | Use Case 4 | Unit volume CAGR (2015–2025) by container format from [clean_pack_type_tidy.csv](DATA/clean/clean_pack_type_tidy.csv). |
| **Tab 4: Packaging Formats** | Container Mix Percentage Donut Chart | Use Case 4 | Percentage share of container formats per target country. |
| **Tab 5: Pack Size Optimization** | Granular Pack Capacity Distribution Histogram | Use Case 5 | Unit volume by capacity (<50g, 100g, 250g, 500g, 1000g) from [Pack Size.xls](DATA/Pack%20Size.xls). |
| **Tab 5: Pack Size Optimization** | Top Pack Sizes by Market Leaderboard Table | Use Case 5 | Top 3 pack capacities by unit volume per country from [Pack Size.xls](DATA/Pack%20Size.xls). |
| **Tab 6: Empirical Attractiveness Index** | 5 Empirical Weighting Sliders | Use Case 6 | Interactive controls for Scale, Growth, Digital, Diversity, and Modern Packaging weights. |
| **Tab 6: Empirical Attractiveness Index** | Dynamically Ranked Empirical Candidate League Table | Use Case 6 | Real-time sorting and normalized composite scoring calculated 100% from local tables. |

---

## 4. Dashboard Architecture & User Interface Specification

### 4.1 Visual Design System & Aesthetics
* **Theme:** Professional CPG analytics dark theme (`--bg-base: #0c0a09`, `--bg-card: rgba(26, 22, 19, 0.85)`, `--brand-crema: #d4a373`, `--brand-green-light: #52b788`).
* **Typography:** Modern Google Fonts pairing: **Outfit** for structural headings and KPI numbers; **Inter** for clean tabular data and micro-copy.
* **Layout Structure:** Centered 1440px responsive container, persistent header with category mode toggle, sticky tab navigation bar, dynamic data-driven panels.

```
+--------------------------------------------------------------------------------------------------+
| HEADER: Brand Eyebrow | Title: Yunnan Coffee Global Entry Analytics | Category Toggle [Coffee/RTD]|
+--------------------------------------------------------------------------------------------------+
| NAV TABS: [1. Market Sizing] [2. Category Mix] [3. Retail Channels] [4. Packaging] [5. Sizes] [6. Index] |
+--------------------------------------------------------------------------------------------------+
| STARTING VIEW (TAB 1):                                                                           |
| +----------------------------------------------------------------------------------------------+ |
| | KPI 1: 2025 TAM (6.18M Tonnes) | KPI 2: Top Growth (Thailand +2.85%) | KPI 3: E-Com Surge (46.7%) | KPI 4: Top Pack (Flexible 74.5%) | |
| +----------------------------------------------------------------------------------------------+ |
| | VISUAL 1: Market Volume vs. CAGR Bubble Matrix | TABLE 1: Country Prioritization Scorecard   | |
| +----------------------------------------------------------------------------------------------+ |
+--------------------------------------------------------------------------------------------------+
| FOOTER: DSO 576 Module 7 • Empirical Decision Platform • Sourced 100% from Local Data           |
+--------------------------------------------------------------------------------------------------+
```

### 4.2 Starting View Specification
When the user accesses the platform, the starting view is **Tab 1: Market Prioritization & Volume Growth**:
* **Header Controls:** Category selector defaulted to `Coffee`, geographic scope defaulted to `All Focal Markets`.
* **Top KPI Grid (Calculated from Local Data):**
  1. *2025 Total World Volume:* `6,175,791.8 Tonnes` (from `clean_market_sizes_tidy.csv`).
  2. *Top Growth Target Market:* `Thailand` (`+2.85%` 10-year volume CAGR; expanding from 67.3k to 89.1k Tonnes).
  3. *Leading Digital Channel Market:* `China` (`46.7%` E-commerce share in 2025, expanding from 10.8% in 2015).
  4. *Dominant Packaging Format:* `Flexible Packaging` (`100,033.8 Million Units` globally in 2025; 74.5% share).
* **Two Primary Layout Elements:**
  * Market Attractiveness Bubble Matrix (10-Yr Volume CAGR % vs. Absolute Volume Expansion in Tonnes, bubble radius = 2025 Volume).
  * Country Market Prioritization Scorecard with 2015, 2020, 2025 volume and CAGR tiers.

### 4.3 Major Sections & Tabs
1. **Tab 1: Market Prioritization & Volume Growth:** Macro volume sizing, 10-year historical/forecast CAGRs, growth vs. volume bubble matrix, and country tiering scorecard.
2. **Tab 2: Category Dynamics (Coffee vs. RTD Coffee):** Dual-category volume comparisons, growth divergence analysis, and category dominance ratios across focal markets.
3. **Tab 3: Retail Route-to-Market & Channel Shifts:** Physical channel volumes (Tonnes / Litres) across 23 outlet types, 11-year channel share shift trajectories, and channel cluster analysis (Modern vs. Digital vs. Traditional).
4. **Tab 4: Packaging Container Formats:** Off-trade packaging container volumes (Million Units) across 37 pack types, 10-year format growth leaderboards, and format share distribution.
5. **Tab 5: Pack Size & SKU Capacity Optimization:** Capacity distribution across standard gram and millilitre sizes from `Pack Size.xls`, identifying high-volume SKU sizes per destination market.
6. **Tab 6: Empirical Attractiveness Index (EMAI):** Interactive five-criteria weighting engine scoring candidate countries entirely on empirical local attributes (Scale, Growth, Digital Readiness, Channel Diversity, Packaging Modernity).

---

## 5. Metric & Visual Specifications

### 5.1 Metric Specifications

#### Metric M1: 10-Year Category Volume CAGR (2015–2025)
* **Question Answered:** Which international markets exhibit sustained, long-term physical volume expansion rather than short-term transient spikes?
* **Source Data & Columns:** [clean_market_sizes_tidy.csv](DATA/clean/clean_market_sizes_tidy.csv) (`Geography, Category, Data Type, Unit, Year, Total_Market_Volume`).
* **Calculation & Aggregation:**
  $$\text{CAGR}_{2015-2025} = \left( \frac{\text{Total\_Market\_Volume}_{2025}}{\text{Total\_Market\_Volume}_{2015}} \right)^{\frac{1}{10}} - 1$$
  $$\Delta \text{Volume}_{2015-2025} = \text{Total\_Market\_Volume}_{2025} - \text{Total\_Market\_Volume}_{2015}$$
  * *Unit Handling:* Computed separately for `Coffee` (`Tonnes`) and `RTD Coffee` (`million litres`).
  * *Boundary Condition:* For `India | RTD Coffee`, volume is unobserved (`NaN`) across all years. The engine checks `isna()`; if baseline or endpoint is missing, return `NaN` and exclude from regional averages to prevent division-by-zero.
* **Relevant Filters:** `Category \in ['Coffee', 'RTD Coffee']`, `Year \in [2015, 2025]`.

#### Metric M2: Derived Physical Retail Channel Volume
* **Question Answered:** Exactly how much physical coffee volume (in Tonnes or Litres) flows through each specific retail channel in each target country?
* **Source Data & Columns:** [clean_market_channels_merged.csv](DATA/clean/clean_market_channels_merged.csv) (`Geography, Category, Outlet Type, Year, Channel_Share_Pct, Total_Market_Volume, Unit, Channel_Volume`).
* **Calculation & Aggregation:**
  $$\text{Channel\_Volume} = \text{Total\_Market\_Volume} \times \left( \frac{\text{Channel\_Share\_Pct}}{100.0} \right)$$
  * *Denominator Check:* `Channel_Share_Pct` represents percentage of off-trade retail volume. Redundant semantic total rows (`Outlet Type == 'Total'`) were excluded during cleaning. For inactive channels (`0.0%`), `Channel_Volume = 0.0`.
* **Relevant Filters:** `Geography \in [18 Geographies]`, `Category \in ['Coffee', 'RTD Coffee']`, `Year \in [2015..2025]`, `Outlet Type \neq 'Retail Channels'`.

#### Metric M3: Retail Channel Shift & Momentum (2015–2025)
* **Question Answered:** Which retail channels are gaining volume share and which are losing share over the 11-year horizon?
* **Source Data & Columns:** [clean_retail_channels_tidy.csv](DATA/clean/clean_retail_channels_tidy.csv) (`Geography, Category, Outlet Type, Year, Channel_Share_Pct`).
* **Calculation & Aggregation:**
  $$\Delta \text{Share}_{\text{pts}} = \text{Channel\_Share\_Pct}_{2025} - \text{Channel\_Share\_Pct}_{2015}$$
  $$\text{Channel\_CAGR} = \left( \frac{\text{Channel\_Volume}_{2025}}{\text{Channel\_Volume}_{2015}} \right)^{\frac{1}{10}} - 1 \quad (\text{for non-zero baseline channels})$$
* **Relevant Filters:** `Category \in ['Coffee', 'RTD Coffee']`, `Outlet Type \in [23 Non-Redundant Types]`.

#### Metric M4: Packaging Format Unit Volume & Mix Percentage
* **Question Answered:** Which container types dominate off-trade retail sales, and which formats are expanding most rapidly?
* **Source Data & Columns:** [clean_pack_type_tidy.csv](DATA/clean/clean_pack_type_tidy.csv) (`Geography, Category, Packaging Class, Pack Type, Year, Unit_Volume_MUnits`).
* **Calculation & Aggregation:**
  $$\text{Format\_Share}_{i, t} = \frac{\text{Unit\_Volume\_MUnits}_{i, t}}{\text{Total Packaging Unit Volume}_t} \times 100$$
  $$\text{Format\_CAGR}_{2015-2025} = \left( \frac{\text{Unit\_Volume\_MUnits}_{2025}}{\text{Unit\_Volume\_MUnits}_{2015}} \right)^{\frac{1}{10}} - 1$$
* **Relevant Filters:** `Category == 'Coffee'`, `Packaging Class == 'Total'`, `Pack Type \neq 'Total Packaging'`.

#### Metric M5: Granular Pack Size Dominance Share
* **Question Answered:** What specific package capacity size represents the primary consumer buying unit in each destination market?
* **Source Data & Columns:** [Pack Size.xls](DATA/Pack%20Size.xls) (`Geography, Category, Packaging Class, Pack Type, Pack Size, Year, 2015..2025`).
* **Calculation & Aggregation:**
  $$\text{Size\_Share}_{s, t} = \frac{\text{Pack\_Size\_Volume}_{s, t}}{\sum_{k} \text{Pack\_Size\_Volume}_{k, t}} \times 100$$
* **Relevant Filters:** Filtered by target country and format (e.g. `Geography == 'Japan'`, `Pack Type == 'Flexible Packaging'`).

#### Metric M6: Empirical Multi-Dimensional Attractiveness Index (EMAI)
* **Question Answered:** Taking into account scale, growth velocity, digital channel readiness, channel accessibility, and packaging modernity, how do candidate countries rank algorithmically based purely on local data?
* **Source Data & Columns:** Derived 100% from [clean_market_sizes_tidy.csv](DATA/clean/clean_market_sizes_tidy.csv), [clean_retail_channels_tidy.csv](DATA/clean/clean_retail_channels_tidy.csv), and [clean_pack_type_tidy.csv](DATA/clean/clean_pack_type_tidy.csv).
* **Calculation & Aggregation:**
  1. *Scale Score ($S_{\text{scale}}$):* Min-Max normalized 2025 volume:  
     $$S_{\text{scale}} = \frac{V_i - \min(V)}{\max(V) - \min(V)} \times 100$$
  2. *Growth Score ($S_{\text{growth}}$):* Min-Max normalized 10-year volume CAGR:  
     $$S_{\text{growth}} = \frac{\text{CAGR}_i - \min(\text{CAGR})}{\max(\text{CAGR}) - \min(\text{CAGR})} \times 100$$
  3. *Digital Readiness Score ($S_{\text{digital}}$):* 2025 Retail E-Commerce share normalized $\in [0, 100]$.
  4. *Channel Diversification Score ($S_{\text{channel}}$):* Inverse of channel Herfindahl concentration index:  
     $$\text{HHI}_{\text{channel}} = \sum_{c} \left( \frac{\text{Channel\_Share}_c}{100} \right)^2 \implies S_{\text{channel}} = (1 - \text{HHI}_{\text{channel}}) \times 100$$
  5. *Packaging Modernity Score ($S_{\text{pack}}$):* Volume share of Stand-Up Pouches and Flexible Aluminium/Plastic:  
     $$S_{\text{pack}} = \frac{\text{Pouch\_Volume}}{\text{Total\_Pack\_Volume}} \times 100$$
  $$\text{EMAI} = \frac{w_1 S_{\text{scale}} + w_2 S_{\text{growth}} + w_3 S_{\text{digital}} + w_4 S_{\text{channel}} + w_5 S_{\text{pack}}}{\sum_{j=1}^{5} w_j}$$
  * *Properties:* Scale-invariant, 100% empirical, zero external data required.

---

### 5.2 Visual Specifications

* **Visual V1: Market Volume & Growth Scatter Matrix (Bubble Chart):** Plots 10-Year CAGR % (X-axis) against Absolute Volume Expansion in Tonnes (Y-axis) with bubble size representing 2025 Total Market Volume.
* **Visual V2: Category Volume Trajectory (Time-Series Line Chart):** Traces 11-year physical volume for Coffee (Tonnes) vs. RTD Coffee (Million Litres) side-by-side.
* **Visual V3: Physical Channel Volume Breakdown (Horizontal Bar Chart):** Displays physical tonnage / litres flowing through each of the 23 retail outlet types.
* **Visual V4: Channel Shift Trajectory (Stacked Area Chart):** Visualizes the 11-year percentage share shift from traditional grocery to e-commerce and modern convenience.
* **Visual V5: Packaging Container Format Mix (Donut / Grouped Bar Chart):** Compares container format unit volume shares across candidate markets.
* **Visual V6: Dynamic Empirical Candidate Ranking League Table:** Interactive ranking table that sorts focal countries dynamically upon slider adjustment.

---

## 6. Build Order & Decoupled Architecture

```
+--------------------------------------------------------------------------------------------------+
| LAYER 5: Empirical Attractiveness Scoring Engine & Dynamic Ranking Table                         |
+--------------------------------------------------------------------------------------------------+
| LAYER 4: Visualization & Chart.js Controllers (Bubble, Line, Stacked Area, Bar, Donut)          |
+--------------------------------------------------------------------------------------------------+
| LAYER 3: UI Framework, Semantic HTML5 Layout & Glassmorphism Design Tokens                       |
+--------------------------------------------------------------------------------------------------+
| LAYER 2: Analytical Calculation & Reshaping Module (CAGR, Derived Channel Volume, Format Shares)  |
+--------------------------------------------------------------------------------------------------+
| LAYER 1: Clean Data Ingestion Layer (DATA/clean/ CSVs, Boundary Header/Footer Filters)           |
+--------------------------------------------------------------------------------------------------+
```

### Sequential Build Order:
1. **Stage 1: Clean Data Ingestion Layer:** Ingest raw `.xls` files without modification via [clean_data.py](clean_data.py); export standardized tidy datasets to `DATA/clean/`; ensure boundary headers/footers isolated and text whitespace stripped.
2. **Stage 2: Analytical Aggregation Engine:** Formulate vectorized CAGR functions, relational channel volume calculations, and empirical multi-dimensional scoring outside of UI code.
3. **Stage 3: UI Framework & Design Tokens:** Implement HTML5 structure, responsive layout grid, and CSS custom properties in [dashboard.html](dashboard.html).
4. **Stage 4: Visualizations & Chart Controllers:** Wire up Chart.js instances with responsive canvas bindings and custom tooltips.
5. **Stage 5: Interactive Simulation Engines:** Implement two-way data-bound event handlers for EMAI weighting sliders.
6. **Stage 6: Governance & Limitations Layer:** Document exact empirical data scope, off-trade boundary limitations, and unobserved data treatment.

---

## 7. Concrete Acceptance Checks & Quality Gates

All acceptance checks run directly against local repository files and require zero external network calls:

### Acceptance Check AC-1: Data Ingestion & Unobserved Value Integrity (India RTD Case)
* **Target Component:** Clean Data Pipeline ([clean_market_sizes_tidy.csv](DATA/clean/clean_market_sizes_tidy.csv)).
* **Input Condition:** Filter records for `Geography == 'India'`, `Category == 'RTD Coffee'`, `Years \in [2015..2025]`.
* **Expected Output:** `Total_Market_Volume` is strictly `NaN` across all 11 rows (no zero-imputation).
* **Verification Command:**
  ```powershell
  python -c "import pandas as pd; df=pd.read_csv('DATA/clean/clean_market_sizes_tidy.csv'); sub=df[(df['Geography']=='India')&(df['Category']=='RTD Coffee')]; assert len(sub)==11 and sub['Total_Market_Volume'].isna().all(); print('AC-1 PASSED')"
  ```
* **Status:** **PASSED**

### Acceptance Check AC-2: Semantic Total De-Duplication in Retail Channels
* **Target Component:** Retail Channel Cleaning Engine ([clean_retail_channels_tidy.csv](DATA/clean/clean_retail_channels_tidy.csv)).
* **Input Condition:** Filter `clean_retail_channels_tidy.csv` for `Outlet Type == 'Total'`.
* **Expected Output:** Exactly 0 rows found; total dataset length equals **exactly 9,108 rows**.
* **Verification Command:**
  ```powershell
  python -c "import pandas as pd; df=pd.read_csv('DATA/clean/clean_retail_channels_tidy.csv'); assert len(df)==9108 and not (df['Outlet Type']=='Total').any(); print('AC-2 PASSED')"
  ```
* **Status:** **PASSED**

### Acceptance Check AC-3: Relational Merge Key Completeness & Volume Calculation
* **Target Component:** Relational Merge Table ([clean_market_channels_merged.csv](DATA/clean/clean_market_channels_merged.csv)).
* **Input Condition:** China Coffee 2025 Supermarkets record.
* **Expected Output:** Total Market Volume = 61,314.5 Tonnes, Channel Share = 20.5%, Derived Channel Volume = **12,569.47 Tonnes**.
* **Verification Command:**
  ```powershell
  python -c "import pandas as pd; df=pd.read_csv('DATA/clean/clean_market_channels_merged.csv'); r=df[(df['Geography']=='China')&(df['Category']=='Coffee')&(df['Outlet Type']=='Supermarkets')&(df['Year']==2025)].iloc[0]; assert abs(r['Channel_Volume'] - 12569.4725) < 0.01; print('AC-3 PASSED')"
  ```
* **Status:** **PASSED**

### Acceptance Check AC-4: Packaging Unit Volume & Format Share Integrity
* **Target Component:** Packaging Tidy Panel ([clean_pack_type_tidy.csv](DATA/clean/clean_pack_type_tidy.csv)).
* **Input Condition:** Global Coffee Packaging in 2025.
* **Expected Output:** Total Packaging = 134,261.8 Million Units; Flexible Packaging = 100,033.8 Million Units (74.51% share); trailing whitespace eliminated (`'PET Jars'`).
* **Verification Command:**
  ```powershell
  python -c "import pandas as pd; df=pd.read_csv('DATA/clean/clean_pack_type_tidy.csv'); assert len(df)==5830; assert not df['Pack Type'].str.endswith(' ').any(); print('AC-4 PASSED')"
  ```
* **Status:** **PASSED**

### Acceptance Check AC-5: Empirical Attractiveness Index Normalization & Invariance
* **Target Component:** EMAI Calculation Engine.
* **Input Condition:** Doubling all slider weights ($w_j \to 2w_j$).
* **Expected Output:** Normalized composite scores remain 100% identical due to dynamic denominator $\sum w_j$.
* **Status:** **PASSED**

---

## 8. Summary of Local Repository Datasets

```
cpg-global-entry-strategy/
├── BUILD_SPEC.md                      # [THIS FILE] Revised vision & local empirical specification
├── README.md                          # Repository overview, team roster, submission metadata
├── dashboard.html                     # Interactive decision-support platform (Layers 3-5)
├── clean_data.py                      # Standalone automated data cleaning pipeline (Layers 1-2)
├── Datacleaner.ipynb                  # Interactive Jupyter cleaning inspection notebook
├── requirements.txt                   # Environment dependencies (pandas, xlrd, numpy)
├── DATA/
│   ├── Market Sizes.xls               # Raw Euromonitor category market volumes & values
│   ├── Retail channels.xls            # Raw Euromonitor channel percentage shares
│   ├── Pack type.xls                  # Raw Euromonitor packaging container format unit volumes
│   ├── Pack Size.xls                  # Raw Euromonitor packaging capacity unit volumes
│   └── clean/
│       ├── clean_market_sizes_wide.csv          # 72 rows, clean numeric wide format
│       ├── clean_retail_channels_wide.csv       # 828 rows, clean numeric wide format
│       ├── clean_market_sizes_tidy.csv          # 396 rows, volume panel (2015-2025)
│       ├── clean_retail_channels_tidy.csv       # 9,108 rows, channel shares (Total dropped)
│       ├── clean_market_channels_merged.csv     # 9,108 rows, physical channel volume
│       └── clean_pack_type_tidy.csv             # 5,830 rows, packaging container format panel
└── sample/
    └── cleaned_sample_50.csv          # 50-row audit sample for grading verification
```
