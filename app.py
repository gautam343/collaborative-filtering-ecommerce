from flask import Flask, render_template, request, jsonify
from model import Recommender
import os

app = Flask(__name__)

TRANSACTIONS_PATH = os.path.join('dataset', 'transactions.csv')
PRODUCTS_PATH = os.path.join('dataset', 'products.csv')

if os.path.exists(TRANSACTIONS_PATH) and os.path.exists(PRODUCTS_PATH):
    recommender = Recommender(TRANSACTIONS_PATH, PRODUCTS_PATH)
else:
    recommender = None
    print("WARNING: Datasets not found. Run generate_dataset.py first.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    if not recommender:
        return jsonify({'error': 'Model not ready'}), 500

    data = request.json
    product_id = data.get('product_id')
    recommendations = recommender.get_item_recommendations(product_id)
    return jsonify(recommendations)

# --- NEW ROUTE: Explanation Portal ---
@app.route('/explain')
def explain():
    product_id = request.args.get('id')
    if not recommender or not product_id:
        return "Product not found", 404
    
    product_info = recommender.get_product_info(product_id)
    explanation_data = recommender.get_similarity_explanation(product_id)
    
    return render_template('explain.html', product=product_info, data=explanation_data)

if __name__ == '__main__':
    app.run(debug=True)