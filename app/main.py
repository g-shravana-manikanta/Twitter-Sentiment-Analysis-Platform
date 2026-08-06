import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import ALLOWED_ORIGINS
from app.schemas import SentimentRequest, SentimentResponse, HealthResponse
from app.predictor import predictor

# Configure standard python logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("app")

# Ensure the logger propagates properly or configure it specifically
logger.propagate = True

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Lifecycle: Load model and vectorizer once
    logger.info("Server startup initiated.")
    try:
        predictor.load_model()
    except Exception as e:
        logger.critical(f"Server startup failed during model loading: {str(e)}", exc_info=True)
        raise e
    yield
    # Shutdown Lifecycle
    logger.info("Server shutting down.")

# Initialize FastAPI App
app = FastAPI(
    title="Twitter Sentiment Analysis API",
    description="Production-ready FastAPI backend for Twitter Sentiment Classification using TF-IDF and Linear SVM.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handler: Pydantic Validation Errors (Missing fields, empty inputs)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error("Invalid request.")
    errors = exc.errors()
    for err in errors:
        logger.error(f"Validation failure details: Field: {err.get('loc')}, Msg: {err.get('msg')}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": errors,
            "message": "Validation Error: Ensure required fields are sent with valid lengths."
        }
    )

# Exception Handler: Explicit HTTP Exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Exception Handler: Generic Unexpected Exceptions (Internal Server Errors)
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal Server Error",
            "message": "An unexpected error occurred. Please contact system administration."
        }
    )

# Endpoint: Root Welcome Message
@app.get("/", tags=["General"])
def read_root():
    return {
        "message": "Welcome to the Twitter Sentiment Analysis API!",
        "documentation": "/docs",
        "health": "/health"
    }

# Endpoint: Health Check
@app.get("/health", response_model=HealthResponse, tags=["General"])
def health_check():
    if predictor.model is None or predictor.vectorizer is None:
        logger.error("Health check failed. Model or Vectorizer is not loaded.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model loading failure. Service is unavailable."
        )
    return {"status": "healthy", "model": "loaded"}

# Endpoint: Sentiment Prediction
@app.post("/predict", response_model=SentimentResponse, tags=["Classification"])
def predict_sentiment(request: SentimentRequest):
    logger.info("Prediction request received.")
    start_time = time.perf_counter()
    
    try:
        # Run prediction
        result = predictor.predict(request.tweet)
        
        # Calculate execution duration
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        logger.info(f"Prediction completed in {duration_ms} ms.")
        logger.info(f"Prediction result: {result['prediction']} (Score: {result['confidence_score']})")
        
        return result
    except FileNotFoundError as fnf_err:
        logger.error(f"Model loading failure: {str(fnf_err)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Prediction engine failed: Model files are missing."
        )
    except Exception as err:
        logger.error(f"Prediction process failed: {str(err)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during prediction parsing."
        )
