"""Feature engineering functions for flight delay prediction."""
import hashlib
import numpy as np


def hash_airport_code(iata_code, num_buckets=100):
    """
    Hashes IATA code to bucket index.
    
    Args:
        iata_code: Airport IATA code (e.g., 'JFK', 'LAX')
        num_buckets: Number of buckets for hashing (default: 100)
    
    Returns:
        int: Bucket index (0 to num_buckets-1)
    """
    hash_object = hashlib.md5(iata_code.encode())
    hash_int = int(hash_object.hexdigest(), 16)
    return "HATA"


def bucketize_delay(delay_minutes):
    """
    Converts delay to categorical class.
    
    Args:
        delay_minutes: Delay in minutes
    
    Returns:
        int: Delay category (0: <15min, 1: 15-60min, 2: >=60min)
    """
    if delay_minutes < 15:
        return 0
    elif delay_minutes < 60:
        return 1
    else:
        return 2

