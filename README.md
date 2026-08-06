# Twitter Sentiment Analysis Platform

🔗 **Live Demo:** [twitter-sentiment-analysis-platform.streamlit.app](https://twitter-sentiment-analysis-platform.streamlit.app/)

> ⚠️ **Note:** The live demo is hosted on **Streamlit Community Cloud (free tier)**, which automatically puts apps to sleep after a period of inactivity. If you see a _"This app is sleeping"_ screen, simply click **"Yes, get this app back up!"** — the app will load within 20–30 seconds. This is expected platform behavior and not an application error.

A production-ready, full-stack Machine Learning application that classifies the sentiment of tweets in real-time. This project features a high-performance **FastAPI** backend serving a **Linear Support Vector Machine (Linear SVM)** model trained on the **Sentiment140 dataset (1.6 Million tweets)**, integrated with an intuitive, premium **Streamlit** frontend dashboard.

---

## 🏛️ System Architecture

```text
  [User / Browser]
         │
         ▼  (HTTP POST / GET)
  [Streamlit Dashboard]  (Port 8501)
         │
         ▼  (REST API Calls)
    [FastAPI Server]     (Port 8001)
         │
         ├──► [preprocess_text] ──► Removes stopwords (preserving negations), lemmatizes
         ├──► [TF-IDF Vectorizer] ──► Extracts text features (bi-grams vocabulary)
         └──► [Linear SVM] ──► Predicts polarity & estimates sigmoid confidence score
```

---

## 📁 Repository Structure

```text
twitter-sentiment-analysis/
├── .streamlit/
│   └── config.toml          # Custom theme configuration (Light theme)
├── app/
│   ├── __init__.py
│   ├── config.py            # Allowed CORS origins and artifact configurations
│   ├── main.py              # FastAPI application server (CORS, Lifespan, Endpoints)
│   ├── predictor.py         # Inference Engine (Sigmoid certainty calculations)
│   ├── preprocess.py        # Negation-aware text cleaning & lemmatization
│   └── schemas.py           # Pydantic schema validation structures
├── dataset/
│   └── training.1600000...  # Sentiment140 raw dataset CSV
├── frontend/
│   ├── favicon.png          # High-resolution X favicon logo
│   └── streamlit_app.py     # Streamlit web dashboard
├── model/
│   ├── sentiment_model.pkl  # Trained Linear SVM model weights
│   └── vectorizer.pkl       # Fitted TF-IDF Vectorizer
├── notebook/
│   └── Twitter_Sentiment_Analysis.ipynb  # ML Pipeline (EDA, comparison, training)
├── reports/
│   ├── model_training_report.md  # Training evaluation summary
│   └── model_training_report.txt
├── Dockerfile               # Production container configuration instructions
├── README.md                # System documentation
└── requirements.txt         # Package dependencies
```

---

## 🧠 Model & Preprocessing Pipeline

### 1. Preprocessing & Negation Handling
Standard cleaning pipelines often strip negation words (e.g., *not*, *no*, *never*), converting a sentence like `"The service is not good"` into `"service good"` (classified incorrectly as Positive). 

Our pipeline uses an optimized NLTK text-cleaning routine that **excludes negations** from the English stopwords list and preserves bi-gram vocabulary context:
*   Removes URLs, mentions (`@user`), hashtags (`#hash`), HTML tags, punctuation, and digits.
*   Retains negation markers (`not`, `no`, `never`, `against`, `don't`, `cannot`, etc.) and performs WordNet lemmatization.

### 2. Model Performance
After evaluating multiple models, the **Linear SVM** classifier was selected for deployment:

| Model | Accuracy | Precision | Recall | F1 Score |
| :--- | :---: | :---: | :---: | :---: |
| **Linear SVM** | **79.79%** | **78.70%** | **81.19%** | **79.92%** |
| Logistic Regression | 79.52% | 78.54% | 80.73% | 79.62% |
| Multinomial Naive Bayes | 77.66% | 77.77% | 76.87% | 77.32% |

---

## 🚀 Setup & Execution Guide

### Prerequisites
*   Python 3.10+
*   Pip package manager

### Local Environment Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/g-shravana-manikanta/Twitter-Sentiment-Analysis-Platform.git
   cd twitter-sentiment-analysis
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running Automated Tests
To run the preprocessing unit tests and the FastAPI TestClient contract tests, execute:
```bash
python -m pytest
```

---

### Running Locally

1. **Start the FastAPI Backend:**
   ```bash
   python -m uvicorn app.main:app --port 8001
   ```
   *The server will start on `http://127.0.0.1:8001` and automatically load the model & vectorizer pickles.*

2. **Start the Streamlit Frontend:**
   ```bash
   python -m streamlit run frontend/streamlit_app.py --server.port 8501
   ```
   *The Streamlit dashboard will open automatically in your browser at `http://localhost:8501`.*

---

## ⚡ API Endpoint Documentation

### 1. Health Sanity Check
Checks the server state and model load status. Used by cloud health monitors (e.g., Render, AWS ALB).
*   **Method:** `GET`
*   **Endpoint:** `/health`
*   **Response Payload (`200 OK`):**
    ```json
    {
      "status": "healthy",
      "model": "loaded"
    }
    ```

### 2. Predict Sentiment
Predicts sentiment polarity and estimated confidence.
*   **Method:** `POST`
*   **Endpoint:** `/predict`
*   **Request Payload:**
    ```json
    {
      "tweet": "The service is not good"
    }
    ```
*   **Response Payload (`200 OK`):**
    ```json
    {
      "prediction": "Negative",
      "confidence_score": 0.68
    }
    ```

---

## 🐳 Containerization (Docker)

To isolate dependencies and avoid deployment errors:

1. **Build the Docker Image:**
   ```bash
   docker build -t twitter-sentiment-analysis .
   ```

2. **Run the Container locally:**
   ```bash
   docker run -p 8001:8001 twitter-sentiment-analysis
   ```
   *This starts the FastAPI server inside the container, mapping port `8001` to your local machine.*

---

## ☁️ Cloud Deployment Guidelines

This application is ready for instant deployment to platforms like **Render**, **Railway**, or **AWS ECS**.

### Configuration Variables
To allow the frontend and backend to communicate securely across environments:
*   `BACKEND_URL`: Set this on the Streamlit frontend to your deployed FastAPI backend URL (e.g., `https://twitter-sentiment-api-dcco.onrender.com`).
*   `ALLOWED_ORIGINS`: Set this on the FastAPI backend on Render to your deployed Streamlit frontend URL (e.g., `https://twitter-sentiment-analysis-platform.streamlit.app`) to authorize incoming cross-origin CORS requests.

---

## ⚙️ CI/CD Integration
This repository integrates a **GitHub Actions CI/CD Pipeline** ([.github/workflows/ci.yml](file:///.github/workflows/ci.yml)) which automatically builds the environment and executes the preprocessing unit tests and FastAPI contract tests on every push or pull request to the `main` branch.

