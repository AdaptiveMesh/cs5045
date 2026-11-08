"""
Module 12: Text Analytics & NLP
CS 5045: Computation for the Data Sciences
Virginia Tech: Applied Data Science MS Program

This script demonstrates text analytics operations on product reviews:
  - Represent:  load text data as structured columns in a DataFrame
  - Filter:     select reviews by rating, keyword presence, or sentiment
  - Transform:  clean text, tokenize, count words, assign sentiment labels
  - Aggregate:  compute word frequencies, average rating and sentiment by helpfulness group
  - Communicate: print summaries, display word counts, show top terms

Dataset: data.csv
  Columns: product, review_text, rating, verified_purchase, helpful_votes
"""

import pandas as pd
import re
from collections import Counter

# ── REPRESENT: Load the dataset ────────────────────────────────────────────────
# Represent: read the CSV into a DataFrame so Python can work with it
df = pd.read_csv("data.csv")

print("=== REPRESENT: Dataset Overview ===")
print(df.head())
print(f"\nShape: {df.shape[0]} reviews, {df.shape[1]} columns")
print(f"Products: {df['product'].unique()}")

# ── TRANSFORM: Clean and prepare the text ──────────────────────────────────────
# Transform: lowercase all review text so 'Great' and 'great' are treated as equal
df["review_clean"] = df["review_text"].str.lower()

# Transform: remove punctuation; keep only letters and spaces
df["review_clean"] = df["review_clean"].apply(
    lambda text: re.sub(r"[^a-z\s]", "", text)
)

print("\n=== TRANSFORM: Cleaned Review Text (first 3 rows) ===")
print(df[["review_text", "review_clean"]].head(3).to_string(index=False))

# TRANSFORM: Tokenize: split each review into individual words ──────────────
# Transform: split a string of text into a list of individual words (tokens)
df["tokens"] = df["review_clean"].str.split()

print("\n=== TRANSFORM: Tokens for first review ===")
print(df["tokens"].iloc[0])

# ── TRANSFORM: Define and remove stop words ───────────────────────────────────
# Transform: stop words are common words ('the', 'and', 'is') that carry
# little meaning. Removing them lets us focus on content-bearing words.
STOP_WORDS = {
    "the", "a", "an", "and", "is", "in", "it", "to", "for",
    "of", "my", "i", "at", "this", "very", "but", "after",
    "even", "are", "not", "do", "from", "be", "all", "have",
    "too", "was", "on", "up", "so", "one", "has", "me",
    "they", "get", "its", "that", "with", "what", "no"
}

# Transform: filter tokens within each review to remove stop words
df["tokens_filtered"] = df["tokens"].apply(
    lambda words: [w for w in words if w not in STOP_WORDS]
)

print("\n=== TRANSFORM: Filtered tokens for first review ===")
print("Before:", df["tokens"].iloc[0])
print("After: ", df["tokens_filtered"].iloc[0])

# ── AGGREGATE: Count word frequency across all reviews ────────────────────────
# Aggregate: collapse all token lists into a single frequency count
all_tokens = []
for token_list in df["tokens_filtered"]:
    all_tokens.extend(token_list)

word_counts = Counter(all_tokens)
top_words = word_counts.most_common(15)

print("\n=== AGGREGATE: Top 15 Words Across All Reviews ===")
for word, count in top_words:
    bar = "#" * count
    print(f"  {word:<20} {count:3d}  {bar}")

# ── TRANSFORM: Assign simple rule-based sentiment ─────────────────────────────
# Transform: create a new column that labels each review with a sentiment category
# based on the star rating; a common proxy when no sentiment labels exist
def assign_sentiment(rating):
    """Transform a numeric rating into a sentiment label."""
    if rating >= 4:
        return "positive"
    elif rating == 3:
        return "neutral"
    else:
        return "negative"

df["sentiment"] = df["rating"].apply(assign_sentiment)

print("\n=== TRANSFORM: Sentiment Labels Added ===")
print(df[["product", "rating", "sentiment"]].to_string(index=False))

# ── FILTER: Isolate negative reviews for deeper inspection ─────────────────────
# Filter: keep only reviews where sentiment is negative
negative_reviews = df[df["sentiment"] == "negative"]

print(f"\n=== FILTER: Negative Reviews ({len(negative_reviews)} of {len(df)}) ===")
print(negative_reviews[["product", "rating", "review_text"]].to_string(index=False))

# ── FILTER: Find reviews mentioning a specific keyword ────────────────────────
# Filter: keep only reviews whose cleaned text contains a keyword of interest
keyword = "battery"
keyword_reviews = df[df["review_clean"].str.contains(keyword)]

print(f"\n=== FILTER: Reviews Mentioning '{keyword}' ===")
print(keyword_reviews[["product", "rating", "review_text"]].to_string(index=False))

# ── AGGREGATE: Word frequency by sentiment category ───────────────────────────
# Aggregate: compute word frequency separately for positive vs. negative reviews
print("\n=== AGGREGATE: Top Words by Sentiment ===")
for sentiment_label in ["positive", "negative"]:
    subset = df[df["sentiment"] == sentiment_label]
    tokens_subset = []
    for token_list in subset["tokens_filtered"]:
        tokens_subset.extend(token_list)
    top_5 = Counter(tokens_subset).most_common(5)
    print(f"\n  {sentiment_label.upper()} reviews: top 5 words:")
    for word, count in top_5:
        print(f"    {word:<20} {count}")

# ── AGGREGATE: Average rating by helpfulness group ─────────────────────────────
# Aggregate: split reviews on the median helpful_votes, then compare average
# rating between the two groups; a groupby pattern that needs a derived
# group column first (product turns out to have identical ratings across
# all four categories in this dataset, so it will not show here)
median_votes = df["helpful_votes"].median()
df["votes_group"] = df["helpful_votes"].apply(
    lambda v: "above median" if v > median_votes else "at or below median"
)
avg_rating = df.groupby("votes_group")["rating"].mean().sort_values()

print(f"\n=== AGGREGATE: Average Rating by Helpfulness Group (median votes = {median_votes:.0f}) ===")
print(avg_rating.round(2).to_string())

# ── AGGREGATE: Sentiment distribution by helpfulness group ─────────────────────
# Aggregate: count how many positive, neutral, and negative reviews fall in
# each helpfulness group
sentiment_counts = df.groupby(["votes_group", "sentiment"]).size().unstack(fill_value=0)

print("\n=== AGGREGATE: Sentiment Distribution by Helpfulness Group ===")
print(sentiment_counts.to_string())

# ── COMMUNICATE: Final summary ─────────────────────────────────────────────────
# Communicate: present a clean, readable summary for a human audience
print("\n=== COMMUNICATE: Summary Report ===")
print(f"Total reviews analyzed:     {len(df)}")
print(f"Unique products reviewed:   {df['product'].nunique()}")
print(f"Positive reviews:           {(df['sentiment'] == 'positive').sum()}")
print(f"Neutral reviews:            {(df['sentiment'] == 'neutral').sum()}")
print(f"Negative reviews:           {(df['sentiment'] == 'negative').sum()}")
print(f"Most common word (content): {top_words[0][0]} ({top_words[0][1]} times)")
print(f"Avg rating, above-median helpful votes:      {avg_rating['above median']:.2f} stars")
print(f"Avg rating, at-or-below-median helpful votes: {avg_rating['at or below median']:.2f} stars")
