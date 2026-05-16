def fixed_chunk(text, chunk_size=50, overlap=10):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

def dynamic_chunk(text):
    chunks = []
    paragraphs = text.split("\n")

    for para in paragraphs:
        para = para.strip()
        if para:
            chunks.append(para)

    return chunks

def choose_chunking_strategy(paragraphs, all_text):

    if paragraphs > 10:

        strategy = "dynamic"

        chunks = dynamic_chunk(all_text)

    else:

        strategy = "fixed"

        chunks = fixed_chunk(all_text)

    return strategy, chunks