from sklearn.metrics.pairwise import cosine_similarity

from app.models import model

def semantic_similarity(answer, reference):
    emb1 = model.encode([answer], normalize_embeddings=True)
    emb2 = model.encode([reference], normalize_embeddings=True)

    sim = cosine_similarity(emb1, emb2)[0][0]
    return float(sim)

def length_score(answer, reference):
    len_ratio = len(answer.split()) / len(reference.split())
    return min(len_ratio, 1.0)

def keyword_score_semantic(answer, keywords):
    answer_emb = model.encode([answer], normalize_embeddings=True)
    kw_emb = model.encode(keywords, normalize_embeddings=True)

    sims = cosine_similarity(answer_emb, kw_emb)[0]

    good = sum(sim > 0.6 for sim in sims)
    return good / len(keywords)

def final_score(answer, reference, keywords):
    sem = semantic_similarity(answer, reference)
    key = keyword_score_semantic(answer, keywords) 
    length = length_score(answer, reference) 

    final = (
        0.6 * sem +
        0.3 * key +
        0.1 * length
    )

    percent = round(final * 100, 2)

    return percent


