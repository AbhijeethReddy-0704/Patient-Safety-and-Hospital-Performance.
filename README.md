# Hospital Safety & Clinical Performance Benchmarking

This project provides an end-to-end data engineering and analytics pipeline to evaluate healthcare quality across Texas. Using CMS datasets, the pipeline extracts, cleans, and analyzes hospital performance to identify top-rated facilities for acute clinical care.

## 🚀 Project Overview
* **Objective**: Benchmark 5-star hospitals in Texas based on 30-day mortality rates.
* **Data Source**: CMS Hospital General Information and Safety Score datasets (22MB+).
* **Key Results**: Successfully identified and visualized top-performing facilities.

## 🛠️ Technical Stack
* **Language**: Python 3.x (Pandas, Matplotlib, Seaborn)
* **Database**: MySQL (Relational Schema Design)
* **Tools**: VS Code, Git/GitHub

### 📈 Key Insights
The following visualization showcases the top-performing 5-star hospitals in Texas. Lower mortality scores indicate better clinical outcomes.

![Hospital Ranking Chart](hospital_ranking_chart.png)

### 🔧 Challenges & Solutions
* **Schema Mapping**: Resolved discrepancies between datasets using SQL joins.
* **Data Integrity**: Handled "Not Available" entries via Python cleaning.
* **Path Management**: Fixed environment-specific pathing issues in VS Code.