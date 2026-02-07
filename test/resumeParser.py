import pymupdf
import re

def resume_to_string(resume: str)-> str:
    out = pymupdf.open(resume)
    text = []
    for page in out: # iterate the document pages
        text.append(page.get_text()) # get plain text
    out.close()
    return "".join(text)

def clean_raw_text(raw_text):
    # 1. Decode byte strings if they appear as b'...'
    if isinstance(raw_text, bytes):
        raw_text = raw_text.decode('utf-8')
    
    # 2. Remove non-ASCII/Hex escape sequences (like \xe2\x97\x8f)
    # This specifically targets those bullet point artifacts
    cleaned = raw_text.encode("ascii", "ignore").decode()

    # 3. Replace multiple newlines or tabs with a single space
    cleaned = re.sub(r'[\t\r\n]+', ' ', cleaned)

    # 4. Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned

def parse_resume(resume: str) -> str:
    text = resume_to_string(resume)
    cleaned_text = clean_raw_text(text)
    return cleaned_text
