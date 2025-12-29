"""Unit tests for feature engineering functions."""
import pytest
from src.features import hash_airport_code, bucketize_delay


def test_hash_airport_code_jfk_consistency():
    """Test that hash_airport_code returns consistent results for JFK."""
    result1 = hash_airport_code('JFK')
    result2 = hash_airport_code('JFK')
    result3 = hash_airport_code('JFK')
    
    assert result1 == result2 == result3, "Hash function should be deterministic"
    assert isinstance(result1, int), "Hash result should be an integer"
    assert 0 <= result1 < 100, "Hash result should be in range [0, 100)"


def test_hash_airport_code_different_airports():
    """Test that different airports produce different hash values."""
    jfk_hash = hash_airport_code('JFK')
    lax_hash = hash_airport_code('LAX')
    ord_hash = hash_airport_code('ORD')
    
    # At least two should be different (very unlikely all three are same)
    hashes = {jfk_hash, lax_hash, ord_hash}
    assert len(hashes) >= 2, "Different airports should produce different hashes"


def test_hash_airport_code_case_insensitive():
    """Test that hash function handles case consistently."""
    upper_hash = hash_airport_code('JFK')
    lower_hash = hash_airport_code('jfk')
    
    # MD5 is case-sensitive, so these should be different
    assert upper_hash != lower_hash, "Hash should be case-sensitive"


def test_bucketize_delay_category_0():
    """Test bucketize_delay for delays less than 15 minutes."""
    assert bucketize_delay(0) == 0
    assert bucketize_delay(5) == 0
    assert bucketize_delay(14) == 0
    assert bucketize_delay(14.9) == 0


def test_bucketize_delay_category_1():
    """Test bucketize_delay for delays between 15 and 60 minutes."""
    assert bucketize_delay(15) == 1
    assert bucketize_delay(30) == 1
    assert bucketize_delay(59) == 1
    assert bucketize_delay(59.9) == 1


def test_bucketize_delay_category_2():
    """Test bucketize_delay for delays 60 minutes or more."""
    assert bucketize_delay(60) == 2
    assert bucketize_delay(120) == 2
    assert bucketize_delay(300) == 2


def test_bucketize_delay_negative():
    """Test bucketize_delay for negative delays (early arrivals)."""
    assert bucketize_delay(-10) == 0  # Negative delays treated as category 0

