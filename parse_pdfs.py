from PyPDF2 import PdfReader
import os
import json
import re
from collections import defaultdict

def extract_topic_questions(pdf_path):
    reader = PdfReader(pdf_path)
    text = "".join(page.extract_text() for page in reader.pages)
    
    # Normalize text
    text = re.sub(r'\s*\n\s*', ' ', text)
    
    # Find all topics and their questions
    topic_blocks = re.split(r'Topic(?:\s*\d*):', text, flags=re.I)[1:]
    topic_map = defaultdict(list)

    for block in topic_blocks:
        parts = re.split(r'\s*\d{1,2}\.\s*', block)
        if len(parts) < 2:
            continue
            
        topic = parts[0].strip()
        questions = [q.strip() for q in parts[1:] if q.strip()]
        
        # Clean up questions from year markers
        cleaned_questions = []
        for q in questions:
            q = re.sub(r'\s*\(\d{4}\)\s*$', '', q)  # Remove year at the end
            q = re.sub(r'^\s*Year:\s*\d{4}\s*\|?\s*', '', q) # Remove year at the beginning
            cleaned_questions.append(q.strip())

        topic_map[topic].extend(cleaned_questions)
        
    return topic_map

# ✅ Automatically detect PDFs inside pyq_data
input_dir = "pyq_data"
if not os.path.exists(input_dir) or not os.listdir(input_dir):
    print(f"⚠️ Directory '{input_dir}' is empty or does not exist. Skipping PDF processing.")
    # Create an empty chunks.json if it doesn't exist
    if not os.path.exists("data/chunks.json"):
        os.makedirs("data", exist_ok=True)
        with open("data/chunks.json", "w") as f:
            json.dump([], f)
    exit()

input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]

final_topic_map = defaultdict(list)

for file in input_files:
    print(f"🔍 Processing: {file}")
    topic_map = extract_topic_questions(file)
    for topic, questions in topic_map.items():
        final_topic_map[topic].extend(questions)

# 📝 Save result
grouped_output = [
    {"topic": topic, "questions": questions}
    for topic, questions in final_topic_map.items()
]

os.makedirs("data", exist_ok=True)
with open("data/chunks.json", "w") as f:
    json.dump(grouped_output, f, indent=2)

print(f"✅ Extracted {sum(len(qs) for qs in final_topic_map.values())} questions across {len(final_topic_map)} topics.")
