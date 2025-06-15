# EV-Viability-Study
## 📐 Architecture Diagram (Markdown-Friendly)
```
+----------------------+
|    GitHub Actions    |  ← Triggers pipeline
+----------+-----------+
           |
           v
+------------------------+
|    Data Pipeline (Py)  |
| - Fetch API data       |
| - Clean / model / plot |
| - Save CSV / PNG       |
+-----------+------------+
           |
           v
+-----------------------------+
|        Outputs Folder       |
|  (summary.csv, plots.png)   |
+-----------------------------+
           |
           v
+----------------------------+
|      Streamlit Dashboard    |
|  (Reads files from outputs) |
+----------------------------+
```
