"""Recipe verification and validation."""
import hashlib
import os
from typing import Dict, Any, Optional

from .registry import get_recipe


def verify_recipe_hash(recipe_key: str, image_path: str) -> bool:
    """Verify that an image file matches the recipe's expected hash."""
    recipe = get_recipe(recipe_key)
    if not recipe:
        return False
    
    expected_hash = recipe.get("image_sha256")
    if not expected_hash:
        # No hash specified in recipe, skip verification
        return True
    
    # Calculate actual hash
    sha256 = hashlib.sha256()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    actual_hash = sha256.hexdigest()
    
    return actual_hash.lower() == expected_hash.lower()


def validate_recipe(recipe: Dict[str, Any]) -> List[str]:
    """Validate a recipe structure and return list of errors."""
    errors = []
    
    required_fields = ["key", "name", "image_path"]
    for field in required_fields:
        if field not in recipe:
            errors.append(f"Missing required field: {field}")
    
    image_path = recipe.get("image_path")
    if image_path and not os.path.exists(image_path):
        errors.append(f"Image file not found: {image_path}")
    
    return errors
