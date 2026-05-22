from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def fit_transform(resumes, job_description):
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    resume_embeddings = model.encode(resumes, convert_to_tensor=True)
    return job_embedding, resume_embeddings

def get_scores(job_embedding, resume_embeddings):
    scores = util.cos_sim(job_embedding, resume_embeddings)[0]
    return scores.cpu().tolist()

def rank(scores, filenames):
    results = [{"filename": fn, "score": float(sc)} for fn, sc in zip(filenames, scores)]
    return sorted(results, key=lambda r: r["score"], reverse=True)


