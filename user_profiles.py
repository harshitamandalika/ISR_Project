import json
import os

path = 'data/user_profiles.json'

def create_user_profiles():
    profiles = {
        "uday": {'name': 'Uday Vysyaraju', 'email': 'udaysanthoshkgp@gmail.com',"research_focus": "image classification deep learning neural networks", "liked_papers": [], "disliked_papers": []},
        "sejeong": {'name': 'Sejeong Moon', 'email': 'smoon23@tamu.edu', "research_focus": "transformers visual attention representation learning images", "liked_papers": [], "disliked_papers": []},
        "harshita": {'name': 'Harshita Mandalika', 'email': 'harshita.mandalika@tamu.edu', "research_focus": "face analysis face recognition biometric vision human identity", "liked_papers": [], "disliked_papers": []},
    }

    os.makedirs('data', exist_ok=True)
    with open(path, 'w') as f:
        json.dump(profiles, f, indent=4)
    #print(f"User profiles saved to {path}")

def load_user_profiles(filepath=path):
    with open(filepath, 'r') as f:
        return json.load(f)
