from transformers import pipeline

def get_summary(model, tokenizer, min_length=50, max_length=500, truncation=True):
    summarizer = pipeline(
        "summarization",
        model=model,
        tokenizer=tokenizer
        )
    summary = summarizer(
        text, min_length=min_length, max_length=max_length,
        truncation=truncation
    )
    return summary

if __name__ == "__main__":
    t5_summ = get_summary(
        "t5-base", "t5-base",
        min_length=50, max_length=500,
        truncation=True
    )
    print(f"{t5_summ=}")

    bart_summ = get_summary(
        "facebook/bart-base", "facebook/bart-base",
        min_length=50, max_length=500, truncation=True
    )
    print(f"{bart_summ=}")

    pe_summ = get_summary(
        "google/pegasus-xsum", "google/pegasus-xsum",
        min_length=50, max_length=500, truncation=True
    )
    print(f"{pe_summ=}")
