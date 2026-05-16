import time

def run_benchmark(model, client, collection_name):
    benchmark_tests = [
        {"query": "ما هي عاصمة السعودية؟", "expected_word": "الرياض"},
        {"query": "What is RAG?", "expected_word": "Retrieval-Augmented"},
        {"query": "What is stored in vector databases?", "expected_word": "embeddings"},
        {"query": "What improves retrieval accuracy?", "expected_word": "chunking"},
        {"query": "What does Arabic support require?", "expected_word": "Unicode"},
        {"query": "What is used for semantic search?", "expected_word": "vector database"},
        {"query": "ما الذي تستخدمه السعودية ضمن رؤية 2030؟", "expected_word": "الذكاء الاصطناعي"},
        {"query": "What do RAG systems retrieve?", "expected_word": "documents"},
        {"query": "What is transformed into embeddings?", "expected_word": "chunks"},
        {"query": "ما هي استخدامات الذكاء الاصطناعي؟", "expected_word": "الرعاية الصحية"}
    ]

    passed = 0
    start_time = time.time()

    for test in benchmark_tests:
        query_embedding = model.encode(test["query"])

        results = client.query_points(
            collection_name=collection_name,
            query=query_embedding.tolist(),
            limit=3
        ).points

        retrieved_text = " ".join([r.payload["text"] for r in results])

        if test["expected_word"] in retrieved_text:
            passed += 1

    end_time = time.time()

    print("\nBenchmark Results")
    print("Passed:", passed, "/", len(benchmark_tests))
    print("Accuracy:", passed / len(benchmark_tests))
    print("Time:", round(end_time - start_time, 4), "seconds")

def chunk_quality_test(chunks):
    good_chunks = 0

    for chunk in chunks:
        if len(chunk.split()) >= 10:
            good_chunks += 1

    chunk_quality = good_chunks / len(chunks)

    print("\nChunking Quality Test")
    print("Good Chunks:", good_chunks, "/", len(chunks))
    print("Chunk Quality Score:", chunk_quality)

    if chunk_quality >= 0.8:
        print("Chunking Quality: PASSED")
    else:
        print("Chunking Quality: FAILED")