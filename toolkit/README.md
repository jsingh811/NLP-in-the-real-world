# Contents

1. [Setup](https://github.com/jsingh811/NLP-in-the-real-world/tree/toolkit/toolkit#setup)   
2. [NLP Tasks](https://github.com/jsingh811/NLP-in-the-real-world/tree/toolkit/toolkit#nlp-tasks)   
2.1. [Information Extraction / NER](https://github.com/jsingh811/NLP-in-the-real-world/tree/toolkit/toolkit#information-extraction--ner)  
2.2. [Sentiment Analysis](https://github.com/jsingh811/NLP-in-the-real-world/tree/toolkit/toolkit#sentiment-analysis)  
3. [Projects](https://github.com/jsingh811/NLP-in-the-real-world/tree/toolkit/toolkit#projects)  
3.1. [Comments Analysis](https://github.com/jsingh811/NLP-in-the-real-world/tree/toolkit/toolkit#comments-analysis)  
3.2. [Recommendation System or Content Similarity](https://github.com/jsingh811/NLP-in-the-real-world/tree/toolkit/toolkit#recommendation-system-or-content-similarity)  

# Setup

Clone the project from Github and run the following for setup.

```
git clone https://github.com/jsingh811/NLP-in-the-real-world.git
cd NLP-in-the-real-world/toolkit
pip install -e .
python -m spacy download en_core_web_sm
```

# NLP Tasks

## Information Extraction / NER

To run information extraction / named entity recognition (NER),

```
import infoextractor

doc = "please write me at fejfow@iejf.com tomorrow about MOM Mission statement by 12.30 pm."
entities = ['email', 'DATE', 'TIME', 'pizza_topping']
extracted_entities, model_selection = run(doc, entities=entities)
# >> Entity 'pizza_topping' is not available in any pre-trained models {'spacy', 'regex'}

print(extracted_entities)
# >> {'email': [('fejfow@iejf.com', 19, 34)], 'DATE': [('tomorrow', (5, 6))], 'TIME': [('12.30 pm', (11, 13))]}

print(models)
#>> {'regex': ['email'], 'spacy': ['DATE', 'TIME']}
```

## Sentiment Analysis

To run sentiment analysis, choose style as "formal", "informal", or "mixed"; choose typos as either "many_nondict_terms", "some_nondict_terms", or "mostly_clean"; choose source as "social_media", "review_comments", or "articles". Leave them blank if you don't have an appropriate value to assign to these fields.

```
import sentiment

# example 1
sentences = ["i love you", "you dislike me or what?", "you hate ice cream", ""]
sentiment, model_choice = get_sentiment(
    sentences,
    style={"mixed": True},
    typos={"mostly_clean": True},
    source={"review_comments": True}
)
print(sentiment)
# >> ['positive', 'neutral', 'negative', 'negative']

print(model_choice)
# >> 'textblob'

# example 2
sentences = ["Show was really good it ws soooo fun."]
sentiment, model_choice = get_sentiment(
    sentences,
    style={"informal": True},
    typos={"many_nondict_terms": True},
    source={"social_media": True, "review_comments": True}
)
print(sentiment)
# >> ['positive']

print(model_choice)
# >> 'vader'
```

## Content Summarizer

Coming soon


# Projects

## Comments Analysis

For running analysis of review comments, use review-analysis as below. It will generate sentiment scores, figure, and word cloud figures by sentiment. It will also return classifications found in each comment. You can specify the categories you want the comments to be classified with.

```
import review_analyzer

comments = [
  "My experience at check-in counter was terrible. The staff was kind of rude and didn't want to help out much. No complaints otherwise.",
  "The carpet in the room was quite stained. I am surprised they didn't replace it given its condition.",
  "I love everything. The front desk was helpful."
]

sentiments, tool_choice = get_sentiment(
    comments,
    style={"formal": True},
    source={"review_comments": True}
)

review_analyzer.generate_plots(comments, sentiments)

classifications = review_analyzer.classify_comments(comments, categories=['staff person', 'hotel property'])

print(classifications)
# >> [{'sequence': "My experience at check-in counter was terrible. The staff was kind of rude and didn't want to help out much. No complaints otherwise.", 'labels': ['staff person', 'hotel property'], 'scores': [0.7497782707214355, 0.25022172927856445]}, {'sequence': "The carpet in the room was quite stained. I am surprised they didn't replace it given its condition.", 'labels': ['hotel property', 'staff person'], 'scores': [0.6811559796333313, 0.3188440203666687]}, {'sequence': 'I love everything. The front desk was helpful.', 'labels': ['staff person', 'hotel property'], 'scores': [0.6326051950454712, 0.3673948347568512]}]
```


## Recommendation System or Content Similarity

For building a content based recommendation system, use `rec_sys` as below. It will generate top n matches with scores using different embeddings. If you expect to find mostly everything that your new data may contain in the corpus, it means you have representative data, and you should choose "sample_likely_represented_in_corpus" as True.
If you are likely to find generic terms/data outside of the corpus, choose 'sample_likely_represented_in_corpus' False.
If corpus is domain specific, select 'corpus_domain_specific' as True, else False.

```
import rec_sys

corpus = [
      "Python Machine Learning Tutorial (Data Science) Python Machine Learning Tutorial - Learn how to predict the kind of music people like. Subscribe for more Python tutorials like ...",
      "Ball python bite I decided to grab a snake out of its tank without asking, this was totally my fault. But now I can say I've been bit by a snake"
  ]
sample = "spotted rattle skin in the field"

print("'sample_likely_represented_in_corpus': False")
recs = run_rec_system(
    corpus,
    [sample],
    top_n=2,
    data={'corpus_domain_specific': True, 'sample_likely_represented_in_corpus': False}
)
print(recs)
#>> [[("Ball python bite I decided to grab a snake out of its tank without asking, this was totally my fault. But now I can say I've been bit by a snake", 0.731253418677792), ('Python Machine Learning Tutorial (Data Science) Python Machine Learning Tutorial - Learn how to predict the kind of music people like. Subscribe for more Python tutorials like ...', 0.6951807783413815)]]

print("'sample_likely_represented_in_corpus': True (consequence of wrong tool choice)")
recs = run_rec_system(
    corpus,
    [sample],
    top_n=2,
    data={'corpus_domain_specific': True, 'sample_likely_represented_in_corpus': True}
)
print(recs)
#>> [[('Python Machine Learning Tutorial (Data Science) Python Machine Learning Tutorial - Learn how to predict the kind of music people like. Subscribe for more Python tutorials like ...', 0.17008208798133495), ("Ball python bite I decided to grab a snake out of its tank without asking, this was totally my fault. But now I can say I've been bit by a snake", 0.0)]]
```
