from sklearn.metrics.pairwise import cosine_similarity

from app.models.model import model
from app.services.llm import ask_llm

def semantic_similarity(emb1, reference):
    emb2 = model.encode([reference], normalize_embeddings=True)

    sim = cosine_similarity(emb1, emb2)[0][0]
    return float(sim)

def length_score(answer, reference):
    len_ratio = len(answer.split()) / len(reference.split())
    return min(len_ratio, 1.0)

def keyword_score_semantic(answer_emb, keywords):
    kw_emb = model.encode(keywords, normalize_embeddings=True)

    sims = cosine_similarity(answer_emb, kw_emb)[0]

    good = sum(sim > 0.6 for sim in sims)
    return good / len(keywords)

def extract_keywords(reference_text: str) -> list[str]:
    prompt = f"""
    Выдели ключевые понятия из ответа.

    Ответ:
    {reference_text}

    Верни только список ключевых слов через запятую.
    Пример:
    инкапсуляция, наследование, полиморфизм
    """

    response = ask_llm(prompt)

    keywords = [k.strip() for k in response.split(",") if k.strip()]

    return keywords

def final_score(answer, reference, keywords):
    answer_emb = model.encode([answer], normalize_embeddings=True)
    sem = semantic_similarity(answer_emb, reference)
    if not keywords:
        keywords = extract_keywords(reference)
    key = keyword_score_semantic(answer_emb, keywords)
    length = length_score(answer, reference) 

    final = (
        0.6 * sem +
        0.3 * key +
        0.1 * length
    )

    percent = round(final * 100)

    return percent


