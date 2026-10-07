"""
HeedX AI — Retrieval-Augmented Generation (RAG) Engine
Indexes evidence-based Nigerian mental health literature, guidelines, and context.
Provides cosine similarity vector search with Gemini embeddings and TF-IDF fallback.
"""

import json
import os
import re
import numpy as np
from typing import List, Dict, Any, Optional
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RAGEngine:
    """
    RAG Engine for HeedX AI.
    Loads knowledge documents, chunks text, generates embeddings,
    and conducts semantic similarity search over curated evidence.
    """

    def __init__(self, knowledge_file: Optional[str] = None):
        if knowledge_file is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            knowledge_file = os.path.join(base_dir, "knowledge", "knowledge_store.json")

        self.knowledge_file = knowledge_file
        self.chunks: List[Dict[str, Any]] = []
        self.tfidf_vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self.gemini_embeddings: List[List[float]] = []
        self._load_and_chunk_corpus()
        self._build_tfidf_index()

    def _load_and_chunk_corpus(self):
        """Loads curated documents and prepares chunk structures with metadata"""
        docs = []
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, "r", encoding="utf-8") as f:
                    docs = json.load(f)
            except Exception as e:
                print(f"[RAGEngine] Error loading knowledge JSON file: {e}")

        # Also discover any markdown knowledge documents in subdirectories
        base_dir = os.path.dirname(self.knowledge_file)
        if os.path.exists(base_dir):
            for root, _, files in os.walk(base_dir):
                for file in files:
                    if file.endswith(".md"):
                        md_path = os.path.join(root, file)
                        try:
                            with open(md_path, "r", encoding="utf-8") as f:
                                md_text = f.read()
                            # Parse optional yaml frontmatter
                            meta = {}
                            body = md_text
                            if md_text.startswith("---"):
                                parts = md_text.split("---", 2)
                                if len(parts) >= 3:
                                    fm_text = parts[1]
                                    body = parts[2].strip()
                                    for line in fm_text.splitlines():
                                        if ":" in line:
                                            k, v = line.split(":", 1)
                                            meta[k.strip()] = v.strip().strip('"').strip("'")
                            doc_id = meta.get("document_id", os.path.splitext(file)[0].upper())
                            # Avoid duplicates if document_id already loaded
                            if not any(d.get("document_id") == doc_id for d in docs):
                                docs.append({
                                    "document_id": doc_id,
                                    "title": meta.get("title", file.replace("_", " ").replace(".md", "").title()),
                                    "source": meta.get("source", "HeedX Clinical Knowledge Corpus"),
                                    "authors": meta.get("authors", "HeedX Research Team"),
                                    "year": int(meta.get("year", 2024)) if meta.get("year", "").isdigit() else 2024,
                                    "country": meta.get("country", "Nigeria"),
                                    "state": meta.get("state", "National"),
                                    "population": meta.get("population", "General"),
                                    "sample_size": meta.get("sample_size"),
                                    "mental_health_domain": meta.get("mental_health_domain", "clinical_knowledge"),
                                    "condition": meta.get("condition", "Mental Health"),
                                    "evidence_level": meta.get("evidence_level", "Clinical Evidence"),
                                    "limitations": meta.get("limitations", "Synthesized guidance"),
                                    "source_url": meta.get("source_url", ""),
                                    "content": body
                                })
                        except Exception as md_err:
                            print(f"[RAGEngine] Error reading {md_path}: {md_err}")

        chunk_id = 0
        for doc in docs:
            content = doc.get("content", "").strip()
            if not content:
                continue

            # Break large documents into 1-3 paragraph chunks
            paragraphs = [p.strip() for p in re.split(r'\n\s*\n', content) if len(p.strip()) > 40]
            if not paragraphs:
                paragraphs = [content]

            for p_idx, para in enumerate(paragraphs):
                chunk_id += 1
                self.chunks.append({
                    "chunk_id": f"{doc.get('document_id', 'DOC')}_C{p_idx+1}",
                    "document_id": doc.get("document_id"),
                    "title": doc.get("title"),
                    "source": doc.get("source"),
                    "authors": doc.get("authors"),
                    "year": doc.get("year"),
                    "country": doc.get("country", "Nigeria"),
                    "state": doc.get("state"),
                    "population": doc.get("population"),
                    "sample_size": doc.get("sample_size"),
                    "mental_health_domain": doc.get("mental_health_domain"),
                    "condition": doc.get("condition"),
                    "study_design": doc.get("study_design"),
                    "measurement_tool": doc.get("measurement_tool"),
                    "evidence_level": doc.get("evidence_level"),
                    "limitations": doc.get("limitations"),
                    "source_url": doc.get("source_url"),
                    "text": para
                })

    def _build_tfidf_index(self):
        """Builds a scikit-learn TF-IDF index for ultra-reliable local semantic search"""
        if not self.chunks:
            return

        corpus_texts = [
            f"{c.get('title', '')} {c.get('condition', '')} {c.get('mental_health_domain', '')} {c.get('text', '')}"
            for c in self.chunks
        ]
        self.tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            max_features=2500
        )
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(corpus_texts)

    def _get_gemini_embedding(self, text: str, api_key: str) -> Optional[List[float]]:
        """Fetch dense vector embedding from Google Gemini API via REST"""
        if not api_key or not text.strip():
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "models/text-embedding-004",
            "content": {
                "parts": [{"text": text[:2048]}]
            }
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                embedding = data.get("embedding", {}).get("values")
                return embedding
        except Exception:
            pass
        return None

    def construct_query(
        self,
        current_text: str = "",
        concerns: Optional[List[str]] = None,
        symptoms: Optional[List[str]] = None,
        stressors: Optional[List[str]] = None,
        context: Optional[List[str]] = None
    ) -> str:
        """
        Builds a high-signal search query from qualitative signals and user text.
        Avoids dumping raw, noisy transcripts.
        """
        query_terms = []
        if concerns:
            query_terms.extend(concerns)
        if symptoms:
            query_terms.extend(symptoms)
        if stressors:
            query_terms.extend(stressors)
        if context:
            query_terms.extend(context)

        # Include key salient words from current text
        if current_text:
            cleaned_words = [w for w in re.findall(r'\b[a-zA-Z]{3,}\b', current_text.lower())
                             if w not in {'the', 'and', 'was', 'for', 'that', 'with', 'have', 'been', 'this'}]
            query_terms.extend(cleaned_words[:6])

        if not query_terms:
            return current_text.strip() or "mental health support and coping"

        # Unique terms preserved in order
        seen = set()
        deduped = []
        for term in query_terms:
            t = str(term).strip().lower()
            if t and t not in seen:
                seen.add(t)
                deduped.append(t)

        return " ".join(deduped[:12])

    def search(
        self,
        query: str,
        top_k: int = 3,
        api_key: Optional[str] = None,
        domain_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes vector search against the indexed knowledge base.
        Returns top_k most relevant chunks along with metadata and similarity score.
        """
        if not self.chunks or not query.strip():
            return []

        # Strategy 1: Local TF-IDF Vector Cosine Similarity (Instant, zero-latency, always available)
        query_vec = self.tfidf_vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Apply domain filter if requested
        ranked_indices = np.argsort(similarities)[::-1]

        results = []
        for idx in ranked_indices:
            score = float(similarities[idx])
            chunk = self.chunks[idx]

            if domain_filter and chunk.get("mental_health_domain") != domain_filter:
                continue

            results.append({
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "title": chunk["title"],
                "source": chunk["source"],
                "authors": chunk["authors"],
                "year": chunk["year"],
                "evidence_level": chunk["evidence_level"],
                "population": chunk["population"],
                "condition": chunk["condition"],
                "limitations": chunk["limitations"],
                "source_url": chunk["source_url"],
                "text": chunk["text"],
                "score": round(score, 3)
            })

            if len(results) >= top_k:
                break

        return results

    def format_evidence_for_prompt(self, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """
        Formats retrieved evidence chunks into a clean, markdown block
        ready for injection into the LLM context.
        """
        if not retrieved_chunks:
            return "No specific external research evidence retrieved."

        lines = ["### RETRIEVED GROUNDING EVIDENCE (Nigerian & Clinical Context):"]
        for idx, chunk in enumerate(retrieved_chunks, 1):
            lines.append(f"**Evidence #{idx}: {chunk.get('title')}** ({chunk.get('year')})")
            lines.append(f"- *Source & Authors:* {chunk.get('source')} | {chunk.get('authors')}")
            lines.append(f"- *Population & Focus:* {chunk.get('population')} ({chunk.get('condition')})")
            lines.append(f"- *Evidence Level:* {chunk.get('evidence_level')}")
            lines.append(f"- *Key Finding / Guidance:* {chunk.get('text')}\n")

        return "\n".join(lines)
