import pandas as pd
import json
import google.generativeai as genai
import os
import re

class ShopBot:
    def __init__(self, product_path):
        # Load product data
        self.df = pd.read_csv(product_path)
        
        # Convert dataframe to a simplified JSON string
        self.products_json = self.df[['id', 'name', 'category', 'price']].to_json(orient='records')
        
        # Configure API Key
        # IMPORTANT: Replace with your actual key
        genai.configure(api_key="")

        # Define the System Prompt
        self.system_prompt = f"""
        You are the intelligent shopping assistant for Anon eCommerce.
        
        Here is our complete product catalog in JSON format:
        {self.products_json}
        
        YOUR INSTRUCTIONS:
        1. Answer user queries enthusiastically.
        2. If the user asks for a product recommendation, pick the best matching items from the catalog above.
        3. You MUST return your response in valid JSON format with exactly two keys:
           - "text": A natural language response to the user (string).
           - "product_ids": A list of the 'id' strings of the products you recommend (e.g. ["jacket-1", "watch-2"]).
        4. If no products match, return an empty list for "product_ids".
        5. Do not make up products. Only use the ones in the catalog.
        """
        
        # Try initializing the newer model available in your list
        try:
            # We use 'gemini-2.5-flash' since your list confirmed you have it
            self.model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=self.system_prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            self.use_fallback = False
            print("✅ Connected to Gemini 2.5 Flash")
        except Exception as e:
            print(f"⚠️ Standard connection failed ({e}). Switching to basic text mode...")
            # Fallback: Use the same model but without forcing JSON mode (sometimes fixes API quirks)
            self.model = genai.GenerativeModel("gemini-2.5-flash")
            self.use_fallback = True

    def get_response(self, user_input):
        try:
            if self.use_fallback:
                # Manual prompt engineering for fallback mode
                full_prompt = f"{self.system_prompt}\n\nUSER QUERY: {user_input}\n\nREMEMBER: Return ONLY valid JSON."
                response = self.model.generate_content(full_prompt)
            else:
                # Standard chat mode
                response = self.model.generate_content(user_input)

            response_text = response.text
            
            # Clean up potential Markdown formatting (e.g. ```json ... ```)
            response_text = re.sub(r"```json|```", "", response_text).strip()

            # Parse JSON
            ai_content = json.loads(response_text)
            
            reply_text = ai_content.get('text', "I found some items for you.")
            recommended_ids = ai_content.get('product_ids', [])

            # Fetch product details (Images, Price) for the UI
            matched_products = []
            for pid in recommended_ids:
                product_row = self.df[self.df['id'] == pid]
                if not product_row.empty:
                    product = product_row.iloc[0]
                    matched_products.append({
                        'id': product['id'],
                        'name': product['name'],
                        'image': product['image'],
                        'price': product['price'],
                        'category': product['category']
                    })

            return {
                "text": reply_text,
                "products": matched_products
            }

        except Exception as e:
            print(f"Chatbot Error: {e}")
            # Print the raw text to help debug if it fails again
            return {
                "text": "I'm having a bit of trouble connecting to my brain right now. 🧠 Please try again!",
                "products": []
            }