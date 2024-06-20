import string
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from wordcloud import WordCloud
from collections import Counter

from sentiment import get_sentiment


# Global and Vars

STOP = set(stopwords.words("english"))
PUNCT = set(string.punctuation)
LEMMA = WordNetLemmatizer()
WC = WordCloud(
    mode="RGBA", collocations=False, background_color=None, width=1500, height=1000
)

# Functions


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in STOP])
    punc_free = "".join([ch for ch in stop_free if ch not in PUNCT])
    normalized = " ".join(LEMMA.lemmatize(word) for word in punc_free.split())

    return " ".join([i for i in normalized.split() if len(i) > 1])


def plot_wc(text_list):
    word_cloud = WC.generate(" ".join(text_list))
    plt.figure(figsize=(30, 20))
    # Display the generated Word Cloud
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def generate_plots(comments, sentiments):
    cntr = Counter(sentiments)
    plt.bar(cntr.keys(), cntr.values())
    plt.show()
    # positives
    plot_wc(
        [
            clean(comments[inx])
            for inx in range(len(sentiments))
            if sentiments[inx] == "positive"
        ]
    )
    # negatives
    plot_wc(
        [
            clean(comments[inx])
            for inx in range(len(sentiments))
            if sentiments[inx] == "negative"
        ]
    )


def classify_comments(comments, categories):
    from transformers import pipeline

    classifier = pipeline(
        "zero-shot-classification", model="typeform/distilbert-base-uncased-mnli"
    )

    result = [
        classifier(comments[i], candidate_labels=categories)
        for i in range(len(comments))
    ]
    return result


if __name__ == "__main__":

    comments = [
        "My experience at check-in counter was terrible. The staff was kind of rude and didn't want to help out much. No complaints otherwise.",
        "The carpet in the room was quite stained. I am surprised they didn't replace it given its condition.",
        "I love everything. The front desk was helpful.",
    ]
    sentiments, tool_choice = get_sentiment(comments, style={"formal": True})

    generate_plots(comments, sentiments)

    print(classify_comments(comments, categories=["staff person", "hotel property"]))
