def nutrient_profiling(nutrients):
    """Evaluate the healthiness of the product based on nutrients per 10g"""
    nutrient_info = {
        "Nutrients per 10g": {
            "energy-kcal": nutrients.get("energy-kcal_100g", 0) / 10,
            "sugars": nutrients.get("sugars_100g", 0) / 10,
            "fat": nutrients.get("fat_100g", 0) / 10,
            "proteins": nutrients.get("proteins_100g", 0) / 10,
            "sodium": nutrients.get("sodium_100g", 0) / 10
        }
    }

    # Health Evaluation
    sugar = nutrient_info["Nutrients per 10g"]["sugars"]
    fat = nutrient_info["Nutrients per 10g"]["fat"]
    

    if sugar > 1.0 or fat > 0.5:
        nutrient_info["Health Evaluation"] = "Less Nutrious"
    elif sugar == 0 and fat == 0:
        nutrient_info["Health Evaluation"] = "Nutrious"
    else:
        nutrient_info["Health Evaluation"] = "Highly Nutrious "

    return nutrient_info


def ingredient_profiling(ingredients_text):
    """Categorize ingredients into organic, chemical, and overlapping (both organic and chemical)."""
    organic_keywords = [
        "natural", "organic", "wheat", "sugar", "salt", "honey", "fruit", "vegetable", 
        "spice", "herb", "flour", "oil", "water", "milk", "butter", "egg", "turmeric", 
        "cumin", "coriander", "ginger", "garlic", "onion", "tomato", "mustard", "coconut", 
        "sunflower", "jaggery", "curry leaves", "mint", "cilantro"
    ]
    chemical_keywords = [
        "aspartame", "phosphoric acid", "acesulfame k", "e150d", "preservative", 
        "artificial flavor", "artificial color", "sodium benzoate", "potassium sorbate", 
        "monosodium glutamate", "msg", "xanthan gum", "guar gum", "citric acid", 
        "acetic acid", "tartrazine", "caramel color"
    ]
    
    ingredients = ingredients_text.lower().split(", ")
    
    organic = [ing for ing in ingredients if any(word in ing for word in organic_keywords)]
    chemical = [ing for ing in ingredients if any(word in ing for word in chemical_keywords)]
    overlapping = [ing for ing in ingredients if ing in organic and ing in chemical]
    other = [ing for ing in ingredients if ing not in organic and ing not in chemical]

    result = {}
    if organic:
        result["Organic"] = organic
    if chemical:
        result["Chemical"] = chemical
    if overlapping:
        result["Overlapping"] = overlapping
    if other:
        result["Other"] = other
    return result