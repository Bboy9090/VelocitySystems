#!/usr/bin/env python3
"""Phoenix Key API CLI - JSON interface for Tauri."""
import sys
import json
import argparse
from phoenix.registry import list_recipes, get_recipe
from phoenix.router import deploy_recipe, recommend_recipe
from phoenix.device_info import get_target_profile


def cmd_list(args):
    """List all recipes."""
    recipes = list_recipes()
    if args.json:
        print(json.dumps(recipes, indent=2))
    else:
        print("\n=== OS RECIPES ===")
        for recipe in recipes:
            print(f"{recipe.get('key', 'unknown'):20} {recipe.get('name', 'Unknown')}")


def cmd_get(args):
    """Get a specific recipe."""
    recipe = get_recipe(args.key)
    if not recipe:
        print(f"Recipe not found: {args.key}", file=sys.stderr)
        sys.exit(1)
    
    print(json.dumps(recipe, indent=2))


def cmd_deploy(args):
    """Deploy a recipe."""
    result = deploy_recipe(args.recipe, args.target, verify=args.verify)
    print(json.dumps(result, indent=2))


def cmd_recommend(args):
    """Recommend a recipe for a device."""
    profile = get_target_profile(args.device if args.device else None)
    recipe_key = recommend_recipe(profile)
    
    if recipe_key:
        result = {"recommended": recipe_key, "device": profile}
    else:
        result = {"recommended": None, "device": profile}
    
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Phoenix Key API")
    subparsers = parser.add_subparsers(dest="command", help="Command")
    
    list_parser = subparsers.add_parser("list", help="List recipes")
    list_parser.add_argument("--json", action="store_true", help="JSON output")
    
    get_parser = subparsers.add_parser("get", help="Get recipe")
    get_parser.add_argument("key", help="Recipe key")
    
    deploy_parser = subparsers.add_parser("deploy", help="Deploy recipe")
    deploy_parser.add_argument("recipe", help="Recipe key")
    deploy_parser.add_argument("target", help="Target device")
    deploy_parser.add_argument("--no-verify", dest="verify", action="store_false", default=True, help="Skip verification")
    
    recommend_parser = subparsers.add_parser("recommend", help="Recommend recipe")
    recommend_parser.add_argument("--device", help="Device ID")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == "list":
            cmd_list(args)
        elif args.command == "get":
            cmd_get(args)
        elif args.command == "deploy":
            cmd_deploy(args)
        elif args.command == "recommend":
            cmd_recommend(args)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
