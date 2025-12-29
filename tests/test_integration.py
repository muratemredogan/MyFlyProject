"""Integration tests for model prediction flow."""
import pytest
import numpy as np
import tensorflow as tf
from unittest.mock import Mock, patch

from src.model import FlightDelayModel
from src.features import hash_airport_code, bucketize_delay
from src.app import predict, PredictionRequest


def test_model_initialization():
    """Test that model can be initialized and built."""
    model = FlightDelayModel(vocab_size=347, embedding_dim=32)
    model.build(input_shape=(None, 1))
    
    # Test that model can make a prediction
    input_tensor = tf.constant([[10]], dtype=tf.int32)
    output = model(input_tensor)
    
    assert output.shape == (1, 1), "Model output should have shape (1, 1)"
    assert isinstance(output.numpy()[0][0], (float, np.floating)), "Output should be numeric"


def test_prediction_flow_with_mock():
    """Test the complete prediction flow with mocked model."""
    # Create a mock model that returns a fixed prediction
    mock_model = Mock(spec=FlightDelayModel)
    mock_model.return_value = tf.constant([[45.5]], dtype=tf.float32)
    
    # Test the prediction logic
    airport_code = "JFK"
    airport_bucket = hash_airport_code(airport_code)
    input_tensor = tf.constant([[airport_bucket]], dtype=tf.int32)
    
    prediction = mock_model(input_tensor)
    predicted_delay = float(prediction.numpy()[0][0])
    delay_category = bucketize_delay(predicted_delay)
    
    assert predicted_delay == 45.5
    assert delay_category == 1  # 15 <= 45.5 < 60


def test_hash_to_prediction_pipeline():
    """Test the pipeline from airport code to prediction."""
    airport_code = "LAX"
    
    # Step 1: Hash airport code
    airport_bucket = hash_airport_code(airport_code)
    assert 0 <= airport_bucket < 100
    
    # Step 2: Create model and predict
    model = FlightDelayModel(vocab_size=347, embedding_dim=32)
    model.build(input_shape=(None, 1))
    
    input_tensor = tf.constant([[airport_bucket]], dtype=tf.int32)
    prediction = model(input_tensor)
    predicted_delay = float(prediction.numpy()[0][0])
    
    # Step 3: Bucketize delay
    delay_category = bucketize_delay(predicted_delay)
    
    assert isinstance(predicted_delay, float)
    assert delay_category in [0, 1, 2]


@patch('src.app.MODEL')
def test_predict_endpoint_logic(mock_model_instance):
    """Test the predict endpoint logic with mocked model."""
    # Setup mock model
    mock_model_instance.return_value = tf.constant([[30.0]], dtype=tf.float32)
    
    # Create request
    request = PredictionRequest(airport_code="JFK")
    
    # Call predict function
    response = predict(request)
    
    assert response.airport_code == "JFK"
    assert response.predicted_delay_minutes >= 0
    assert response.delay_category in [0, 1, 2]


def test_multiple_airport_predictions():
    """Test predictions for multiple different airports."""
    model = FlightDelayModel(vocab_size=347, embedding_dim=32)
    model.build(input_shape=(None, 1))
    
    airports = ["JFK", "LAX", "ORD", "DFW", "ATL"]
    predictions = []
    
    for airport in airports:
        airport_bucket = hash_airport_code(airport)
        input_tensor = tf.constant([[airport_bucket]], dtype=tf.int32)
        prediction = model(input_tensor)
        predicted_delay = float(prediction.numpy()[0][0])
        delay_category = bucketize_delay(predicted_delay)
        
        predictions.append({
            'airport': airport,
            'delay': predicted_delay,
            'category': delay_category
        })
    
    assert len(predictions) == 5
    for pred in predictions:
        assert pred['delay'] >= 0
        assert pred['category'] in [0, 1, 2]

