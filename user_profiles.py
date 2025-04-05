import json
import os

path = 'data/user_profiles.json'

def create_user_profiles():
    profiles = {
        "user1": {"research_focus": "image classification deep learning neural networks", "liked_papers": [], "disliked_papers": []},
        "user2": {"research_focus": "object detection real time images bounding boxes detection performance", "liked_papers": [], "disliked_papers": []},
        "user3": {"research_focus": "segmentation medical images pixel labeling annotation", "liked_papers": [], "disliked_papers": []},
        "user4": {"research_focus": "3D vision reconstruction depth sensors spatial analysis geometry", "liked_papers": [], "disliked_papers": []},
        "user5": {"research_focus": "transformers visual attention representation learning images", "liked_papers": [], "disliked_papers": []},
        "user6": {"research_focus": "healthcare imaging diagnostic tools brain scan chest x-ray mri", "liked_papers": [], "disliked_papers": []},
        "user7": {"research_focus": "video processing action detection video classification motion tracking", "liked_papers": [], "disliked_papers": []},
        "user8": {"research_focus": "face analysis face recognition biometric vision human identity", "liked_papers": [], "disliked_papers": []},
        "user9": {"research_focus": "domain shift visual generalization dataset adaptation few-shot learning", "liked_papers": [], "disliked_papers": []},
        "user10": {"research_focus": "image generation generative models artistic synthesis visual creativity", "liked_papers": [], "disliked_papers": []}
    }

    os.makedirs('data', exist_ok=True)
    with open(path, 'w') as f:
        json.dump(profiles, f, indent=4)
    #print(f"User profiles saved to {path}")

def load_user_profiles(filepath=path):
    with open(filepath, 'r') as f:
        return json.load(f)
