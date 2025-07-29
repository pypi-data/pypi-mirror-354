
from gensim.summarization import summarize

def summarize_text(text: str, ratio=0.2):
    try:
        return summarize(text, ratio=ratio)
    except ValueError:
        return text  # 너무 짧으면 그대로 반환
