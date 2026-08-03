from pydantic import BaseModel, Field

class SentimentRequest(BaseModel):
    tweet: str = Field(
        ..., 
        min_length=1, 
        description="The tweet text to classify"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "tweet": "I love this phone"
            }
        }

class SentimentResponse(BaseModel):
    prediction: str = Field(
        ..., 
        description="The predicted sentiment label (Positive or Negative)"
    )
    confidence_score: float = Field(
        ..., 
        description="Estimated confidence score for the prediction"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "prediction": "Positive",
                "confidence_score": 0.92
            }
        }

class HealthResponse(BaseModel):
    status: str = Field(
        "healthy", 
        description="The API operational status"
    )
    model: str = Field(
        "loaded", 
        description="The ML model loading state"
    )
