import sqlite3


def save_metadata(chunks, strategy):
    conn = sqlite3.connect("metadata.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY,
        chunk_text TEXT,
        strategy TEXT,
        words_count INTEGER
    )
    """)

    cursor.execute("DELETE FROM chunks")

    for i, chunk in enumerate(chunks):
        cursor.execute("""
        INSERT OR REPLACE INTO chunks (id, chunk_text, strategy, words_count)
        VALUES (?, ?, ?, ?)
        """, (i, chunk, strategy, len(chunk.split())))

    conn.commit()
    conn.close()


def get_chunk_count():

    conn = sqlite3.connect("metadata.db")

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM chunks")

    count = cursor.fetchone()[0]

    conn.close()

    return count