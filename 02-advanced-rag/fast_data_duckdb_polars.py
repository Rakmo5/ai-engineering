"""
Advanced Elective 3: High-Performance Data Ingestion with DuckDB & Polars
Demonstrates how top AI engineers prepare, filter, and chunk massive datasets
(Parquet, JSONL) at 10x-50x the speed of pandas before generating vector embeddings.
"""

import time
import os

def demonstrate_duckdb_sql():
    """
    DuckDB is an in-process columnar SQL OLAP database.
    It can query remote or local Parquet, CSV, and JSON files directly without loading
    them entirely into RAM.
    """
    try:
        import duckdb
        print("--- 1. DuckDB In-Memory Analytical Pipeline ---")
        
        # Connect in-memory
        con = duckdb.connect(database=':memory:')
        
        # Create a mock knowledge-base corpus (e.g. 50,000 documents)
        con.execute("""
            CREATE TABLE knowledge_base AS 
            SELECT 
                range AS doc_id,
                'Engineering document #' || range AS title,
                'Lorem ipsum dolor sit amet, chunk data for system ' || (range % 100) AS content,
                CASE WHEN range % 2 = 0 THEN 'technical' ELSE 'compliance' END AS department,
                random() * 100 AS access_tier
            FROM range(50000);
        """)
        
        start = time.time()
        # Fast SQL aggregation and filtering before embedding generation
        result = con.execute("""
            SELECT department, COUNT(*) as count, AVG(access_tier) as avg_tier
            FROM knowledge_base
            WHERE access_tier > 25.0
            GROUP BY department
        """).fetchall()
        elapsed = time.time() - start
        
        print(f"Aggregated 50,000 rows in: {elapsed*1000:.2f} ms")
        print("Result:", result)
        
    except ImportError:
        print("[DuckDB Note] Install via: pip install duckdb")

def demonstrate_polars_laziness():
    """
    Polars is a blazingly fast multi-threaded DataFrame library written in Rust.
    Its LazyFrame API optimizes the query plan before executing.
    """
    try:
        import polars as pl
        print("\n--- 2. Polars Lazy Execution Pipeline ---")
        
        # Create Lazy DataFrame
        data = {
            "chunk_id": list(range(10000)),
            "text": [f"Sample passage for vector embedding chunk {i}" for i in range(10000)],
            "char_count": [len(f"Sample passage for vector embedding chunk {i}") for i in range(10000)]
        }
        
        start = time.time()
        df = pl.DataFrame(data).lazy()
        
        # Define transformation pipeline (zero computation happens here)
        query = (
            df.filter(pl.col("char_count") > 20)
              .with_columns(
                  (pl.col("char_count") / 4).alias("estimated_tokens")
              )
              .select(["chunk_id", "char_count", "estimated_tokens"])
        )
        
        # Execute in parallel with Rust backend
        result_df = query.collect()
        elapsed = time.time() - start
        
        print(f"Polars processed 10,000 rows in: {elapsed*1000:.2f} ms")
        print(result_df.head(3))
        
    except ImportError:
        print("[Polars Note] Install via: pip install polars")

if __name__ == "__main__":
    print("Testing High-Speed Data Pipelines (DuckDB & Polars)...\n")
    demonstrate_duckdb_sql()
    demonstrate_polars_laziness()
