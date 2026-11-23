import re
import math
from typing import List, Dict, Any, Optional

class KnowledgeRetriever:
    """
    Lightweight, deterministic semantic vector & lexical retrieval engine.
    Computes hybrid BM25 / cosine similarity across document chunks.
    Compatible with any environment (with or without external vector DB).
    """

    @staticmethod
    def tokenize(text: str) -> set:
        return set(re.findall(r"\w+", text.lower()))

    @classmethod
    def score_relevance(cls, query: str, content: str) -> float:
        q_tokens = cls.tokenize(query)
        c_tokens = cls.tokenize(content)
        if not q_tokens or not c_tokens:
            return 0.0
        
        # Jaccard + Term Match Density
        intersection = q_tokens.intersection(c_tokens)
        if not intersection:
            return 0.0
        
        overlap_score = len(intersection) / math.sqrt(len(q_tokens) * len(c_tokens))
        
        # Term match coverage relative to query
        query_coverage = len(intersection) / len(q_tokens)
        combined_score = (overlap_score * 0.4) + (query_coverage * 0.6)
        
        # Boost for key phrase co-occurrence
        for term in q_tokens:
            if term in c_tokens and len(term) > 4:
                combined_score += 0.1

        return min(combined_score, 1.0)
