Distributed Sales Analytics using PySpark RDDs

A scalable data processing pipeline implemented using the PySpark RDD API. This project simulates a MapReduce-style task to perform distributed joins and aggregations on sales data, identifying top performers and regional trends.


🚀 Project Overview
The primary objective is to process two separate datasets—sales personnel details and transaction records—to derive high-level business insights. The pipeline demonstrates:

Distributed Joins: Merging personnel info with sales data using common keys.

MapReduce Workflow: Efficiently aggregating transaction amounts before joining to minimize data shuffle.

Global & Regional Insights: Identifying the top 3 sales performers globally and calculating total sales per geographic region.

🛠️ Tech Stack
Language: Python

Framework: Apache Spark (PySpark RDD API)

Environment: Google Colab / Local Spark Cluster

Data Format: CSV (Comma Separated Values)

📊 Data Schema
The project utilizes two relational datasets:

1. sales_people.csv
Contains metadata for the sales force. | Column | Description | | :--- | :--- | | id | Unique identifier for the salesperson | | name | Full name of the individual | | region | Geographic territory (North, South, East, West) |

2. sales_data.csv
Contains granular transaction records. | Column | Description | | :--- | :--- | | sale_id | Unique identifier for the transaction | | person_id | Foreign key referencing the salesperson | | amount | Numerical value of the sale |

⚙️ Implementation Details
1. Map Phase (Parsing & Cleaning)
Raw text files are loaded into RDDs. Headers are filtered out, and the strings are mapped into structured Key-Value pairs:

People RDD: (person_id, (name, region))

Sales RDD: (person_id, amount)

2. Reduce Phase (Aggregation & Join)
To ensure optimal performance and reduce network overhead (shuffle), sales are aggregated before the join:

reduceByKey() is used to sum all amounts for each person_id.

join() combines the aggregated sales with the salesperson’s metadata.

3. Optimization
Caching: The final_sales_rdd is cached in memory using .cache() because it is reused for multiple downstream actions (Top 3 calculation and Regional aggregation).

📈 Key Results
Based on the expanded dataset of 10 personnel and 20 transactions, the system produces the following insights:

Top 3 Global Performers:

Diana Prince (West)

Hank Pym (West)

Alice Johnson (North)

Regional Dominance: The West region leads in total sales volume.
