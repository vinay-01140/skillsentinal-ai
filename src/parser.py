import pdfplumber
import re
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print("Error reading PDF:", e)
        return ""
    return text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
def parse_resume(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    clean_resume_text = clean_text(raw_text)
    return clean_resume_text
if __name__ == "__main__":

    pdf_path = "data/resumes/sample_res.pdf"

    text = parse_resume(pdf_path)

    print("----- CLEANED RESUME TEXT -----")
    print(text[:1000])   # print first 1000 characters
    print("--------------------------------")