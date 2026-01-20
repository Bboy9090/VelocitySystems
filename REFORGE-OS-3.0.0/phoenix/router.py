"""OS deployment router."""
import os
import subprocess
from typing import Dict, Any, Optional, List

from .registry import get_recipe
from ..bootforge.imager import write_image


def deploy_recipe(recipe_key: str, target_dev: str, *, verify: bool = True) -> Dict[str, Any]:
    """Deploy an OS recipe to a target device."""
    recipe = get_recipe(recipe_key)
    if not recipe:
        raise ValueError(f"Recipe not found: {recipe_key}")
    
    image_path = recipe.get("image_path")
    if not image_path or not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found for recipe {recipe_key}: {image_path}")
    
    # Execute pre-steps
    pre_steps = recipe.get("pre_steps", [])
    for step in pre_steps:
        _execute_step(step)
    
    # Write image
    result = write_image(image_path, target_dev, verify=verify)
    
    # Execute post-steps
    post_steps = recipe.get("post_steps", [])
    for step in post_steps:
        _execute_step(step)
    
    return {
        "success": result["success"],
        "recipe": recipe_key,
        "target": target_dev,
        "image_written": result.get("written", 0),
        "verified": result.get("verified", False)
    }


def recommend_recipe(device_info: Dict[str, Any]) -> Optional[str]:
    """Recommend an OS recipe based on device profile."""
    # Simple matching logic - can be enhanced
    model = device_info.get("model", "").lower()
    platform = device_info.get("platform", "").lower()
    
    # Try to match device patterns
    recipes = os.listdir(os.path.join(os.path.dirname(__file__), "recipes"))
    for recipe_file in recipes:
        if recipe_file.endswith(".json"):
            recipe_key = recipe_file[:-5]
            recipe = get_recipe(recipe_key)
            if recipe:
                patterns = recipe.get("device_patterns", [])
                for pattern in patterns:
                    if pattern.lower() in model:
                        return recipe_key
    
    return None


def _execute_step(step: Dict[str, Any]) -> None:
    """Execute a deployment step."""
    step_type = step.get("type")
    if step_type == "command":
        cmd = step.get("command")
        if cmd:
            subprocess.run(cmd, shell=True, check=step.get("check", False))
    elif step_type == "wait":
        import time
        time.sleep(step.get("seconds", 1))
    # Add more step types as needed
