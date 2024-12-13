# Gun Violence Incident Analysis

<p align="center">
    <img src="https://www.gunviolencearchive.org/sites/default/files/logo.png" alt="Gun Violence Archive" width="50%">
</p>

## Overview

This project aims to analyze gun violence incidents in the United States, leveraging a comprehensive dataset spanning from January 2013 to March 2018. Using advanced big data technologies and machine learning models, we uncover critical insights, predict trends, and support data-driven decision-making to address this significant public health and societal issue.

## Dataset

The dataset, sourced from the Gun Violence Archive (GVA), includes detailed records of over 260,000 gun violence incidents. Key columns in the dataset include:

| Column                          | Description                                                   |
|--------------------------------|---------------------------------------------------------------|
| `incident_id`                  | Unique identifier for each incident                           |
| `date`                         | Date of the incident                                          |
| `state`                        | State where the incident occurred                             |
| `city_or_county`               | City or county where the incident occurred                   |
| `address`                      | Specific address of the incident (if available)              |
| `n_killed`                     | Number of people killed in the incident                       |
| `n_injured`                    | Number of people injured in the incident                      |
| `incident_url`                 | URL with further details about the incident                   |
| `source_url`                   | URL of the source of the data                                 |
| `gun_stolen`                   | Indicator if the gun involved was stolen                      |
| `gun_type`                     | Type of gun involved                                          |
| `incident_characteristics`     | Characteristics of the incident                               |
| `latitude`                     | Latitude of the incident location                             |
| `longitude`                    | Longitude of the incident location                            |
| `n_guns_involved`              | Number of guns involved in the incident                       |
| `participant_age`              | Age of participants involved in the incident                 |
| `participant_gender`           | Gender of participants                                        |
| `participant_relationship`     | Relationship of participants to each other                   |
| `participant_status`           | Status of the participants (e.g., suspect, victim)           |
| `participant_type`             | Type of participant (e.g., perpetrator, victim)              |
| `notes`                        | Additional notes about the incident                           |

## Project Goals

1. Perform comprehensive exploratory data analysis (EDA) to identify trends, patterns, and key insights.
2. Develop predictive models for time series forecasting and classification of incidents based on severity.
3. Visualize geographic and temporal distributions to highlight high-risk areas and periods.
4. Enable informed decision-making for public health interventions and resource allocation.

## Technologies Used

- **Big Data Tools:** Apache Spark, PySpark for distributed data processing.
- **Machine Learning Models:** SARIMA, SARIMAX, Prophet, LSTM for time series; Logistic Regression, Gradient Boosting for classification.
- **Visualization Tools:** Matplotlib, Seaborn, Plotly for data visualization.
- **Deployment:** Streamlit for interactive dashboards and visualizations.
- **Data Management:** Pandas, NumPy for preprocessing and analysis.

## Folder Structure

```
├── README.md                # Project overview
├── data                     # Raw and cleaned datasets
│   ├── gun-violence-data_01-2013_03-2018.csv
│   ├── gun_violence_cleaned_data_2013_2018.csv
├── helper                   # Helper functions
│   ├── constants.py
│   └── __init__.py
├── images                   # Analysis and result visualizations
├── notebooks                # Jupyter notebooks for various analyses
│   ├── 01_initial_exploratory_analysis.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_cleaned_data_exploration.ipynb
│   ├── 04_cluster_analysis.ipynb
│   ├── 05_classification.ipynb
│   └── 06_time_series_analysis.ipynb
├── scripts                  # Python scripts for automation and visualization
│   ├── visualizations.py
│   ├── snowflake_sink.py
│   └── __init__.py
├── streamlit                # Streamlit app for interactive dashboards
│   ├── app.py
│   ├── data
│   ├── images
│   └── models
└── requirements.txt         # Dependencies
```

## How to Use

1. Clone the repository:
   ```bash
   git clone [<repository_url>](https://github.com/bharath03-a/Gun-Violence-Incidents)
   ```

3. Explore the notebooks for step-by-step analysis:
   - Initial exploratory analysis: `notebooks/01_initial_exploratory_analysis.ipynb`
   - Data preprocessing: `notebooks/02_data_preprocessing.ipynb`
   - Cleaned data exploration: `notebooks/03_cleaned_data_exploration.ipynb`
   - Clustering: `notebooks/04_cluster_analysis.ipynb`
   - Classification: `notebooks/05_classification.ipynb`
   - Time Series Analysis: `notebooks/06_time_series_analysis.ipynb`

4. Run the Streamlit app for an interactive dashboard:
   ```bash
   streamlit run streamlit/app.py
   ```

## Appendix

Additional visualizations and analyses are available in the `images/` directory and the Streamlit dashboard. Further insights and updates can be found in the project repository.

## Acknowledgments

We thank the Gun Violence Archive (GVA) for providing the dataset that served as the foundation for this project.
