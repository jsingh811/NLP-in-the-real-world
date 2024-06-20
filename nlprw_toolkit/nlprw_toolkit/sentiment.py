from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

STYLE = {
    "formal": "textblob",
    "informal": "vader",
    "mixed": "textblob",
}
TYPOS = {
    "many_nondict_terms": "vader",
    "some_nondict_terms": "textblob",
    "mostly_clean": "textblob",
}
SOURCE = {
    "social_media": "vader",
    "review_comments": "textblob",
    "articles": "textblob",
}


def get_textblob_sentiment(text):
    testimonial = TextBlob(text)
    score = testimonial.sentiment.polarity
    if score < 0:
        return "negative"
    elif score > 0:
        return "positive"
    else:
        return "neutral"


def get_vader_sentiment(text):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(text)
    maxval = max([sentiment_dict["neg"], sentiment_dict["pos"], sentiment_dict["neu"]])
    if sentiment_dict["neg"] == maxval:
        return "negative"
    elif sentiment_dict["pos"] == maxval:
        return "positive"
    else:
        return "neutral"


def get_sentiment(list_text, source={}, style={}, typos={}):
    choice = []
    for k in style:
        if style[k] and k in STYLE:
            choice.append(STYLE[k])
    for k in source:
        if source[k] and k in SOURCE:
            choice.append(SOURCE[k])
    for k in typos:
        if typos[k] and k in TYPOS:
            choice.append(TYPOS[k])
    if len(choice) == 0:
        winner = "textblob"
    else:
        winner = Counter(choice).most_common(1)[0][0]
    result = []
    if winner == "textblob":
        for t in list_text:
            result.append(get_textblob_sentiment(t))
    elif winner == "vader":
        for t in list_text:
            result.append(get_vader_sentiment(t))
    return result, winner


if __name__ == "__main__":
    sentences = ["i love you", "you dislike me or what?", "you hate ice cream", ""]
    sentiment, model_choice = get_sentiment(
        sentences,
        style={"mixed": True},
        typos={"mostly_clean": True},
        source={"review_comments": True},
    )
    print(sentiment)
    # >> ['positive', 'neutral', 'negative', 'neutral']

    print(model_choice)
    # >> 'textblob'

    sentences = ["The rooms were not very clean when we checked-in."]
    sentiment, model_choice = get_sentiment(
        sentences,
        style={"formal": True},
        typos={"mostly_clean": True},
        source={"review_comments": True},
    )
    print(sentiment)
    # >> ['negative']

    print(model_choice)
    # >> 'textblob'

    sentences = ["Show was really good it ws soooo fun."]
    sentiment, model_choice = get_sentiment(
        sentences,
        style={"informal": True},
        typos={"many_nondict_terms": True},
        source={"social_media": True, "review_comments": True},
    )
    print(sentiment)
    # >> ['positive']

    print(model_choice)
    # >> 'vader'
