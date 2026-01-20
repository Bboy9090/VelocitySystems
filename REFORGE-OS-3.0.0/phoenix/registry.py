"""OS recipe registry."""
import os
import json
from typing import Dict, Any, List, Optional


RECIPES_DIR = os.path.join(os.path.dirname(__file__), "recipes")
os.makedirs(RECIPES_DIR, exist_ok=True)


def list_recipes() -> List[Dict[str, Any]]:
    """List all available OS recipes."""
    recipes = []
    for filename in os.listdir(RECIPES_DIR):
        if filename.endswith(".json"):
            recipe_path = os.path.join(RECIPES_DIR, filename)
            try:
                with open(recipe_path, "r", encoding="utf-8") as f:
                    recipe = json.load(f)
                    recipes.append(recipe)
            except Exception as e:
                print(f"Error loading recipe {filename}: {e}")
    return recipes


def get_recipe(key: str) -> Optional[Dict[str, Any]]:
    """Get a specific recipe by key."""
    recipe_path = os.path.join(RECIPES_DIR, f"{key}.json")
    if not os.path.exists(recipe_path):
        return None
    
    try:
        with open(recipe_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading recipe {key}: {e}")
        return None


def register_recipe(recipe: Dict[str, Any]) -> str:
    """Register a new recipe."""
    key = recipe.get("key") or recipe.get("name", "unknown").lower().replace(" ", "_")
    recipe_path = os.path.join(RECIPES_DIR, f"{key}.json")
    
    with open(recipe_path, "w", encoding="utf-8") as f:
        json.dump(recipe, f, indent=2, ensure_ascii=False)
    
    return key
