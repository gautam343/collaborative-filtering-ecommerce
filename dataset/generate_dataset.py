import pandas as pd
import random
import os

def generate_datasets():
    # 1. Define products based on your repository's images
    products = [
        {'id': '1', 'image': '1.jpg', 'name': 'Baby Fabric Shoes', 'category': 'Baby'},
        {'id': '2', 'image': '2.jpg', 'name': 'Mens Hoodies T-Shirt', 'category': 'Men'},
        {'id': '3', 'image': '3.jpg', 'name': 'Girls T-Shirt', 'category': 'Kids'},
        {'id': '4', 'image': '4.jpg', 'name': 'Woolen Hat For Men', 'category': 'Men'},
        {'id': 'belt', 'image': 'belt.jpg', 'name': 'Mens Leather Belt', 'category': 'Accessories'},
        {'id': 'clothes-1', 'image': 'clothes-1.jpg', 'name': 'Relaxed Short Sleeve T-Shirt', 'category': 'Women'},
        {'id': 'clothes-2', 'image': 'clothes-2.jpg', 'name': 'Girls Pink Embro Design Top', 'category': 'Women'},
        {'id': 'clothes-3', 'image': 'clothes-3.jpg', 'name': 'Black Floral Wrap Midi Skirt', 'category': 'Women'},
        {'id': 'clothes-4', 'image': 'clothes-4.jpg', 'name': 'Pure Garment Dyed Cotton Shirt', 'category': 'Women'},
        {'id': 'jacket-1', 'image': 'jacket-1.jpg', 'name': 'Mens Winter Leathers Jacket', 'category': 'Men'},
        {'id': 'jacket-2', 'image': 'jacket-2.jpg', 'name': 'Mens Winter Leathers Jacket', 'category': 'Men'},
        {'id': 'jacket-3', 'image': 'jacket-3.jpg', 'name': 'Mens Winter Leathers Jacket', 'category': 'Men'},
        {'id': 'jacket-4', 'image': 'jacket-4.jpg', 'name': 'Mens Winter Leathers Jacket', 'category': 'Men'},
        {'id': 'jacket-5', 'image': 'jacket-5.jpg', 'name': 'MEN Yarn Fleece Full-Zip Jacket', 'category': 'Men'},
        {'id': 'jacket-6', 'image': 'jacket-6.jpg', 'name': 'MEN Yarn Fleece Full-Zip Jacket', 'category': 'Men'},
        {'id': 'jewellery-1', 'image': 'jewellery-1.jpg', 'name': 'Rose Gold Peacock Earrings', 'category': 'Jewelry'},
        {'id': 'jewellery-2', 'image': 'jewellery-2.jpg', 'name': 'Platinum Zircon Classic Ring', 'category': 'Jewelry'},
        {'id': 'jewellery-3', 'image': 'jewellery-3.jpg', 'name': 'Silver Deer Heart Necklace', 'category': 'Jewelry'},
        {'id': 'party-wear-1', 'image': 'party-wear-1.jpg', 'name': 'Womens Party Wear Shoes', 'category': 'Women'},
        {'id': 'party-wear-2', 'image': 'party-wear-2.jpg', 'name': 'Womens Party Wear Shoes', 'category': 'Women'},
        {'id': 'perfume', 'image': 'perfume.jpg', 'name': 'Titan 100 Ml Womens Perfume', 'category': 'Perfume'},
        {'id': 'shampoo', 'image': 'shampoo.jpg', 'name': 'Shampoo Conditioner Packs', 'category': 'Cosmetics'},
        {'id': 'shirt-1', 'image': 'shirt-1.jpg', 'name': 'Pure Garment Dyed Cotton Shirt', 'category': 'Men'},
        {'id': 'shirt-2', 'image': 'shirt-2.jpg', 'name': 'Pure Garment Dyed Cotton Shirt', 'category': 'Men'},
        {'id': 'shoe-1', 'image': 'shoe-1.jpg', 'name': 'Mens Leather Formal Wear Shoes', 'category': 'Men'},
        {'id': 'shoe-1_1', 'image': 'shoe-1_1.jpg', 'name': 'Mens Leather Formal Wear Shoes', 'category': 'Men'},
        {'id': 'shoe-2', 'image': 'shoe-2.jpg', 'name': 'Casual Mens Brown Shoes', 'category': 'Men'},
        {'id': 'shoe-2_1', 'image': 'shoe-2_1.jpg', 'name': 'Casual Mens Brown Shoes', 'category': 'Men'},
        {'id': 'shoe-3', 'image': 'shoe-3.jpg', 'name': 'Boot With Suede Detail', 'category': 'Men'},
        {'id': 'shoe-4', 'image': 'shoe-4.jpg', 'name': 'Boot With Suede Detail', 'category': 'Men'},
        {'id': 'shoe-5', 'image': 'shoe-5.jpg', 'name': 'Boot With Suede Detail', 'category': 'Men'},
        {'id': 'shorts-1', 'image': 'shorts-1.jpg', 'name': 'Better Basics French Terry Sweatshorts', 'category': 'Men'},
        {'id': 'shorts-2', 'image': 'shorts-2.jpg', 'name': 'Better Basics French Terry Sweatshorts', 'category': 'Men'},
        {'id': 'sports-1', 'image': 'sports-1.jpg', 'name': 'Trekking & Running Shoes - Black', 'category': 'Sports'},
        {'id': 'sports-2', 'image': 'sports-2.jpg', 'name': 'Trekking & Running Shoes - Black', 'category': 'Sports'},
        {'id': 'sports-3', 'image': 'sports-3.jpg', 'name': 'Sports Claw Womens Shoes', 'category': 'Sports'},
        {'id': 'sports-4', 'image': 'sports-4.jpg', 'name': 'Sports Claw Womens Shoes', 'category': 'Sports'},
        {'id': 'sports-5', 'image': 'sports-5.jpg', 'name': 'Air Trekking Shoes - White', 'category': 'Sports'},
        {'id': 'sports-6', 'image': 'sports-6.jpg', 'name': 'Air Trekking Shoes - White', 'category': 'Sports'},
        {'id': 'watch-1', 'image': 'watch-1.jpg', 'name': 'Smart Watch Vital Plus', 'category': 'Watches'},
        {'id': 'watch-2', 'image': 'watch-2.jpg', 'name': 'Smart Watch Vital Plus', 'category': 'Watches'},
        {'id': 'watch-3', 'image': 'watch-3.jpg', 'name': 'Pocket Watch Leather Pouch', 'category': 'Watches'},
        {'id': 'watch-4', 'image': 'watch-4.jpg', 'name': 'Pocket Watch Leather Pouch', 'category': 'Watches'},
    ]

    # --- NEW STEP: Add Prices to Products ---
    for p in products:
        # Assign a random price between $15 and $150
        p['price'] = round(random.uniform(15.00, 150.00), 2)

    # 2. Save Product Catalog (Now includes 'price' column)
    catalog_df = pd.DataFrame(products)
    if not os.path.exists('dataset'):
        os.makedirs('dataset')
    catalog_df.to_csv('dataset/products.csv', index=False)
    print(f"✅ dataset/products.csv created with prices.")

    # 3. Generate Synthetic Transactions
    # We simulate 50 users (ID 1000-1050) making 500 total purchases
    transactions = []
    user_ids = range(1000, 1050)

    for _ in range(500): 
        user_id = random.choice(user_ids)
        product = random.choice(products)
        quantity = random.randint(1, 5)
        
        transactions.append({
            'CustomerID': user_id,
            'StockCode': product['id'],
            'Description': product['name'],
            'Quantity': quantity,
            # Use the specific price we assigned to the product above
            'UnitPrice': product['price'],
            'Country': 'United Kingdom'
        })

    transactions_df = pd.DataFrame(transactions)
    transactions_df.to_csv('dataset/transactions.csv', index=False)
    print(f"✅ dataset/transactions.csv created.")

if __name__ == "__main__":
    generate_datasets()