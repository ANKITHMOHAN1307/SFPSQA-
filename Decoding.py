import os
import requests
import json
from Evaluation import nutrient_profiling, ingredient_profiling

def get_console_width():
    """Get the console width, or a default value if not available."""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80  # Default width if no terminal

# Initialize console width
console_width = get_console_width()

def decode_from_upload(barcode_data):
    """Decodes uploaded barcode and prints evaluation."""
    print(f"\n[Upload] Decoded Data: {barcode_data}")
    # Access `console_width` from here or pass it as an argument if needed

def decode_from_scan(barcode_data):
    """Decodes scanned barcode and prints evaluation."""
    print(f"\n[Scanner] Decoded Data: {barcode_data}")
    # Access `console_width` from here or pass it as an argument if needed
# Decoding.py

import requests
from Evaluation import nutrient_profiling, ingredient_profiling

def get_product_details(barcode):
    """Fetch product details using Open Food Facts API."""
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return {"Error": f"API request failed: {e}"}

    if 'product' not in data:
        return {"Error": "No product found for this barcode."}

    product = data['product']
    nutriments = product.get("nutriments", {})

    product_info = {
        "Title": product.get("product_name", "Unknown"),
        "Brand": product.get("brands", "Unknown"),
        "Category": product.get("categories", "Unknown"),
        "Image": product.get("image_url", "No image available"),
        "Serving Size": product.get("serving_size", "Unknown"),
        "product": product,  # full product data for reference
        "nutriments": nutriments,
        "ingredients_text": product.get("ingredients_text", "")
    }

    # Add profiling results
    product_info["Nutrient Profiling"] = nutrient_profiling(nutriments)
    product_info["Ingredient Profiling"] = ingredient_profiling(product_info["ingredients_text"])

    return product_info

def decode_from_scan(barcode_data):
    """Decodes scanned barcode and prints evaluation."""
    print(f"\n[Scanner] Decoded Data: {barcode_data}")
    product_info = get_product_details(barcode_data)

    if "Error" in product_info:
        print("\n", product_info["Error"])
    else:
        print("\n**Product Information:**")
        for key, value in product_info.items():
            if key not in ["Nutrient Profiling", "Ingredient Profiling"]:
                print(f"  - {key}: {value}")

        print("\n**Nutrient Profiling:**")
        for key, value in product_info["Nutrient Profiling"].items():
            print(f"  - {key}: {value}")

        print("\n**Ingredient Profiling:**")
        for category, items in product_info["Ingredient Profiling"].items():
            print(f"  - {category}: {', '.join(items) if items else 'None'}")
    return product_info

def decode_from_upload(barcode_data):
    """Decodes uploaded barcode and prints evaluation."""
    print(f"\n[Upload] Decoded Data: {barcode_data}")
    product_info = get_product_details(barcode_data)

    if "Error" in product_info:
        print("\n", product_info["Error"])
    else:
        print("\n**Product Information:**")
        for key, value in product_info.items():
            if key not in ["Nutrient Profiling", "Ingredient Profiling"]:
                print(f"  - {key}: {value}")

        print("\n**Nutrient Profiling:**")
        for key, value in product_info["Nutrient Profiling"].items():
            print(f"  - {key}: {value}")

        print("\n**Ingredient Profiling:**")
        for category, items in product_info["Ingredient Profiling"].items():
            print(f"  - {category}: {', '.join(items) if items else 'None'}")
    return product_info

if __name__ == '__main__':
    # Test with a known barcode
    barcode = '8901648002444'
    product_details = get_product_details(barcode)
    if "Error" in product_details:
        print(product_details["Error"])
    else:
        print(json.dumps(product_details, indent=4, ensure_ascii=False))
