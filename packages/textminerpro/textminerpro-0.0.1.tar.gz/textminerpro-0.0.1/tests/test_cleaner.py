from textminer.cleaner import remove_stopwords

def test_remove_stopwords():
    text = "This is a simple sentence for testing."
    cleaned = remove_stopwords(text, lang='english')
    assert "is" not in cleaned
    assert "This" not in cleaned
    assert "simple" in cleaned
