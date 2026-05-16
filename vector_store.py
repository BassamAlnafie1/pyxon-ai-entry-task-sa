from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

def setup_qdrant():
    client = QdrantClient(":memory:")
    collection_name = "documents"

    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    return client, collection_name

def create_embeddings(chunks):
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    embeddings = model.encode(chunks)
    return model, embeddings

def save_to_qdrant(client, collection_name, chunks, embeddings):
    points = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        point = PointStruct(
            id=i,
            vector=embedding.tolist(),
            payload={"text": chunk}
        )
        points.append(point)

    client.upsert(
        collection_name=collection_name,
        points=points
    )