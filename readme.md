# Enterprise Sales Forecasting Dashboard

A production-ready sales forecasting system designed to support business decision-making.  
This project demonstrates an end-to-end machine learning pipeline on Google Cloud Platform, from data ingestion and model training to real-time prediction via a web dashboard and API.

---

## Dashboard Preview

### Dashboard UI (Date Selection with Calendar)
![Dashboard UI](img/dashboard_1.png)

### Inference Result (Prediction Output)
![Inference Result](img/dashboard_2.png)

> The Streamlit dashboard allows users to select a date and receive real-time sales predictions.  
> The prediction logic is backed by a scalable Cloud Run inference API.

---

## What Problem Does This Project Solve?

Accurate sales forecasting is essential for budgeting, inventory planning, and strategic decision-making.  
However, many machine learning projects rely on unrealistic evaluation methods that lead to overconfident predictions in production.

This project focuses on:

- Reliable time-series forecasting for business use
- Realistic model evaluation without future data leakage
- A deployment-ready architecture suitable for enterprise environments

---

## System Architecture

**GCP × Vertex AI × Cloud Run × BigQuery × Terraform × GitHub Actions**

![Architecture Diagram](img/Architecture.drawio.png)

**High-level flow:**

1. Sales data is stored and queried in BigQuery  
2. Model training runs on Vertex AI using custom training jobs  
3. Trained models are versioned and managed centrally  
4. Predictions are served via a Cloud Run inference API  
5. The Streamlit dashboard consumes the API for real-time forecasting  
6. Infrastructure and deployments are automated via Terraform and CI/CD

---

## Model Evaluation (Realistic Validation)

To ensure reliable forecasting performance, two validation strategies were compared:

### Random Split (with future data leakage)
- R²: **0.72**
- RMSE: **6.86**

> Demonstrates high apparent accuracy, but is unsuitable for real-world forecasting.

### TimeSeriesSplit (no future data leakage)
- Average R²: **0.44**
- Average RMSE: **9.25**

> Provides a more honest estimate of how the model performs in production.

This project intentionally prioritizes **realistic evaluation over optimistic metrics**, reflecting best practices for enterprise-grade ML systems.

Below is an example of the sales trend used in this project:

![Sales Trend](img/graph.png)

---

## Key Features & Technical Stack

### Key Features
- End-to-end automated ML pipeline
- Real-time sales prediction via Cloud Run API
- Interactive dashboard for business users
- Time-series–aware validation strategy
- Fully reproducible infrastructure

### Technical Stack
- **Cloud Platform:** Google Cloud Platform (GCP)
- **Data & Storage:** BigQuery, Cloud Storage
- **Machine Learning:** Vertex AI (custom training)
- **Serving Layer:** Cloud Run
- **Web Interface:** Streamlit
- **Infrastructure as Code:** Terraform
- **CI/CD:** GitHub Actions

---

## Infrastructure as Code (IaC)

All cloud resources are provisioned and managed using **Terraform**, enabling:

- Reproducible and auditable environments
- Version-controlled infrastructure
- Scalable and maintainable system design

Terraform configurations are organized in the `terraform/` directory, following modular best practices.

---

## CI/CD Pipeline

GitHub Actions automates the full lifecycle:

- Linting and testing on pull requests  
- Docker image build and push to Artifact Registry  
- Model training and registration on Vertex AI  
- Deployment of services and infrastructure

Workflow definitions are located in `.github/workflows/`.

---

## Purpose

This project is designed as a portfolio piece to demonstrate my ability to build **production-grade machine learning systems** using Google Cloud.

It showcases skills relevant to:

- Enterprise data engineering  
- Machine learning system design  
- Cloud-native architecture  
- International freelance and overseas engineering roles  

All design decisions are aligned with real-world constraints and best practices commonly expected in global engineering teams.

---

## Key Takeaways

- Emphasis on realistic ML evaluation over inflated metrics  
- Clear separation between training and inference components  
- Automation-first approach using IaC and CI/CD  
- Business-oriented design rather than experiment-driven ML
