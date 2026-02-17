import json

def load_skill_dictionary(path="data/skills.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
def extract_skills(clean_text, skill_dict):
    resume_skills = {}
    text = f" {clean_text} "

    for standard_skill, aliases in skill_dict.items():
        resume_skills[standard_skill] = False
        for alias in aliases:
            if f" {alias} " in text:
                resume_skills[standard_skill] = True
                break
    return resume_skills
if __name__ == "__main__":
    pdf_path = "data/resumes/sample_res.pdf"
    clean_resume_text = parse_resume(pdf_path)
    skill_dict = load_skill_dictionary()
    extracted_skills = extract_skills(clean_resume_text, skill_dict)
    print("Extracted Resume Skills:\n")
    for skill, present in extracted_skills.items():
        if present:
            print("✔", skill)
