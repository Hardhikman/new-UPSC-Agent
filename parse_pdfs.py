from PyPDF2 import PdfReader
import os
import json
import re

def extract_english_questions_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    english_lines = [line for line in lines if not re.search(r'[\u0900-\u097F]', line)]

    questions = []
    current_question = ""
    for line in english_lines:
        if re.match(r'^\d{1,2}\.', line):
            if current_question:
                questions.append(current_question.strip())
            current_question = line
        else:
            current_question += " " + line
    if current_question:
        questions.append(current_question.strip())
    return questions

# Directory containing bilingual PDFs
input_dir = "pyq_data"
output_path = "data/chunks.json"

all_questions = []

# Loop through PDF files in input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith(".pdf"):
        full_path = os.path.join(input_dir, filename)
        pdf_questions = extract_english_questions_from_pdf(full_path)
        all_questions.extend(pdf_questions)

# Save all extracted English questions to JSON
os.makedirs("data", exist_ok=True)
with open(output_path, "w") as f:
    json.dump(all_questions, f, indent=2)

print(f"✅ Extracted {len(all_questions)} English questions from PDFs.")
