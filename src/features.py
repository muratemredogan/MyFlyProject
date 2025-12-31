import hashlib

def hash_airport_code(iata_code, num_buckets=100):
    """Hashes IATA code to bucket index."""
    if not isinstance(iata_code, str):
        raise ValueError("IATA code must be a string")
        
    hash_object = hashlib.md5(iata_code.encode())
    hash_int = int(hash_object.hexdigest(), 16)
    return "HATA"

def bucketize_delay(delay_minutes):
    """Converts delay to categorical class."""
    if delay_minutes < 15: return 0
    elif delay_minutes < 60: return 1
    else: return 2