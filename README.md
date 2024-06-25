# PhonePe-Pulse-Data-Visualization

## Table of Contents
- [Introduction](#introduction)
- [Problem Statement](#problem-statement)
- [Technology Stack Used](#technology-stack-used)
- [Approach](#approach)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction
PhonePe-Pulse-Data-Visualization is a project aimed at extracting, processing, and visualizing metrics and statistics from the PhonePe pulse GitHub repository. This project enables the generation of user-friendly visualizations that provide valuable insights using Python, MySQL, Streamlit, and Plotly.

## Problem Statement
The PhonePe pulse GitHub repository contains a vast collection of metrics and statistics. The objective of this project is to extract and process this data, enabling the generation of user-friendly visualizations that provide valuable insights.

## Technology Stack Used
- **Python**
- **MySQL**
- **Streamlit**
- **Plotly**
- **Github Cloning**
- **Geo Visualization**
- **Dynamic Updation**

## Approach
1. **Data Extraction**: The data is obtained from the PhonePe pulse GitHub repository using scripting techniques and cloned for further processing.
2. **Data Transformation**: The extracted data is formatted into a suitable structure, ensuring it is clean and ready for analysis. Pre-processing tasks may be performed as necessary.
3. **Database Integration**: The transformed data is inserted into a MySQL database, offering efficient storage and retrieval capabilities.
4. **Live Geo Visualization Dashboard**: Python's Streamlit and Plotly libraries are utilized to create an interactive and visually appealing dashboard. This dashboard presents the data in real-time, enabling users to explore the insights effectively.
5. **Database Integration with the Dashboard**: The relevant data is fetched from the MySQL database and seamlessly integrated into the dashboard, ensuring the displayed information is up-to-date and accurate.
6. **User-Selectable Dropdown Options**: The dashboard incorporates a minimum of 10 distinct dropdown options, providing users with the ability to select and view various facts and figures of interest. This feature enhances the customization and flexibility of the dashboard.

## Prerequisites
- Python 3.6+
- MySQL
- [pip](https://pip.pypa.io/en/stable/installation/)

## Installation
1. Clone the repository:
    ```bash
   git clone https://github.com/AkashScoder/DS_Phonepe-Pulse-Data-Visualization-and-Exploration.git
   cd DS_Phonepe-Pulse-Data-Visualization-and-Exploration

    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the MySQL database:
    - Create a new database.
    - Run the provided SQL script to create the necessary tables.
    - Update the database connection settings in the configuration file.

## Usage
1. **Data Extraction**: Run the script to extract and clone data from the PhonePe pulse GitHub repository.
    ```bash
    python data_extraction.py
    ```

2. **Data Transformation and Insertion**: Transform the extracted data and insert it into the MySQL database.
    ```bash
    python data_transformation.py
    ```

3. **Run the Streamlit Dashboard**: Start the Streamlit server to view the live geo-visualization dashboard.
    ```bash
    streamlit run dashboard.py
    ```

## Examples
### Scatter Plot
```python
import plotly.express as px
df = pd.read_sql("SELECT * FROM transactions", con=connection)
fig = px.scatter(df, x="transaction_amount", y="transaction_count", color="state", title="Scatter Plot")
fig.show()
