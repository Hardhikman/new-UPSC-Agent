import json, re

directives = ["Discuss", "Analyze", "Evaluate", "Examine", "Justify"]
subjects = {
    "Polity": ["parliament", "constitution", "federalism", "governance"],
    "History": ["freedom", "british", "movement"],
    "Geography": ["climate", "river", "disaster"],
    "Society": ["gender", "caste", "education"],
    "Economy": ["budget", "gdp", "inflation"],
    "Ethics": ["ethics", "attitude", "integrity"]
}

with open("data/chunks.json") as f:
    raw = json.load(f)  # Load questions

tagged = []
for q in raw:
    qn = re.match(r"Q(\d+)", q)  # Match question number
    marks = 10 if qn and int(qn.group(1)) <= 10 else 15
    # This finds the first matching directive keyword in the question text, defaulting to 'Unknown' if none are found.
    directive = next((d for d in directives if d.lower() in q.lower()), "Unknown")
    subject = "Unknown"
    for s, kws in subjects.items():
        if any(k in q.lower() for k in kws):
            subject = s
            break
    tagged.append({"question": q, "marks": marks, "directive": directive, "subject": subject})

with open("data/tagged_questions.json", "w") as f:
    json.dump(tagged, f, indent=2)