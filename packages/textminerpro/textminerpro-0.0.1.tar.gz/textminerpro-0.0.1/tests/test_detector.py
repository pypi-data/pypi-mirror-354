from textminer.detector import detect_language

def test_detect_language_korean():
    assert detect_language("안녕하세요") == "ko"

def test_detect_language_english():
    assert detect_language("Hello, how are you?") == "en"
