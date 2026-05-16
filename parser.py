import os
import pymupdf
import docx
def parse_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_pdf(path):
    pdf = pymupdf.open(path)
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

def parse_docx(path):
    doc = docx.Document(path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def parse_file(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        return parse_txt(path)

    elif ext == ".pdf":
        return parse_pdf(path)

    elif ext == ".docx":
        return parse_docx(path)

    else:
        return "Unsupported file type"     

def clean_text(text):

    text = text.replace("\n", " ")

    text = " ".join(text.split())

    return text


all_text = ""

files = [
    "Data/Ai.txt",
    "Data/rag.pdf",
    "Data/saudi.docx"
]

for file in files:

    text = parse_file(file)

    text = clean_text(text)

    all_text += text + "\n"

#print(all_text)
words = len(all_text.split())

paragraphs = len(all_text.split("\n"))
