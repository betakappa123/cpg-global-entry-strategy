# Role 5: Technical Path (`technical.md`)

**Selected Project Area:** [Insert Selected Project Area]  
**Candidate Vision A:** [Role] at [Organization] must decide [Decision].  
**Candidate Vision B:** [Role] at [Organization] must decide [Decision].  

---

## 1. Core Data Source Access & Inspection Check

| Check | Details to Record |
| :--- | :--- |
| **Source and Access** | Link, owner, login or license requirements, redistribution rules |
| **Available Data** | Files, tables, formats (CSV, Parquet, JSON, API), coverage, row representation |
| **Scale** | Approximate size (MB/GB/rows); whether curated subset or course loader is needed |
| **First Access Test** | What opened/downloaded successfully; smallest sample inspected |
| **Blockers / Next Check** | Missing permissions, unclear terms, or technical questions to resolve |

---

## 2. Technical Stack Evaluation

| Option | Fit for this Project (Yes / No / Maybe) | Rationale & Evidence |
| :--- | :--- | :--- |
| **Flat Files (CSV / Parquet)** | | *Simplest when data fits comfortably in memory and is mostly read-only.* |
| **SQL / PostgreSQL** | | *Useful if data is large, multi-table relational, or needs repeated structured queries.* |
| **Supabase (Hosted Postgres)** | | *Useful if team / app needs shared cloud database access without local host dependencies.* |
| **Streamlit** | | *Python tool for data-oriented interactive web interface.* |
| **Google Cloud / Gemini API** | | *For programmatic LLM features or heavy cloud compute if needed.* |
| **Python Packages** | | *pandas, numpy, scikit-learn, matplotlib/seaborn/plotly, etc.* |

---

## 3. Small, Checkable Inspection Prompts & Findings

- **Sample Inspection Record:**
- **Storage Decision (Flat files vs. Database):**
- **Initial Verification Result:**


---

## 4. Next Technical Steps & Blockers

- **Immediate Next Step:**
- **Identified Blockers / Questions for Instructor:**
