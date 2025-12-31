import json
import re


def load_skill_dictionary(path="data/skills.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_skills(clean_text, skill_dict):
    found_skills = set()
    text = f" {clean_text} "

    for standard_skill, aliases in skill_dict.items():
        for alias in aliases:
            alias = f" {alias} "
            if alias in text:
                found_skills.add(standard_skill)
                break

    return list(found_skills)


# -------- TEST BLOCK --------
if __name__ == "__main__":
    sample_text = """
    experienced in python, ml, reactjs, sql and cloud computing
    """

    clean_text = normalize_text(sample_text)

    skills = load_skill_dictionary()
    extracted = extract_skills(clean_text, skills)

    print("Extracted Skills:")
    print(extracted)
