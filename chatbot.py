import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

class ShopBot:
    def __init__(self, product_path):
        self.product_path = product_path
        self.df = pd.read_csv(self.product_path)
        
        # Pre-process data for NLP
        # We combine name and category to create a "searchable" text field
        self.df['search_text'] = (self.df['name'] + " " + self.df['category']).fillna('').str.lower()
        
        # Initialize TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['search_text'])

    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        
        # 1. Handle Greetings
        greetings = ['hi', 'hello', 'hey', 'good morning', 'greetings']
        if user_input in greetings:
            return {
                "text": "Hello! 👋 I'm your Anon shopping assistant. Ask me about products like 'formal shoes', 'watches', or 'winter jackets'!",
                "products": []
            }

        # 2. Handle "Help" or "Menu"
        if 'help' in user_input or 'menu' in user_input:
            return {
                "text": "I can help you find products. Try typing:\n- 'Show me menswear'\n- 'I need a red shirt'\n- 'Best watches'",
                "products": []
            }

        # 3. Product Search (Content-Based Filtering)
        # Transform user query into the same vector space as our products
        user_vec = self.vectorizer.transform([user_input])
        
        # Calculate similarity
        cosine_sim = cosine_similarity(user_vec, self.tfidf_matrix).flatten()
        
        # Get top 3 matches
        # We only keep matches with a score > 0.1 (to avoid random noise)
        related_indices = cosine_sim.argsort()[:-4:-1]
        top_matches = []
        
        for idx in related_indices:
            if cosine_sim[idx] > 0.1: 
                product = self.df.iloc[idx]
                top_matches.append({
                    'id': product['id'],
                    'name': product['name'],
                    'image': product['image'],
                    # We might not have price in products.csv depending on generate_dataset.py
                    # If missing, default to a range or look it up if you merged data differently
                    'price': "Check Details", 
                    'category': product['category']
                })

        if top_matches:
            return {
                "text": f"I found {len(top_matches)} items that match '{user_input}':",
                "products": top_matches
            }
        else:
            return {
                "text": "I couldn't find anything matching that description. 😕 Try searching for 'shoes', 'bag', or 'jacket'.",
                "products": []
            }