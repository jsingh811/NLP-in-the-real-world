import re
import spacy

ENTITY_MODEL = {
    "email": "regex",
    "ORG": "spacy",
    "CARDINAL": "spacy",
    "DATE": "spacy",
    "GPE": "spacy",
    "PERSON": "spacy",
    "MONEY": "spacy",
    "PRODUCT": "spacy",
    "TIME": "spacy",
    "PERCENT": "spacy",
    "WORK_OF_ART": "spacy",
    "QUANTITY": "spacy",
    "NORP": "spacy",
    "LOC": "spacy",
    "EVENT": "spacy",
    "ORDINAL": "spacy",
    "FAC": "spacy",
    "LAW": "spacy",
    "LANGUAGE": "spacy",
}

ALL_ENTITIES = set(ENTITY_MODEL.keys())
MODELS = set(ENTITY_MODEL.values())


def extract_email(text):
    # \S matches any non-whitespace character
    # @ for its occurrence in the emaIl ID,
    #  . for the period after @
    # + for when a character is repeated one or more times
    emails = re.finditer("\S+@\S+\.\S+", text)
    return {"email": [(m.group(), m.start(0), m.end(0)) for m in emails]}


def extract_spacy(text):
    res = {}
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    for word in doc.ents:
        t, l = word.text, word.label_
        if l not in res:
            res[l] = []
        res[l].append((t, (word.start, word.end)))
    return res


def set_entity_funs(spacy_model="en_core_web_sm"):
    entity_funs = {"email": extract_email}
    entity_funs.update(
        {
            ent: (extract_spacy if ENTITY_MODEL[ent] == "spacy" else None)
            for ent in [
                "PRODUCT",
                "DATE",
                "EVENT",
                "TIME",
                "ORG",
                "CARDINAL",
                "GPE",
                "PERSON",
                "MONEY",
                "PERCENT",
                "WORK_OF_ART",
                "QUANTITY",
                "NORP",
                "LOC",
                "EVENT",
                "ORDINAL",
                "FAC",
                "LAW",
                "LANGUAGE",
            ]
        }
    )
    return entity_funs


def extract_entity(text, entities, spacy_model="en_core_web_sm"):
    res = {}
    funs = []
    entity_funs = set_entity_funs(spacy_model=spacy_model)
    for en in entities:
        funs.append(entity_funs[en])
    funs = set(funs)
    for f in funs:
        res.update(f(text))
    return {en: res.get(en, []) for en in entities}


def run(
    text,
    entities=[],
    entity_model=ENTITY_MODEL,
    verbose=False,
    spacy_model="en_core_web_sm",
):
    res = {}
    entities_comp = {}
    for cl in entities:
        if cl not in ALL_ENTITIES:
            print(f"Entity {cl} is not available in any pre-trained models {MODELS}")
            print(f"Provide labeled data to train a model for the {cl} entity")
        else:
            entities_comp[cl] = ENTITY_MODEL[cl]

    models = set(entities_comp.values())
    # find model for each entity
    if verbose:
        print("Extracting entities")
    mod_picks = {}
    for m in models:
        ents = [cl for cl in entities_comp if entities_comp[cl] == m]
        if verbose:
            print(ents, m)
        mod_picks[m] = ents
        res.update(extract_entity(text, ents, spacy_model=spacy_model))

    # return results back to user
    return res, mod_picks


if __name__ == "__main__":
    ents, models = run(
        "please write me at fejfow@iejf.com tomorrow about MOM Mission statement by 12.30 pm.",
        entities=["email", "pizza", "DATE", "EVENT", "TIME"],
    )
    print(ents)
    print(models)
