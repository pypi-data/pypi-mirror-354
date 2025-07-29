# langxchange/db_tool.py

import os
import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import sqlalchemy
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

import pymongo
from pymongo.errors import PyMongoError


class DbTool:
    """
    Unified tool for relational and NoSQL DBs with schema stored in a vector store.
    Automatically selects relevant tables/collections, generates queries via LLM,
    executes them, and returns results + context.
    """

    def __init__(
        self,
        llm: Any,
        vector_db: Any,
        embedder: Any,
        connection_string: Optional[str] = None,
        docs_dir: str = "db_docs",
        schema_collection: str = "__schema__",
        schema_top_k: int = 5
    ):
        """
        :param llm: OpenAIHelper (or similar) for chat()
        :param vector_db: a vector store helper with .insertone(df, collection_name) and .query(...)
        :param embedder: embedding helper with .embed(texts)
        :param connection_string: SQLAlchemy URI or MongoURI
        :param docs_dir: where to persist example_queries.json
        :param schema_collection: name of the collection in vector_db to hold schema docs
        :param schema_top_k: how many schema entries to retrieve per query
        """
        self.llm = llm
        self.vector_db = vector_db
        self.embedder = embedder
        self.conn_str = connection_string or os.getenv("DB_URI")
        if not self.conn_str:
            raise EnvironmentError("DB_URI must be set for relational or mongodb URI")

        self.docs_dir = Path(docs_dir)
        self.docs_dir.mkdir(exist_ok=True, parents=True)
        self.examples_path = self.docs_dir / "example_queries.json"
        self.schema_collection = schema_collection
        self.schema_top_k = schema_top_k

        # DB connection
        if self.conn_str.startswith("mongodb"):
            self.is_nosql = True
            self.mongo_client = pymongo.MongoClient(self.conn_str)
            db_name = self.conn_str.rsplit("/", 1)[-1]
            self.mongo_db = self.mongo_client[db_name]
        else:
            self.is_nosql = False
            self.engine: Engine = sqlalchemy.create_engine(self.conn_str)
            self.inspector = inspect(self.engine)

        self._schema_cache: Optional[Dict[str, Any]] = None
        self._examples_cache: Optional[Dict[str, Any]] = None

    def introspect_schema(self) -> Dict[str, Any]:
        """
        Inspect the database schema (tables or collections). 
        If the vector‐DB collection (self.schema_collection) already exists, prompt the user 
        before overwriting. By default, skip and return existing cache (or empty dict if first run).
        """
        # 1) If we've already done introspection in this session, just return the cache
        if self._schema_cache is not None:
            return self._schema_cache

        # 2) Check if the schema_collection already exists in vector_db
        existing_count = 0
        try:
            existing_count = self.vector_db.get_collection_count(self.schema_collection)
        except Exception:
            existing_count = 0

        if existing_count > 0:
            # Skip introspection entirely and return an empty or previously cached schema
            print("Skipping introspection; keeping existing schema in vector store.")
            self._schema_cache = {}  # No new schema loaded in this run
            return self._schema_cache
            # resp = input(
            #     f"⚠️  The vector‐DB collection '{self.schema_collection}' "
            #     f"already contains {existing_count} schema documents.\n"
            #     "Would you like to overwrite (re‐index) it? [y/N]: "
            # ).strip().lower()
            # if resp != "y":
            #     # Skip introspection entirely and return an empty or previously cached schema
            #     print("Skipping introspection; keeping existing schema in vector store.")
            #     self._schema_cache = {}  # No new schema loaded in this run
            #     return self._schema_cache

        # 3) Build the in‐memory schema dictionary from the live database
        schema: Dict[str, Any] = {}
        if self.is_nosql:
            for coll in self.mongo_db.list_collection_names():
                sample = self.mongo_db[coll].find_one() or {}
                schema[coll] = list(sample.keys())
        else:
            for table in self.inspector.get_table_names():
                cols = [f"{c['name']} ({c['type']})" for c in self.inspector.get_columns(table)]
                schema[table] = cols

        # 4) Convert each table/collection schema into a text document
        docs = []
        for name, cols in schema.items():
            label = "Collection" if self.is_nosql else "Table"
            text_body = f"{label} `{name}` has fields:\n- " + "\n- ".join(cols)
            docs.append({"schema_name": name, "schema_text": text_body})

        # 5) Build a DataFrame of schema docs and embed them
        import pandas as pd
        df = pd.DataFrame(docs)
        df["documents"] = df["schema_text"]
        df["metadata"] = df[["schema_name"]].to_dict(orient="records")
        embeddings = self.embedder.embed(df["documents"].tolist())
        df["embeddings"] = embeddings

        # 6) Overwrite any existing schema collection in vector_db
        try:
            self.vector_db.delete_persistence(self.schema_collection, None)
        except Exception:
            pass

        # 7) Insert new schema documents into vector_db
        self.vector_db.insertone(df[["documents", "metadata", "embeddings"]], self.schema_collection)

        # 8) Cache and return the newly built schema
        self._schema_cache = schema
        return schema


    # def introspect_schema(self) -> Dict[str, Any]:
    #     if self._schema_cache is not None:
    #         return self._schema_cache

    #     schema: Dict[str, Any] = {}
    #     if self.is_nosql:
    #         for coll in self.mongo_db.list_collection_names():
    #             sample = self.mongo_db[coll].find_one() or {}
    #             schema[coll] = list(sample.keys())
    #     else:
    #         for table in self.inspector.get_table_names():
    #             cols = [f"{c['name']} ({c['type']})" for c in self.inspector.get_columns(table)]
    #             schema[table] = cols

    #     # # Persist examples JSON if missing
    #     # if not self.examples_path.exists():
    #     #     self.examples_path.write_text(json.dumps({}, indent=2))

    #     # Store schema docs in vector DB
    #     docs = []
    #     for name, cols in schema.items():
    #         text = f"{'Collection' if self.is_nosql else 'Table'} `{name}` has fields:\n- " + "\n- ".join(cols)
    #         docs.append({"schema_name": name, "schema_text": text})
    #     # build DataFrame
    #     import pandas as pd
    #     df = pd.DataFrame(docs)
    #     df["documents"] = df["schema_text"]
    #     df["metadata"] = df[["schema_name"]].to_dict(orient="records")
    #     embeddings = self.embedder.embed(df["documents"].tolist())
    #     df["embeddings"] = embeddings

    #     # insert into vector_db (overwrite existing collection)
    #     try:
    #         self.vector_db.delete_persistence(self.schema_collection, None)
    #     except Exception:
    #         pass
    #     self.vector_db.insertone(df[["documents", "metadata", "embeddings"]], self.schema_collection)

    #     self._schema_cache = schema
    #     return schema

    def load_examples(self) -> Dict[str, Any]:
        if self._examples_cache is not None:
            return self._examples_cache
        self._examples_cache = json.loads(self.examples_path.read_text())
        return self._examples_cache

    def generate_query(self, user_request: str) -> Tuple[List[str], Any]:
        """
        1) Retrieve top-k relevant schema entries via vector DB
        2) Ask the LLM to output JSON: {"tables": [...], "sql": "..."}
        """
        schema = self.introspect_schema()
        examples = self.load_examples()
        # embed and retrieve
        q_emb = self.embedder.embed([user_request])[0]
        hits = self.vector_db.query(self.schema_collection, q_emb, top_k=self.schema_top_k)
        print(hits)
        # Normalize "hits" into a list of metadata‐dicts called `metadatas`
        if isinstance(hits, dict):
            # ChromaHelper returns a dict with keys "metadatas", "documents", etc.
            raw_mds = hits.get("metadatas", [])
        else:
            # FAISSHelper returns a plain list of dicts, each containing a "metadata" key
            raw_mds = []
            for item in hits:
                # item might be a dict with key "metadata" or it might be a list; handle both
                if isinstance(item, dict) and "metadata" in item:
                    raw_mds.append(item["metadata"])
                elif isinstance(item, dict) and "metadatas" in item:
                    # in case some custom wrapper used "metadatas"
                    raw_mds.extend(item["metadatas"])
                else:
                    # as a last resort, treat the entire item as metadata if it's a dict
                    if isinstance(item, dict):
                        raw_mds.append(item)
                    # if item is a list or something else, skip it
                    # (we only care about dict‐shaped metadata)
        
        # Now extract schema_name from each metadata dict, if present
        chosen_names: List[str] = []
        for md in raw_mds:
            if isinstance(md, dict):
                name = md.get("schema_name") or md.get("schemaName") or md.get("schema") 
                # try a few common keys; adjust if you used a different field name
                if name and isinstance(name, str):
                    chosen_names.append(name)
        
        
            # if md is not a dict, skip it entirely
        # chosen = [m["schema_name"] for m in hits.get("metadatas", hits)]  # support both helpers
        system_prompt = (f"""You are an expert SQL generator.
             Given a small subset of table schemas (with column lists) {str(hits)} and example queries {examples}, 
             produce a single, valid SQL statement that answers the user's request,
             Output only the SQL—no explanations, no comments, no markdown.""")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_request}
        ]
        resp = self.llm.chat(messages=messages, temperature=0.7, max_tokens=512)
        return resp



    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """
        Run the generated SQL against the database.
        Ensures that `sql` is a non‐empty string and passes it through `text(...)` before executing.
        """
        if self.is_nosql:
            raise NotImplementedError("Automatic NoSQL generation not yet supported")

        # 1) Sanity check: ensure `sql` is a string
        if not isinstance(sql, str):
            raise RuntimeError(f"[❌ ERROR] Expected SQL string, got {type(sql).__name__!r} instead")

        sql = sql.strip()
        if not sql:
            raise RuntimeError("[❌ ERROR] SQL string is empty after stripping whitespace")

        # 2) Wrap the SQL in a TextClause
        try:
            stmt = text(sql)
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Could not prepare SQLAlchemy text() from SQL: {e}")

        # 3) Execute and fetch results
        try:
            with self.engine.connect() as conn:
                result = conn.execute(stmt)

                if result.returns_rows:
                    # Use .mappings() to get each row as a real dict
                    rows = result.mappings().all()
                else:
                    # DML/DDL (INSERT/UPDATE/DELETE): commit and return empty list
                    conn.commit()
                    rows = []

                return rows

        except SQLAlchemyError as e:
            # Include the SQL in the error message for easier debugging
            raise RuntimeError(f"[❌ ERROR] SQL execution failed for:\n{sql}\nError: {e}")




    
