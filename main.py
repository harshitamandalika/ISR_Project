from fetch_papers import fetch_recent_cv_papers
from user_profiles import create_user_profiles, load_user_profiles, save_user_profiles, update_user_feedback
from recommender import BM25_papers_rec, infer_disliked_papers
import pandas as pd

if __name__ == '__main__':
    keywords = ['computer', 'vision']
    max_result = 100
    
    #fetch_recent_cv_papers(keywords, max_result=max_result)
    #create_user_profiles() 

    profiles = load_user_profiles()
    papers_df = pd.read_csv('ISR_Project/data/papers.csv')
    user_id = 'user2'
    user = profiles[user_id]

    shown_df = BM25_papers_rec(user['research_focus'], papers_df, top_n=5)
    print("Initial Recommendations:\n")
    print(shown_df[['title', 'id']])
    shown_ids = shown_df['id'].tolist()

    # Testing if working
    liked_ids = shown_ids[:3]
    disliked_ids = infer_disliked_papers(shown_ids, liked_ids)

    print("Before updating ----- \n", profiles[user_id])
    update_user_feedback(user_id, {'liked': liked_ids, 'disliked': disliked_ids}, profiles)
    print("After updating : main\n", profiles[user_id])
    save_user_profiles(profiles)

    # profile and feedback from file
    profiles = load_user_profiles()
    user = profiles[user_id]
    liked_ids = user.get('liked_papers', [])
    disliked_ids = user.get('disliked_papers', [])

    # confirming if feedback loaded 
    print("liked_ids from profile:\n", liked_ids)
    print("disliked_ids from profile:\n", disliked_ids)

    # Recommendation with first feedback applied
    top5 = BM25_papers_rec(user['research_focus'], papers_df, liked_ids, disliked_ids)

    print("Recommendations after First Feedback:\n")
    print(top5[['title', 'id']])
    
    top5_ids = top5['id'].tolist()
    # Testing if working
    liked_ids = top5_ids[:3]
    disliked_ids = infer_disliked_papers(top5_ids, liked_ids)

    print("Before updating ----- \n", profiles[user_id])
    update_user_feedback(user_id, {'liked': liked_ids, 'disliked': disliked_ids}, profiles)
    print("After updating : main\n", profiles[user_id])
    save_user_profiles(profiles)

    # profile and feedback from file
    profiles = load_user_profiles()
    user = profiles[user_id]
    liked_ids = user.get('liked_papers', [])
    disliked_ids = user.get('disliked_papers', [])

    # confirming if feedback loaded 
    print("liked_ids from profile:\n", liked_ids)
    print("disliked_ids from profile:\n", disliked_ids)

    # Recommendation with  second feedback applied
    top5 = BM25_papers_rec(user['research_focus'], papers_df, liked_ids, disliked_ids)

    print("Recommendations after Second Feedback:\n")
    print(top5[['title', 'id']])