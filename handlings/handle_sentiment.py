from transformers import pipeline


sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


def handle_sentiment_feedback(message, pending_rating):
    sentiment = sentiment_model(message)[0]
    label, score = sentiment["label"], round(sentiment["score"], 2)
    pending_rating["active"] = True
    pending_rating["last_sentiment"] = label
    if label == "POSITIVE":
        return "😊 I'm glad you liked it!\nWould you like to rate this answer from 1–5 stars?"
    else:
        return "😔 Sorry to hear that.\nWould you like to rate this answer from 1–5 stars?"