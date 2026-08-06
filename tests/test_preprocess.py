import os
import sys

# Add project root to python path for safe imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app.preprocess import preprocess_text

def test_preprocess_standard():
    text = "I am loving this phone, it is amazing!"
    cleaned = preprocess_text(text)
    assert "loving" in cleaned
    assert "amazing" in cleaned

def test_preprocess_negations():
    text = "The customer service was not good and never resolved the issue"
    cleaned = preprocess_text(text)
    # Check that negation words are explicitly preserved
    assert "not" in cleaned
    assert "never" in cleaned

def test_preprocess_strip_links_and_handles():
    text = "Check this link https://google.com and follow @user"
    cleaned = preprocess_text(text)
    # Check that URL and user handles are completely stripped
    assert "google" not in cleaned
    assert "user" not in cleaned
