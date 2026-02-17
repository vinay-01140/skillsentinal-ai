import pandas as pd
import json
import re


def load_skills():

    with open("data/skills.json") as f:
        return json.load(f)


def normalize(text):

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " " + re.sub(r"\s+", " ", text) + " "


def extract_from_text(text, skill_dict):

    found = set()
    text = normalize(text)

    for skill, aliases in skill_dict.items():
        for a in aliases:
            if f" {a} " in text:
                found.add(skill)
                break

    return found


def main():

    skills = load_skills()

    df = pd.read_csv("data/job_market/job_postings.csv")

    clean_rows = []

    for _, row in df.iterrows():

        desc = str(row.get("description", ""))

        found = extract_from_text(desc, skills)

        for s in found:
            clean_rows.append(s)

    pd.DataFrame({"skill": clean_rows}) \
      .value_counts() \
      .reset_index(name="count") \
      .to_csv("data/job_market/clean_job_skills.csv", index=False)

    print("✅ Clean job skills created")


if __name__ == "__main__":
    main()
