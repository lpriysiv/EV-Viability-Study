# EV-Viability-Study
                +----------------------+
                |    GitHub Actions    |  ← Scheduled or manual trigger
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
        +------------------+------------------+
        |                                     |
        v                                     v
+---------------+                    +--------------------+
|   Local / S3  |                    |   Streamlit App    |
|  Store results| ← reads files from |  (read-only mode)  |
+---------------+                    +--------------------+
