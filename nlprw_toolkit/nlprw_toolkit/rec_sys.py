from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def train_tfidf_embeddings(corpus):
    vect = TfidfVectorizer()
    # get tfidf of all samples in the corpus
    docs = vect.fit_transform(corpus)
    return vect, docs


def tfidf_sim(sample_doc, vect, docs, top_n=8):
    # get tfidf vector for sample document
    selected_itm = vect.transform([sample_doc])

    # similarity between sample doc and the rest of the corpus
    cosine_sim = [cosine_similarity(selected_itm, itm)[0][0] for itm in docs]

    # index of top 8 matches
    indx_topn = sorted(
        range(len(cosine_sim)), key=lambda i: cosine_sim[i], reverse=True
    )[:top_n]
    top_scores = [(i, cosine_sim[i]) for i in indx_topn]
    return top_scores


def load_spacy_embeddings(corpus):
    import spacy

    nlp = spacy.load("en_core_web_lg")
    docs_spacy = [nlp("u'" + itm + "'") for itm in corpus]
    return nlp, docs_spacy


def spacy_sim(sample_doc, model, docs_spacy, top_n=8):
    selected_itm = model("u'" + sample_doc + "'")

    # Similarity between sample doc and the rest of the corpus
    sp_sim = [selected_itm.similarity(itm) for itm in docs_spacy]

    # index of top 8 matches
    indx_topn = sorted(range(len(sp_sim)), key=lambda i: sp_sim[i], reverse=True)[
        :top_n
    ]
    top_scores = [(i, sp_sim[i]) for i in indx_topn]
    return top_scores


def load_bert_model(corpus):
    from sentence_transformers import SentenceTransformer, util

    bert_model = SentenceTransformer("bert-base-nli-mean-tokens")

    document_embeddings = bert_model.encode(corpus)
    return bert_model, document_embeddings


def bert_sim(sample_doc, model, document_embeddings, top_n=8):
    selected_itm = model.encode(sample_doc)

    # Similarity between sample doc and the rest of the corpus
    bert_sim = [
        util.pytorch_cos_sim(selected_itm, itm).item() for itm in document_embeddings
    ]

    # index of top 8 matches
    indx_topn = sorted(range(len(bert_sim)), key=lambda i: bert_sim[i], reverse=True)[
        :top_n
    ]
    top_scores = [(i, bert_sim[i]) for i in indx_topn]
    return top_scores


def choose_model(data):
    """
    Will I find everything the sample may contain in the corpus? if so, it means you have representative data.
    Choose "sample_likely_represented_in_corpus" as True.

    Will I find generic terms/data outside of the corpus? if so, choose 'sample_likely_represented_in_corpus' False

    If corpus is domain specific, select 'corpus_domain_specific' as True, else False.
    """
    if data["corpus_domain_specific"] and data["sample_likely_represented_in_corpus"]:
        model = "tfidf"
    elif (
        data["corpus_domain_specific"] is False
        or data["sample_likely_represented_in_corpus"] is False
    ):
        model = "spacy"
    else:
        model = "spacy"
    return model


def run_rec_system(
    corpus,
    samples,
    top_n=8,
    data={"corpus_domain_specific": True, "sample_likely_represented_in_corpus": True},
):
    res = []
    model = choose_model(data)
    if model == "tfidf":
        tfidf_vect, tfidf_corpus = train_tfidf_embeddings(corpus)
        for s in samples:

            tfidf_top = tfidf_sim(s, tfidf_vect, tfidf_corpus, top_n=top_n)
            res.append([(corpus[i[0]], i[1]) for i in tfidf_top])
    elif model == "spacy":
        spacy_vect, spacy_corpus = load_spacy_embeddings(corpus)
        for s in samples:

            tfidf_top = spacy_sim(s, spacy_vect, spacy_corpus, top_n=top_n)
            res.append([(corpus[i[0]], i[1]) for i in tfidf_top])
    return res


if __name__ == "__main__":
    corpus = [
        "Python Machine Learning Tutorial (Data Science) Python Machine Learning Tutorial - Learn how to predict the kind of music people like. Subscribe for more Python tutorials like ...",
        "Ball python bite I decided to grab a snake out of its tank without asking, this was totally my fault. But now I can say I've been bit by a snake",
    ]
    sample = "spotted rattle skin in the field"
    # "Learn machine learning in 3 days"

    print("Specific sample with 'domain_specific':False")
    specific_recs = run_rec_system(
        corpus,
        [sample],
        top_n=2,
        data={
            "corpus_domain_specific": True,
            "sample_likely_represented_in_corpus": False,
        },
    )
    print(specific_recs)
    print(
        "Specific sample with 'domain_specific': True (consequence of wrong tool choice)"
    )
    specific_recs = run_rec_system(
        corpus,
        [sample],
        top_n=2,
        data={
            "corpus_domain_specific": True,
            "sample_likely_represented_in_corpus": True,
        },
    )
    print(specific_recs)
