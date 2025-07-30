#!/usr/bin/env python3
"""
Generate theme template for Gradio Themer component
Usage: python generate_theme_template.py --name "My Theme" --background "#ffffff"
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Any


def generate_theme_template(
    theme_name: str, background_color: str = "#ffffff"
) -> Dict[str, Any]:
    """
    Generate a theme template with sensible defaults

    Args:
        theme_name: Display name for the theme
        background_color: Main background color for the theme

    Returns:
        Dictionary containing the complete theme configuration
    """
    theme_key = theme_name.lower().replace(" ", "_").replace("-", "_")

    template = {
        "themes": {
            theme_key: {
                "name": theme_name,
                "colors": {
                    # Base colors - main backgrounds and text
                    "base-100": "#ffffff",  # Main background
                    "base-200": "#f8fafc",  # Secondary background
                    "base-300": "#e2e8f0",  # Border color
                    "base-content": "#1e293b",  # Main text color
                    # Primary colors - main action buttons
                    "primary": "#3b82f6",  # Primary button color
                    "primary-content": "#ffffff",  # Primary button text
                    # Secondary colors - secondary actions
                    "secondary": "#64748b",  # Secondary button color
                    "secondary-content": "#ffffff",  # Secondary button text
                    # Accent colors - highlights and special elements
                    "accent": "#f59e0b",  # Accent color
                    "accent-content": "#000000",  # Accent text color
                    # Neutral colors - neutral elements
                    "neutral": "#374151",  # Neutral color
                    "neutral-content": "#ffffff",  # Neutral text color
                    # Status colors
                    "error": "#ef4444",  # Error color
                    "error-content": "#ffffff",  # Error text color
                },
                "background": background_color,  # Overall theme background
            }
        },
        "default_theme": theme_key,
        "default_font": "Inter",
    }

    return template


def add_theme_to_existing_config(
    config_path: str, theme_name: str, background_color: str = "#ffffff"
) -> bool:
    """
    Add a new theme to an existing configuration file

    Args:
        config_path: Path to existing configuration file
        theme_name: Name of the new theme
        background_color: Background color for the theme

    Returns:
        True if successful, False otherwise
    """
    try:
        # Load existing config
        with open(config_path, "r") as f:
            config = json.load(f)

        # Generate new theme
        new_template = generate_theme_template(theme_name, background_color)
        theme_key = list(new_template["themes"].keys())[0]

        # Add to existing themes
        if "themes" not in config:
            config["themes"] = {}

        config["themes"][theme_key] = new_template["themes"][theme_key]

        # Write back to file
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        return True

    except Exception as e:
        print(f"❌ Error adding theme to existing config: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate Gradio theme template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate new theme config file
  python generate_theme_template.py --name "My Theme"
  
  # Generate with custom background
  python generate_theme_template.py --name "Dark Theme" --background "#1f2937"
  
  # Add to existing config file
  python generate_theme_template.py --name "New Theme" --add-to existing_themes.json
  
  # Generate with custom output path
  python generate_theme_template.py --name "Corporate" --output corporate_themes.json
        """,
    )

    parser.add_argument("--name", required=True, help="Theme display name")
    parser.add_argument(
        "--background", default="#ffffff", help="Background color (default: #ffffff)"
    )
    parser.add_argument(
        "--output",
        default="user_themes.json",
        help="Output file path (default: user_themes.json)",
    )
    parser.add_argument(
        "--add-to",
        dest="add_to",
        help="Add theme to existing config file instead of creating new one",
    )

    args = parser.parse_args()

    if args.add_to:
        # Add to existing configuration
        if not Path(args.add_to).exists():
            print(f"❌ Configuration file {args.add_to} does not exist")
            return 1

        if add_theme_to_existing_config(args.add_to, args.name, args.background):
            print(f"✅ Added theme '{args.name}' to {args.add_to}")
            print(f"📝 Edit the file to customize colors further")
        else:
            print(f"❌ Failed to add theme to {args.add_to}")
            return 1
    else:
        # Generate new configuration file
        template = generate_theme_template(args.name, args.background)

        # Write to file
        with open(args.output, "w") as f:
            json.dump(template, f, indent=2)

        print(f"✅ Generated theme template: {args.output}")
        print(f"📝 Edit the file to customize colors and add more themes")
        print(f"🎨 Theme key: {list(template['themes'].keys())[0]}")

    return 0


if __name__ == "__main__":
    exit(main())
