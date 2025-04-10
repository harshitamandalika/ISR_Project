from fetch_papers import fetch_recent_cv_papers
from user_profiles import create_user_profiles, load_user_profiles
from recommender import recommend_papers_tfidf
import pandas as pd

# checking for a single user
def recommend_for_user(user_id):
    profiles = load_user_profiles()
    papers_df = pd.read_csv('data/papers.csv')
    user = profiles[user_id]
    return recommend_papers_tfidf(user['research_focus'], papers_df, user.get('disliked_papers', []), top_n=5)

if __name__ == '__main__':
    keywords = ['computer', 'vision']
    max_result = 100
    
    fetch_recent_cv_papers(keywords, max_result=max_result)
    create_user_profiles()  
    top5 = recommend_for_user('user6')
    print(top5[['title', 'id']])
