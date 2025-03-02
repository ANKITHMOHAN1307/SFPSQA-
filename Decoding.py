import requests
from Evaluation import nutrient_profiling, ingredient_profiling
import json
import os
def get_product_details(barcode):
    """Fetch product details using Open Food Facts API"""
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        if 'product' in data:
            product = data['product']
            
            product_info = {
                "Title": product.get("product_name", "Unknown"),
                "Brand": product.get("brands", "Unknown"),
                "Category": product.get("categories", "Unknown"),
                "Image": product.get("image_url", "No image available"),
                "Serving Size": product.get("serving_size", "Unknown"),
                "Nutrients per 10g": product.get("nutriments", {})
            }

            # Get nutrient profiling
            nutrient_analysis = nutrient_profiling(product_info["Nutrients per 10g"])

            # Get ingredient profiling
            ingredients_text = product.get("ingredients_text", "No ingredients found.")
            ingredient_analysis = ingredient_profiling(ingredients_text)

            # Add to product_info
            product_info["Nutrient Profiling"] = nutrient_analysis
            product_info["Ingredient Profiling"] = ingredient_analysis

            return product_info
        else:
            return {"Error": "No product found for this barcode."}
    else:
        return {"Error": f"API request failed with status code {response.status_code}"}


def decode_from_scan(barcode_data):
    """Decodes scanned barcode and prints evaluation"""
    print(f"\n[Scanner] Decoded Data: {barcode_data}")
    product_info = get_product_details(barcode_data)

    if "Error" in product_info:
        print("\n", product_info["Error"])
    else:
        # print(json.dumps(product_info, indent=4, sort_keys=False, ensure_ascii=False))

        # Print evaluation results
        print("\n **Nutrient Profiling:**")
        for key, value in product_info["Nutrient Profiling"].items():
            print(f"  - {key}: {value}")

        print("\n **Ingredient Profiling:**")
        for category, items in product_info["Ingredient Profiling"].items():
            print(f"  - {category}: {', '.join(items) if items else 'None'}")
    return product_info

def decode_from_upload(barcode_data):
    """Decodes uploaded barcode and prints evaluation"""
    print(f"\n[Upload] Decoded Data: {barcode_data}")
    product_info = get_product_details(barcode_data)

    if "Error" in product_info:
        print("\n", product_info["Error"])
    else:
        # print(json.dumps(product_info, indent=4, sort_keys=False, ensure_ascii=False))

        # Print evaluation results
        print("\n **Nutrient Profiling:**")
        for key, value in product_info["Nutrient Profiling"].items():
            print(f"  - {key}: {value}")

        print("\n **Ingredient Profiling:**")
        for category, items in product_info["Ingredient Profiling"].items():
            print(f"  - {category}: {', '.join(items) if items else 'None'}")

    return product_info






# Get the width of the console
console_width = os.get_terminal_size().columns


# barcode = '8904083300021'
# print(get_product_details(barcode))