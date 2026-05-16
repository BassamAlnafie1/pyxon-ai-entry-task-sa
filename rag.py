def retrieve_chunks(query, model, client, collection_name, top_k=3):
    query_embedding = model.encode(query)

    results = client.query_points(
        collection_name=collection_name,
        query=query_embedding.tolist(),
        limit=top_k
    ).points

    chunks = []

    for result in results:
        chunks.append(result.payload["text"])

    return chunks
def build_context(chunks):

    context = "\n\n".join(chunks)

    return context

def generate_answer(query, context):

    answer = f"""
    Question:
    {query}

    Answer Based On Retrieved Context:
    {context}
    """

    return answer

def prepare_llm_prompt(query, context):

    prompt = f"""
Answer the question using the context below.

Question:
{query}
Context:
{context}
Answer:
"""

    return prompt    