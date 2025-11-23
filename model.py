import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:
    def __init__(self, transaction_path, product_path):
        self.transaction_path = transaction_path
        self.product_path = product_path
        self.transactions_df = None
        self.products_df = None
        self.customer_item_matrix = None
        self.item_item_sim_matrix = None
        self.product_details = {}
        self.product_prices = {}
        self._train_model()

    def _train_model(self):
        print("Loading datasets...")
        self.transactions_df = pd.read_csv(self.transaction_path)
        self.products_df = pd.read_csv(self.product_path)
        
        # Create lookup dictionaries for quick access
        self.product_details = self.products_df.set_index('id').to_dict(orient='index')
        avg_prices = self.transactions_df.groupby('StockCode')['UnitPrice'].mean()
        self.product_prices = avg_prices.to_dict()

        print("Building Matrices...")
        # 1. Create Customer-Item Matrix (Who bought what)
        self.customer_item_matrix = self.transactions_df.pivot_table(
            index='CustomerID',
            columns='StockCode',
            values='Quantity',
            aggfunc='sum'
        ).fillna(0).map(lambda x: 1 if x > 0 else 0)

        # 2. Create Item-Item Similarity Matrix (Transpose the matrix)
        # This calculates which items are often bought together
        self.item_item_sim_matrix = pd.DataFrame(
            cosine_similarity(self.customer_item_matrix.T),
            index=self.customer_item_matrix.columns,
            columns=self.customer_item_matrix.columns
        )
        print("Model training complete.")

    def get_product_info(self, product_id):
        """Get details for a single product"""
        details = self.product_details.get(product_id)
        if details:
            # Append ID and Price to the details dictionary
            details['id'] = product_id
            details['price'] = round(self.product_prices.get(product_id, 25.00), 2)
            return details
        return None

    def get_item_recommendations(self, product_id, top_n=4):
        """
        Recommend products similar to the one provided.
        Used for the 'Added to Cart' popup.
        """
        if product_id not in self.item_item_sim_matrix.index:
            return []

        # Get similarity scores for this item, sort descending
        similar_items = self.item_item_sim_matrix[product_id].sort_values(ascending=False)
        
        # Exclude the item itself (index 0) and take top N
        similar_items_ids = similar_items.index[1:top_n+1]
        
        recommendations = []
        for item_id in similar_items_ids:
            details = self.product_details.get(item_id)
            score = similar_items[item_id] # Get the cosine similarity score
            
            if details:
                recommendations.append({
                    'id': item_id,
                    'name': details['name'],
                    'category': details['category'],
                    'image': details['image'],
                    'price': round(self.product_prices.get(item_id, 25.00), 2),
                    'score': round(score * 100, 1) # Convert to percentage for display
                })
        return recommendations

    def get_similarity_explanation(self, product_id, top_n=10):
        """
        Returns detailed scoring data for the explanation page.
        Shows exactly why items are recommended (their similarity score).
        """
        if product_id not in self.item_item_sim_matrix.index:
            return []

        # Get all similarities, sort desc
        similar_items = self.item_item_sim_matrix[product_id].sort_values(ascending=False)
        
        explanation_data = []
        # Skip index 0 (itself)
        for item_id in similar_items.index[1:top_n+1]:
            details = self.product_details.get(item_id)
            score = similar_items[item_id]
            
            if details:
                explanation_data.append({
                    'name': details['name'],
                    'image': details['image'],
                    'score': round(score * 100, 2), # Precise score
                    'bar_width': int(score * 100)   # Integer for CSS width
                })
        return explanation_data