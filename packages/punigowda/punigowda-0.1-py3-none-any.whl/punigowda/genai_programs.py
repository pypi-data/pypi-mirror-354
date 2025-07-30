def print_genai_programs(n):
    programs = {
        1: ''' import gensim.downloader as api
 # Load pre-trained model
 model = api.load("glove-wiki-gigaword-50")
 # Example words
 word1 = "king"
 word2 = "man"
 word3 = "woman"
 # Performing vector arithmetic
 result_vector = model[word1]- model[word2] + model[word3]
 predicted_word = model.most_similar([result_vector], topn=2)
 print(f"Result of '{word1}- {word2} + {word3}' is: {predicted_word[1][0]}")''',
        2: '''import gensim.downloader as api
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np

model = api.load("glove-wiki-gigaword-50")
words = ["computer", "internet", "software", "hardware", "disk", 
         "robot", "data", "network", "cloud", "algorithm"]

vectors = PCA(n_components=2).fit_transform([model[w] for w in words])

plt.figure(figsize=(8, 6))
for word, (x, y) in zip(words, vectors):
    plt.scatter(x, y)
    plt.annotate(word, (x, y))
plt.title("PCA of Technology Word Embeddings")
plt.xlabel("PC 1")
plt.ylabel("PC 2")
plt.show()

input_word = "computer"
print(f"Words similar to '{input_word}':", model.most_similar(input_word, topn=5))
''',
        3: '''import gensim
from gensim.models import Word2Vec
import nltk
from nltk.tokenize import word_tokenize

corpus = [
    "A patient with diabetes requires regular insulin injections.",
    "Medical professionals recommend exercise for heart health.",
    "Doctors use MRI scans to diagnose brain disorders.",
    "Antibiotics help fight bacterial infections but not viral infections.",
    "The surgeon performed a complex cardiac surgery successfully.",
    "Doctors and nurses work together to treat patients.",
    "A doctor specializes in diagnosing and treating diseases."
]

tokenized_corpus = [word_tokenize(sentence.lower()) for sentence in corpus]

model = Word2Vec(sentences=tokenized_corpus, vector_size=100, window=3, min_count=1, workers=4, sg=1)

model.save("medical_word2vec.model")

similar_words = model.wv.most_similar("doctor", topn=5)

print("Top 5 words similar to 'doctor':")
print(similar_words)
l''',
        4: '''from transformers import pipeline
import gensim.downloader as api

glove_model = api.load("glove-wiki-gigaword-50")

word = "technology"
similar_words = glove_model.most_similar(word, topn=5)
print(f"Similar words to '{word}': {similar_words}")

generator = pipeline("text-generation", model="gpt2")

def generate_response(prompt, max_length=100):
    response = generator(prompt, max_length=max_length, num_return_sequences=1)
    return response[0]['generated_text']

original_prompt = "Explain the impact of technology on society."
original_response = generate_response(original_prompt)

enriched_prompt = "Explain the impact of technology, innovation, science, engineering, and digital advancements on society."
enriched_response = generate_response(enriched_prompt)

print("Original Prompt Response:")
print(original_response)

print("\\nEnriched Prompt Response:")
print(enriched_response)
''',
        5: '''import gensim.downloader as api

# Load GloVe model
model = api.load("glove-wiki-gigaword-50")

# Function to create an easy paragraph
def construct_easy_paragraph(seed_word, similar_words):
    paragraph = (
        f"{seed_word.capitalize()} is fun and exciting. It can start with a {similar_words[0][0]} to new places. "
        f"Each {similar_words[1][0]} brings something new to learn. "
        f"{similar_words[2][0].capitalize()} helps us grow and see the world in a different way. "
        f"In the end, every {seed_word} feels like a special {similar_words[3][0]}."
    )
    return paragraph

# Use "adventure" as the seed word
seed_word = "adventure"
similar_words = model.most_similar(seed_word, topn=4)

# Generate and print paragraph
paragraph = construct_easy_paragraph(seed_word, similar_words)
print(paragraph)
''',
        6: '''from transformers import pipeline

# Load the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# Example sentences
sentences = [
    "I love this product! It works perfectly.",
    "This is the worst experience I've ever had.",
    "The weather is nice today.",
    "I feel so frustrated with this service."
]

# Analyze sentiment for each sentence
results = sentiment_pipeline(sentences)

# Print the results
for sentence, result in zip(sentences, results):
    print(f"Sentence: {sentence}")
    print(f"Sentiment: {result['label']}, Confidence: {result['score']:.4f}")
    print()
''',
        7: '''from transformers import pipeline

summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

passage = """Machine learning is a subset of artificial intelligence that focuses on training algorithms
to make predictions. It is widely used in industries like healthcare, finance, and retail."""

summary = summarizer(passage, max_length=30, min_length=10, do_sample=False)

print("Summary:")
print(summary[0]['summary_text'])
''',
        8: '''import os
from cohere import Client
from langchain.prompts import PromptTemplate

co = Client("eN25fsIQZKr5mMM8VnxQMOw7bSH25SH0hClnkCwK")

with open("dontpad->puni.txt", "r", encoding="utf-8") as f:
    text = f.read()

prompt = PromptTemplate(input_variables=["text"], template="Summarize this:\n{text}\nSummary:").format(text=text)
res = co.generate(model="command", prompt=prompt, max_tokens=50)

print("Summary:\n", res.generations[0].text.strip())''',
        9: '''import wikipedia
import json
from pydantic import BaseModel

# Define the schema
class InstitutionInfo(BaseModel):
    name: str
    founder: str = "Not found"
    founding_year: str = "Not found"
    branches: str = "Not found"
    employees: str = "Not found"
    summary: str

# Simple string-based extractor
def extract_info(name):
    try:
        page = wikipedia.page(name)
        content = page.content
        summary = wikipedia.summary(name, sentences=2)

        lines = content.split('\n')  # split into lines for easy scanning
        founder = year = branches = employees = "Not found"

        for line in lines:
            line_lower = line.lower()
            if "founder" in line_lower and founder == "Not found":
                founder = line
            elif "founded" in line_lower and year == "Not found":
                year = line
            elif "branch" in line_lower and branches == "Not found":
                branches = line
            elif "employee" in line_lower and employees == "Not found":
                employees = line

        return InstitutionInfo(
            name=name,
            founder=founder,
            founding_year=year,
            branches=branches,
            employees=employees,
            summary=summary
        )
    except Exception as e:
        print("Error:", e)
        return None

# Run the extractor
name = input("Enter institution name: ")
info = extract_info(name)
if info:
    print(json.dumps(info.model_dump(), indent=2))''',
        10: '''import fitz  # PyMuPDF
import re

doc = fitz.open("download ipc.pdf from google")
text = "".join(doc.load_page(i).get_text() for i in range(5, 50))
sections = dict(re.findall(r'(\d{1,4})\.\s+([A-Z][^\n\.]+)', text))

# IPC Bot
def ipc_bot(q):
    q = q.lower()
    if m := re.search(r'section\s*(\d+)', q):
        return sections.get(m.group(1), "No match.")
    for num, heading in sections.items():
        if any(word in heading.lower() for word in q.split()):
            return f"Section {num}: {heading}"
    return "No match."

# Chat loop
print("IPC Bot is ready. Type 'exit' to quit.\n")
while (q := input("You: ")).lower() not in ["exit", "quit"]:
    print("IPC Bot:", ipc_bot(q))'''
    }

    if n in programs:
        print(programs[n])
    else:
        print("Invalid program number. Please choose between 1 and", len(programs))
