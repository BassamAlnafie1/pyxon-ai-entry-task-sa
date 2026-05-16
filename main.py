from parser import parse_file, clean_text
import chunking
from vector_store import setup_qdrant, create_embeddings, save_to_qdrant
from sql_store import save_metadata
from benchmark import run_benchmark, chunk_quality_test
from rag import retrieve_chunks
from rag import build_context
from rag import generate_answer
from rag import prepare_llm_prompt
from sql_store import get_chunk_count   
files = [
    "Data/Ai.txt",
    "Data/rag.pdf",
    "Data/saudi.docx"
]

all_text = ""

for file in files:
    text = parse_file(file)
    text = clean_text(text)
    all_text += text + "\n"

words = len(all_text.split())
paragraphs = len(all_text.split("\n"))

print("Words:", words)
print("Paragraphs:", paragraphs)

strategy, chunks = chunking.choose_chunking_strategy(
    paragraphs,
    all_text
)

print("Chunking Strategy:", strategy)
print("Number of Chunks:", len(chunks))

client, collection_name = setup_qdrant()

model, embeddings = create_embeddings(chunks)

save_to_qdrant(client, collection_name, chunks, embeddings)

print("Embeddings saved to Qdrant")
print("Number of embeddings:", len(embeddings))
print("Embedding size:", len(embeddings[0]))

save_metadata(chunks, strategy)

print("Metadata saved to SQLite")

arabic_diacritics = "المَمْلَكَةُ العَرَبِيَّةُ السُّعُودِيَّةُ"
print("\nArabic Diacritics Test:")
print(arabic_diacritics)

run_benchmark(model, client, collection_name)

chunk_quality_test(chunks)
query = "ما هي عاصمة السعودية؟"

retrieved_chunks = retrieve_chunks(
    query,
    model,
    client,
    collection_name
)

print("\nRetrieved Chunks:")

for chunk in retrieved_chunks:
    print(chunk)
    print("-" * 50)

context = build_context(retrieved_chunks)

print("\nContext:\n")
print(context)

prompt = prepare_llm_prompt(query, context)
print("\nLLM Prompt:\n")
print(prompt)

count = get_chunk_count()
print("\nTotal Chunks in SQLite:", count)
