import csv
import re
import nltk
from nltk.corpus import words

nltk.download('words')
english_words = set(words.words())


def is_proper_english_word(word):
    return word.lower() in english_words
def read_words_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            return text
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

text =read_words_from_file("pubmed-fnirs-set.txt")
fau_pattern = re.compile(r'FAU - ([\w\s,]+)')
au_pattern = re.compile(r'AU - ([\w\s,]+)')
ad_pattern = re.compile(r'AD  - ([\w\s,]+)')

# Extract authors and affiliations
authors = fau_pattern.findall(text)
author_initials = au_pattern.findall(text)
affiliations = ad_pattern.findall(text)

# Extract unique affiliations
unique_affiliations = {i: affiliations[i] for i in range(len(affiliations)) if affiliations[i]}

# Prepare data for CSV
data = []
for i, author in enumerate(authors):
    name_parts = author.split(', ')
    if len(name_parts) == 2:
        last_name, first_name = name_parts
    else:
        first_name, last_name = name_parts[0], ''

    affiliation = unique_affiliations.get(i, '').rsplit(', ', 1)
    if len(affiliation) == 2:
        institution, country = affiliation
    else:
        institution, country = affiliation[0], ''

    data.append({
        'First Name': first_name,
        'Last Name': last_name,
        'Affiliation': institution,
        'Country': country
    })
csv_file = 'exp.csv'

# Write data to CSV
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['First Name', 'Last Name', 'Affiliation', 'Country']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print(f"CSV file '{csv_file}' created successfully.")