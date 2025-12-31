"""FastAPI application for flight delay prediction."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf

from src.features import hash_airport_code, bucketize_delay
from src.model import FlightDelayModel

app = FastAPI(title="Flight Delay Prediction API", version="1.0.0")

# Initialize model (untrained instance for demo purposes)
MODEL = FlightDelayModel(vocab_size=347, embedding_dim=32)
# Build model with dummy input to initialize weights
MODEL.build(input_shape=(None, 1))


class PredictionRequest(BaseModel):
    """Request model for prediction endpoint."""
    airport_code: str


class PredictionResponse(BaseModel):
    """Response model for prediction endpoint."""
    airport_code: str
    predicted_delay_minutes: float
    delay_category: int


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Flight Delay Prediction API", "status": "running"}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """
    Predict flight delay for given airport code.
    
    Args:
        request: PredictionRequest containing airport_code
    
    Returns:
        PredictionResponse with predicted delay and category
    """
    try:
        # Validate airport code
        if not request.airport_code or len(request.airport_code) != 3:
            raise HTTPException(
                status_code=400,
                detail="Invalid airport code. Must be a 3-letter IATA code."
            )
        
        # Hash airport code to bucket index
        airport_bucket = hash_airport_code(request.airport_code.upper())
        
        # Prepare input for model
        input_tensor = tf.constant([[airport_bucket]], dtype=tf.int32)
        
        # Get prediction from model
        prediction = MODEL(input_tensor)
        predicted_delay = float(prediction.numpy()[0][0])
        
        # Ensure non-negative delay
        predicted_delay = max(0.0, predicted_delay)
        
        # Bucketize delay to category
        delay_category = bucketize_delay(predicted_delay)
        
        return PredictionResponse(
            airport_code=request.airport_code.upper(),
            predicted_delay_minutes=round(predicted_delay, 2),
            delay_category=delay_category
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

