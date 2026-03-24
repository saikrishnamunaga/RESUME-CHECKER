from sentence_transformers import SentenceTransformer, util
import spacy
import re
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class NLPEngine:
    def __init__(self):
        self.model = None
        self.nlp = None
        self.domain_keywords = {
            'IT': ['python', 'java', 'javascript', 'developer', 'engineer', 'sql', 'docker', 'aws'],
            'Sales': ['sales', 'marketing', 'account', 'client', 'revenue', 'lead'],
            'Healthcare': ['nurse', 'doctor', 'patient', 'medical', 'healthcare', 'hospital'],
            'Management': ['manager', 'director', 'leadership', 'team', 'project', 'strategy'],
            'Mechanical': ['engineer', 'mechanical', 'cad', 'solidworks', 'manufacturing']
        }
        self.vectorizer = TfidfVectorizer(max_features=100)

    def _lazy_load(self):
        if self.model is None:
            try:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
            except:
                self.model = None
        if self.nlp is None:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except:
                self.nlp = None

    def detect_domain(self, job_desc: str) -> str:
        scores = {}
        for domain, keywords in self.domain_keywords.items():
            score = sum(1 for kw in keywords if kw in job_desc.lower())
            scores[domain] = score
        return max(scores, key=scores.get)

    def extract_entities(self, text: str) -> List[str]:
        self._lazy_load()
        skills = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)?\b', text)
        return list(set(skills))[:10]

    def compute_match_score(self, resume_text: str, job_desc: str) -> Dict:
        self._lazy_load()
        similarity = 50.0
        if self.model is not None:
            emb_resume = self.model.encode(resume_text)
            emb_job = self.model.encode(job_desc)
            similarity = util.cos_sim(emb_resume, emb_job)[0][0].item() * 100

        # Keyword match with TF-IDF
        tfidf_sim = 0
        if resume_text.strip():
            tfidf_matrix = self.vectorizer.fit_transform([resume_text, job_desc])
            tfidf_sim = 100 * tfidf_matrix[0].dot(tfidf_matrix[1].T).toarray()[0][0]

        # Weighted score
        score = 0.7 * similarity + 0.3 * tfidf_sim

        # Extract
        resume_skills = self.extract_entities(resume_text)
        job_skills = self.extract_entities(job_desc)

        strengths = [s for s in resume_skills if s.lower() in job_desc.lower()]
        missing = [s for s in job_skills if s.lower() not in resume_text.lower()]

        domain = self.detect_domain(job_desc)

        return {
            "domain": domain,
            "score": round(score, 2),
            "strengths": strengths[:5],
            "missing": missing[:5],
            "suggestions": ["Add more specific projects"] if score < 70 else []
        }

nlp_engine = NLPEngine()

