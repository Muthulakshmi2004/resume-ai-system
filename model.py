from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def fit_transform(job_description, resumes):
    corpus = [job_description] + resumes
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(corpus)
    return matrix

def get_scores(matrix):
    job_vec = matrix[0]
    resume_vecs = matrix[1:]
    similarities = cosine_similarity(job_vec, resume_vecs)
    return similarities.flatten()

def rank(resumes, scores):
    return sorted(zip(resumes, scores), key=lambda x: x[1], reverse=True)
