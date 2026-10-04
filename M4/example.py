"""
Module 4: Data Structures
CS 5045: Computation for the Data Sciences
Virginia Tech | Instructor: Kurt Stein

Demonstrates Python's core data structures: lists, dictionaries, and tuples,
using a library book catalog dataset.

Run from the Code/ directory:
    python3 example.py
"""

import csv
import os

# ── REPRESENT: load the dataset from CSV ──────────────────────────────────────
# Represent = store information in a form the computer can work with.
# Here we read the CSV file into a list of dictionaries. Each row becomes
# one dictionary; each column name becomes a key.

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")

books = []
with open(DATA_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Convert numeric columns from string to the right types
        row["year"] = int(row["year"])
        row["pages"] = int(row["pages"])
        row["available"] = row["available"] == "True"
        books.append(row)

print("=" * 60)
print("REPRESENT: Book catalog loaded")
print(f"  Total books: {len(books)}")
print(f"  First book : {books[0]}")
print()

# ── REPRESENT: anatomy of a list ─────────────────────────────────────────────
# A list is an ordered sequence of values. Indexing starts at 0.

titles = [book["title"] for book in books]   # list comprehension: one title per book
print("List of titles (first 3):", titles[:3])
print("Last title (index -1)   :", titles[-1])
print()

# ── REPRESENT: anatomy of a dictionary ───────────────────────────────────────
# A dictionary maps keys to values. Keys are usually strings; values can be anything.
# Think: a dictionary is one row of a spreadsheet turned sideways.

first_book = books[0]
print("Dictionary: first book:")
for key, value in first_book.items():
    print(f"  {key:12s} → {value}")
print()

# ── REPRESENT: a tuple for a record that should not change ───────────────────
# Tuples are like lists but immutable; once created, they cannot be modified.
# Use them when the structure should stay fixed (e.g., coordinates, a catalog record).

book_record = (first_book["title"], first_book["author"], first_book["year"])
print("Tuple record (title, author, year):", book_record)
print("Title via index 0               :", book_record[0])
print()

# ── TRANSFORM: create a new field for each book ──────────────────────────────
# Transform = change values or create new ones.
# Here we add a "decade" key to each dictionary, derived from "year".

for book in books:
    book["decade"] = (book["year"] // 10) * 10    # e.g., 2019 → 2010

print("TRANSFORM: 'decade' column added")
print("  Sample: title, year, decade:")
for book in books[:4]:
    print(f"    {book['title'][:35]:35s} {book['year']}  →  {book['decade']}s")
print()

# ── TRANSFORM: normalise genre labels ────────────────────────────────────────
# Some genre labels need cleaning. Here we unify them into a short canonical form.

GENRE_MAP = {
    "Statistics": "Stats",
    "Social Science": "Social Sci",
    "Behavioral Economics": "Economics",
    "Psychology": "Psychology",
    "Mathematics": "Math",
    "Technology": "Tech",
    "History": "History",
    "Nature": "Nature",
    "Health": "Health",
}

for book in books:
    book["genre_short"] = GENRE_MAP.get(book["genre"], book["genre"])

print("TRANSFORM: 'genre_short' column added")
sample_genres = [(b["genre"], b["genre_short"]) for b in books[:5]]
for long, short in sample_genres:
    print(f"  {long:25s} → {short}")
print()

# ── REPRESENT: build an index dictionary ─────────────────────────────────────
# A dictionary can act as an index: map a key (title) to the full record.
# This is the same idea as a database index: look up by a unique identifier.

catalog_index = {book["title"]: book for book in books}

print("REPRESENT: catalog index (dict of dicts)")
looked_up = catalog_index["Factfulness"]
print(f"  Look up 'Factfulness': author={looked_up['author']}, year={looked_up['year']}")
print()

# ── REPRESENT: group books by genre using a dict of lists ────────────────────
# This is a very common pattern: aggregate books into buckets by category.

by_genre: dict = {}
for book in books:
    genre = book["genre_short"]
    if genre not in by_genre:
        by_genre[genre] = []          # start a new bucket
    by_genre[genre].append(book["title"])

print("REPRESENT: books grouped by genre (dict of lists)")
for genre, titles_list in sorted(by_genre.items()):
    print(f"  {genre:12s}: {titles_list}")
print()

# ── REPRESENT: ordered list of unique genres ──────────────────────────────────
# Sets let us collect unique values; we then sort them to get a stable order.

unique_genres = sorted(set(book["genre"] for book in books))
print("Unique genres (sorted list):", unique_genres)
print()

# ── TRANSFORM: build a summary list using list comprehension ─────────────────
# Produce a new list of (title, pages) tuples: only the fields we need.

page_data = [(book["title"], book["pages"]) for book in books]
print("TRANSFORM: page_data list (title, pages): first 5:")
for title_str, pages in page_data[:5]:
    print(f"  {title_str[:40]:40s}  {pages} pp")
print()

# ── REPRESENT / COMMUNICATE: final summary ───────────────────────────────────
print("=" * 60)
print("Summary of data structures used:")
print(f"  list of dicts : {len(books)} books")
print(f"  index dict    : {len(catalog_index)} entries")
print(f"  genre groups  : {len(by_genre)} genres")
print(f"  unique genres : {unique_genres}")
