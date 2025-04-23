import pandas as pd
from rank_bm25 import BM25Okapi

def BM25_papers_rec(user_profile, papers_df, liked_ids=None, disliked_ids=None, top_n=5):
    liked_ids = liked_ids or []
    disliked_ids = disliked_ids or []

    # Normalizing paper_IDs and excluding previously seen papers
    excluded_ids = set(pid.strip().lower().rsplit('v', 1)[0] for pid in liked_ids + disliked_ids)
    print("Excluded papers")
    print(excluded_ids)
    papers_df['norm_id'] = papers_df['id'].str.strip().str.lower().str.rsplit('v', n=1).str[0]
    unseen_papers_df = papers_df[~papers_df['norm_id'].isin(excluded_ids)].copy()
    print("Unseen papers")
    print(unseen_papers_df)

    if unseen_papers_df.empty:
        print("No unseen papers left.")
        return unseen_papers_df.iloc[[]]  

    # Tokenizing corpus and query
    tokenized_corpus = [abstract.lower().split() for abstract in unseen_papers_df['abstract']]
    tokenized_query = user_profile.lower().split()

    # BM25 scoring
    bm25 = BM25Okapi(tokenized_corpus)
    sim_scores = bm25.get_scores(tokenized_query)

    # Returning indices of top scores
    top_matches = sorted(range(len(sim_scores)), key=lambda i: sim_scores[i], reverse=True)[:top_n]
    return unseen_papers_df.iloc[top_matches]

def build_updated_query(user_profile, liked_ids, papers_df):
    # Normalizing both sides to match properly
    normalized_ids = [pid.strip().lower() for pid in liked_ids]
    papers_df['normalized_id'] = papers_df['id'].str.strip().str.lower()
    liked_abstracts = papers_df[papers_df['normalized_id'].isin(normalized_ids)]['abstract'].tolist()

    latest_liked = ' '.join(liked_abstracts)
    updated_query = user_profile + ' ' + latest_liked

    print("Updated query (start):", updated_query[:300], "...")
    return updated_query

def infer_disliked_papers(shown_ids, liked_ids):
    return [pid for pid in shown_ids if pid not in liked_ids]