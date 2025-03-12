import pandas as pd
import json
from datetime import datetime
import sys
import os

# Ensure the project's root directory is in sys.path for proper module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#   Import required modules
from config.settings import RAW_DATA_FILE, TRANSFORMED_DATA_FILE

def transform_data():
    """
    Processes the extracted data to generate sales metrics.

    Returns:
        str: The file path of the transformed data.

    Raises:
        Exception: If there is an error during data transformation.
    """
    try:
        print(f"Reading data from {RAW_DATA_FILE}")
        data = pd.read_json(RAW_DATA_FILE)
        
        required_columns = ['id', 'title', 'price', 'category']
        for col in required_columns:
            if col not in data.columns:
                raise ValueError(f"Required column '{col}' not found in the dataset")
        
        # Check for missing values in critical columns
        if data[required_columns].isnull().any().any():
            print("Warning: Null values detected in critical columns")
        
        # Apply a sales factor to each category
        category_factors = {
            'electronics': 15,
            'jewelery': 8,
            "men's clothing": 12,
            "women's clothing": 20
        }
        
        # Calculate total sales, average price, and product count by category
        data['sales_factor'] = data['category'].map(lambda cat: category_factors.get(cat, 10))
        data['sales'] = data['price'] * data['sales_factor']
        
        # Generate metrics by category
        total_sales_by_category = data.groupby('category')['sales'].sum().reset_index()
        total_sales_by_category.rename(columns={'sales': 'total_sales'}, inplace=True)
        
        # Calculate average price by category
        avg_price_by_category = data.groupby('category')['price'].mean().reset_index()
        avg_price_by_category.rename(columns={'price': 'avg_price'}, inplace=True)
        
        # Count the number of products in each category
        product_count_by_category = data.groupby('category').size().reset_index()
        product_count_by_category.rename(columns={0: 'product_count'}, inplace=True)
        
        # Merge all metrics into a single DataFrame
        metrics = pd.merge(total_sales_by_category, avg_price_by_category, on='category')
        metrics = pd.merge(metrics, product_count_by_category, on='category')
        metrics['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save transformed data to CSV
        print(f"Saving metrics to {TRANSFORMED_DATA_FILE}")
        metrics.to_csv(TRANSFORMED_DATA_FILE, index=False)
        
        return TRANSFORMED_DATA_FILE
    
    except Exception as e:
        print(f"Error during data transformation: {str(e)}")
        raise

# Entry point for the script
if __name__ == "__main__":
    file_path = transform_data()
    print(f"File successfully generated: {file_path}")

