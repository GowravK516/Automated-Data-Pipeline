# Automated Data Ingestion Pipeline

An automated, end-to-end data pipeline built to fetch, transform, and store live external data using CI/CD workflows. 

## 🛠️ Tech Stack
* **Language:** Python 3
* **Data Processing:** Pandas
* **Automation:** GitHub Actions (CI/CD)
* **Data Source:** REST API Integration

## ⚙️ Architecture & Workflow
1. **Scheduled Ingestion:** A GitHub Actions Cron job triggers the pipeline automatically every day at midnight.
2. **API Extraction:** The Python script connects to a live external REST API using the `requests` library to fetch the latest JSON data.
3. **Data Transformation:** The raw JSON is loaded into a Pandas DataFrame, where it is filtered, cleaned, and formatted.
4. **Storage:** The processed data is exported as a clean `live_dataset.csv` ready for downstream analytics.

## 👥 Contributors
* Gowrav (Code Implementation)
* Niveditha (CI/CD Automation)
* Gowtham (Repository Management & Code Review)
