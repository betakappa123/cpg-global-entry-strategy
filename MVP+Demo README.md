# Yunnan Coffee Global Entry

DSO 576 — Project MVP

## Overview and intended users

Yunnan Coffee Global Entry is an interactive decision-support dashboard for strategy and commercial teams at a Yunnan coffee company. It addresses one central question: **Where should the next increment of sellable coffee go?** Users compare overseas opportunities with a China domestic baseline, explore channels and packaging, and test financial assumptions before deciding which markets deserve further research or a pilot.

The dashboard combines observed market evidence with clearly labeled planning assumptions. Its outputs support screening and further diligence; they are not investment approvals or forecasts of actual company sales.

## Project links

- [Live application](https://yunnan-coffee-global-entry.flaredlaugh2.chatgpt.site/)
- [Demo video](https://www.youtube.com/watch?v=_ebX7scGW8w)
- [GitHub repository](https://github.com/betakappa123/cpg-global-entry-strategy)

## Main features

| Page | What users can do | Decision supported |
| --- | --- | --- |
| Executive Scorecard | Review the selected scenario, margin spread, top eligible overseas target, readiness scores, unit economics, and focal-market comparison. | Identify markets worth investigating and compare export economics with domestic sales. |
| Market Attractiveness | Change category, country scope, start/end years, and exploration market; compare physical-volume trends, growth, nominal retail unit values, coverage, and e-commerce shares. | Assess market scale and direction while checking whether evidence is comparable and complete. |
| Product & Channels | Explore channel hierarchies, packaging types and sizes, proposed formats, and assumed channel fit. | Develop a product and route-to-market hypothesis to validate with buyers. |
| Financial Simulator | Adjust destination, annual export volume, wholesale invoice price, freight and insurance, tariff rate, and annual destination marketing. Review revenue, modeled operating profit and margin, profit delta, and the export-versus-domestic chart. | Test whether an export allocation remains attractive under different assumptions. |
| MCDA Decision Matrix | Adjust priorities for physical growth, modeled margin, trade ease, logistics, and origin affinity; inspect scores and rankings. | Understand how strategic preferences affect market screening. |
| Risks & Objections | Review trade-policy uncertainty, FX exposure, freshness and transit, channel fees, data limitations, capital requirements, and a conditional compliance roadmap. | Identify the evidence and approvals needed before a pilot or expansion. |

## Data scope and interpretation

The displayed source series covers **2015–2025**, with the selected period shown in the interface. The project uses market-size, retail-channel, packaging-type, and packaging-size data. The embedded source documentation identifies four team CSVs from the Final Data Version, derived from licensed Passport / Euromonitor source series. The source does not specify which years are observations versus forecasts.

The focal-market comparison includes **China, Japan, Australia, the United States, and Germany** where source observations are available. **South Korea and Singapore have no supplied source observations** in the demonstrated version. They remain visible as insufficient-data cases rather than receiving invented market measurements or eligible rankings. Broader country scopes and regional/world context can also be explored. Regional and world series overlap with country data and must not be added to country totals.

- Physical Coffee volume is displayed in tonnes; RTD Coffee volume is in million litres. Packaging counts are in million units, and package sizes use g or ml. Do not combine incompatible units.
- Category-average retail unit value is not a specialty-coffee quote or wholesale invoice price. Nominal USD comparisons do not isolate inflation, exchange-rate, or price effects.
- Channel shares use the displayed full-market denominator. Compare direct siblings in the channel hierarchy; do not add a parent to its children.
- Packaging counts describe observed formats, not demand for the Yunnan brand. Incomplete size groups are disclosed and do not establish a complete preference distribution.
- Missing observations remain unavailable rather than being interpreted as measured zeros.
- Only physical growth in the MCDA is measured from source data; modeled margin, tariff, transit, and origin-affinity inputs include planning assumptions. Financial scenarios concern finished Coffee and should not be applied directly to RTD Coffee.

**Data subset/sample:** The application uses the full cleaned datasets; no sampling or additional reduction was applied for deployment. Interactive filters change the displayed analytical scope without reducing the underlying datasets. Missing source observations and incomplete coverage remain disclosed.

## Analytical scopes

The app maintains three separate scopes:

- **Source exploration:** follows the selected category, country scope, years, and exploration market.
- **Financial simulation:** follows the selected export destination and live financial inputs, for finished Coffee only.
- **MCDA, readiness radar, and comparison economics:** use fixed Coffee 2015–2025 source growth and 50-tonne financial presets. MCDA weights change the composite rankings; they do not change the underlying radar criterion scores.

Changing a packaging size does not change financial-model volume or price. A financial simulator change does not replace the fixed MCDA financial presets.

## How to use

1. Open the live app and review the Executive Scorecard.
2. Select a category, country scope, period, and exploration market. Check coverage and units before comparing markets.
3. Explore Product & Channels to identify formats and channels worth testing.
4. Use the Financial Simulator to change assumptions and compare the export allocation with the same-volume domestic baseline.
5. Adjust MCDA weights to examine ranking sensitivity, then review Risks & Objections to define the next diligence steps.

The default screening ranks Australia first but states that **no market currently clears the priority-entry rule**. A favorable financial scenario alone does not establish market eligibility or confirmed demand.

### Difficult case: missing country data

Select **South Korea** on Product & Channels. The app displays: “Source market data unavailable for this country. Product rubric is a planning hypothesis only.” Missing evidence should be read as unavailable, and planning assumptions should not be treated as observed market results.

## Local setup and run instructions

The dashboard is a self-contained HTML application. Its data, styles, JavaScript, and Chart.js library are embedded in the file. Running this HTML does not require Python, Node.js, dependency installation, a build step, or a separate data download.

1. Download the self-contained dashboard HTML from the project files. The supplied local copy is named `Yunnan Coffee _ Global Entry.html`. Keep the `.html` extension when saving it.
2. Double-click the file, or use **Open With → Google Chrome** (or another modern browser).
3. Use the navigation tabs, filters, and simulator controls directly in the browser. No local server is required for this self-contained file.

Alternatively, download the repository using GitHub's **Code → Download ZIP**, then extract it, or clone it:

```bash
git clone https://github.com/betakappa123/cpg-global-entry-strategy.git
cd cpg-global-entry-strategy
```

Open the self-contained dashboard HTML included with the submitted project. The hosted version is also available through the Live application link above.

## Financial interpretation

Revenue equals finished kilograms × wholesale invoice price. Modeled cost includes sourcing, processing/roasting/packaging, freight, duties, and annual destination marketing. Duties use invoice revenue × the selected tariff rate. Domestic comparisons use the same finished volume. Margin spread is measured in **percentage points**, while profit delta is measured in **USD**.

The default Japan scenario at 50 tonnes yields $1,300,000 revenue, $625,000 modeled operating profit, and a $430,000 profit advantage over the $195,000 domestic comparator. These results follow the disclosed assumptions rather than verified commercial quotations.

## Current limitations

- Coverage is limited to the supplied source series, with gaps for some countries and packaging-size groups. The app is not a live market-data feed.
- Market size, channel mix, and packaging counts do not establish reachable specialty demand or willingness to buy Yunnan coffee.
- Financial outputs are contribution-style planning scenarios. The interface notes exclusions such as overhead, tax, capital expenditure, and other unmodeled costs. Tariffs and logistics inputs are assumptions requiring destination- and product-specific validation.
- MCDA rankings depend on weights, scoring choices, and assumptions. Missing market evidence prevents an eligible ranking even if scenario economics can be calculated.
- Buyer validation, distributor quotations, shelf-life checks, and a separate capital/working-capital case are needed before committing volume.
