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
        print("Please upload a valid text-based PDF.")
        return ""

    return text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
if __name__ == "__main__":
    pdf_path = "data/resumes/sample_res.pdf"

    raw_text = extract_text_from_pdf(pdf_path)
    clean_resume_text = clean_text(raw_text)

    print("------ CLEAN RESUME TEXT ------\n")
    print(clean_resume_text)
