import streamlit as st
import tempfile

from parser import parse_file, clean_text
from chunking import fixed_chunk, dynamic_chunk
from vector_store import setup_qdrant, create_embeddings, save_to_qdrant
from rag import retrieve_chunks, build_context, prepare_llm_prompt
from sql_store import save_metadata

st.title("IntelliParse AI")

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf", "docx", "txt"]
)

chunking_strategy = st.selectbox(
    "Choose chunking strategy",
    ["fixed", "dynamic"]
)

query = st.text_input("Ask a question about the document")

if uploaded_file is not None:
    suffix = "." + uploaded_file.name.split(".")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name

    text = parse_file(file_path)
    text = clean_text(text)

    st.subheader("Document Analysis")
    st.write("Words:", len(text.split()))
    st.write("Characters:", len(text))

    if chunking_strategy == "fixed":
        chunks = fixed_chunk(text)
    else:
        chunks = dynamic_chunk(text)

    st.write("Number of Chunks:", len(chunks))

    client, collection_name = setup_qdrant()
    model, embeddings = create_embeddings(chunks)
    save_to_qdrant(client, collection_name, chunks, embeddings)
    save_metadata(chunks, chunking_strategy)

    st.success("Document processed successfully")

    if query:
        retrieved_chunks = retrieve_chunks(
            query,
            model,
            client,
            collection_name
        )

        context = build_context(retrieved_chunks)
        prompt = prepare_llm_prompt(query, context)

        st.subheader("Retrieved Chunks")
        for chunk in retrieved_chunks:
            st.write(chunk)
            st.divider()

      
