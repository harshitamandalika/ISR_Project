import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_papers_tfidf(research_focus, papers_df, disliked_ids=None, top_n=5):
    corpus = [research_focus] + papers_df['abstract'].tolist()
    tfidf = TfidfVectorizer(stop_words='english').fit_transform(corpus)
    sim_scores = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

    # Penalize disliked papers(to ensure that the papers disliked by the user are not likely to be recommended again)
    if disliked_ids:
        for i, paper_id in enumerate(papers_df['id']):
            if paper_id in disliked_ids:
                sim_scores[i] = -1.0

    # Return top 5 papers ranked by similarity
    top_matches = sim_scores.argsort()[-top_n:][::-1]
    print(sorted(sim_scores)[-top_n:][::-1])
    return papers_df.iloc[top_matches]