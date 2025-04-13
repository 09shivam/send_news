from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_article(text):
    try:
        word_count = len(text.split())

        # Cap input to 1024 tokens for model efficiency
        if word_count > 1024:
            text = " ".join(text.split()[:1024])

        # Set max_length and min_length better for short and long inputs
        if word_count < 150:
            max_len = 60
            min_len = 20
        elif word_count < 300:
            max_len = 100
            min_len = 30
        else:
            max_len = 150
            min_len = 50

        summary = summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error summarizing article: {e}")
        return None
