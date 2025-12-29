"""Keras model for flight delay prediction."""
import tensorflow as tf
from tensorflow.keras import layers, Model


class FlightDelayModel(Model):
    """Neural network model for predicting flight delays."""
    
    def __init__(self, vocab_size=347, embedding_dim=32):
        """
        Initialize the FlightDelayModel.
        
        Args:
            vocab_size: Size of the vocabulary (number of airport buckets)
            embedding_dim: Dimension of the embedding layer
        """
        super(FlightDelayModel, self).__init__()
        self.airport_embedding = layers.Embedding(
            vocab_size, embedding_dim, input_length=1
        )
        self.dense1 = layers.Dense(64, activation='relu')
        self.dense2 = layers.Dense(32, activation='relu')
        self.output_layer = layers.Dense(1)

    def call(self, inputs):
        """
        Forward pass through the model.
        
        Args:
            inputs: Input tensor (airport bucket indices)
        
        Returns:
            Tensor: Predicted delay value
        """
        x = self.airport_embedding(inputs)
        x = layers.Flatten()(x)
        x = self.dense1(x)
        x = self.dense2(x)
        return self.output_layer(x)

