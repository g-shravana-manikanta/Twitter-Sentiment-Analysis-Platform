import os

# Base directory of the project (parent of 'app')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model and Vectorizer file paths resolved absolutely relative to BASE_DIR
MODEL_PATH = os.getenv(
    "MODEL_PATH", 
    os.path.join(BASE_DIR, "model", "sentiment_model.pkl")
)
VECTORIZER_PATH = os.getenv(
    "VECTORIZER_PATH", 
    os.path.join(BASE_DIR, "model", "vectorizer.pkl")
)

# CORS Allowed Origins
ALLOWED_ORIGINS = [
    "http://localhost:8501",
    "http://127.0.0.1:8501"
]

# Support overriding origins via env variables (comma-separated strings)
env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins:
    ALLOWED_ORIGINS = [origin.strip() for origin in env_origins.split(",") if origin.strip()]
