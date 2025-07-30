from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Callable, Sequence, Optional
from gradio.components.base import FormComponent
from gradio.events import Events


class GradioThemer(FormComponent):
    """
    A custom Gradio component for applying user-configurable themes to Gradio applications.

    This component allows users to:
    - Configure unlimited custom themes via JSON configuration files
    - Preview themes with live Gradio components
    - Switch between themes dynamically
    - Export CSS for use in other projects
    """

    EVENTS = [
        Events.change,
        Events.input,
        Events.submit,
    ]

    def __init__(
        self,
        value: Dict[str, Any] | Callable | None = None,
        theme_config_path: Optional[str] = None,
        *,
        label: str | None = None,
        every: float | None = None,
        inputs: (
            FormComponent | Sequence[FormComponent] | set[FormComponent] | None
        ) = None,
        show_label: bool | None = None,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
    ):
        """
        Parameters:
            value: Default theme configuration. Should be a dict with 'themeInput', 'themeConfig', and 'generatedCSS' keys.
            theme_config_path: Path to user themes configuration file (JSON). If None, searches for common filenames.
            label: The label for this component, displayed above the component if `show_label` is `True`.
            every: Continously calls `value` to recalculate it if `value` is a function.
            inputs: Components that are used as inputs to calculate `value` if `value` is a function.
            show_label: If True, will display label.
            scale: Relative size compared to adjacent Components.
            min_width: Minimum pixel width.
            interactive: If True, will be rendered as an editable component.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM.
            render: If False, component will not render be rendered in the Blocks context.
            key: A unique key for this component.
        """
        # Load user themes from configuration before calling super().__init__
        self.user_themes = self._load_user_themes(theme_config_path)

        super().__init__(
            label=label,
            every=every,
            inputs=inputs,
            show_label=show_label,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value,
            render=render,
            key=key,
        )

    def _load_user_themes(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load themes from user configuration file

        Args:
            config_path: Optional path to theme configuration file

        Returns:
            Dictionary containing user themes, or built-in themes as fallback
        """
        # Default paths to search for theme config
        search_paths = [
            config_path,
            "user_themes.json",
            "themes.json",
            "gradio_themes.json",
            os.path.expanduser("~/.gradio/gradio_themes.json"),
            # Also check in the component's directory for the example file
            os.path.join(
                os.path.dirname(__file__), "..", "..", "user_themes_example.json"
            ),
        ]

        for path in search_paths:
            if path and Path(path).exists():
                try:
                    with open(path, "r") as f:
                        config = json.load(f)
                        themes = config.get("themes", {})
                        if themes:
                            print(f"✅ Loaded {len(themes)} user themes from {path}")
                            return themes
                except Exception as e:
                    print(f"⚠️ Error loading theme config from {path}: {e}")
                    continue

        # Return built-in fallback themes if no config found
        print("📝 No user theme config found, using built-in themes")
        return self._get_builtin_themes()

    def _get_builtin_themes(self) -> Dict[str, Any]:
        """Get the built-in fallback themes"""
        return {
            "corporate": {
                "name": "Corporate",
                "colors": {
                    "base-100": "oklch(100% 0 0)",
                    "base-200": "oklch(96% 0.02 276.935)",
                    "base-300": "oklch(90% 0.05 293.541)",
                    "base-content": "oklch(22.389% 0.031 278.072)",
                    "primary": "oklch(58% 0.158 241.966)",
                    "primary-content": "oklch(100% 0 0)",
                    "secondary": "oklch(55% 0.046 257.417)",
                    "secondary-content": "oklch(100% 0 0)",
                    "accent": "oklch(60% 0.118 184.704)",
                    "accent-content": "oklch(100% 0 0)",
                    "neutral": "oklch(0% 0 0)",
                    "neutral-content": "oklch(100% 0 0)",
                    "error": "oklch(70% 0.191 22.216)",
                    "error-content": "oklch(0% 0 0)",
                },
                "background": "#06b6d4",
            },
            "cupcake": {
                "name": "Cupcake",
                "colors": {
                    "base-100": "oklch(100% 0 0)",
                    "base-200": "oklch(96% 0.014 340.77)",
                    "base-300": "oklch(92% 0.021 340.77)",
                    "base-content": "oklch(22.389% 0.031 278.072)",
                    "primary": "oklch(65.69% 0.196 342.55)",
                    "primary-content": "oklch(100% 0 0)",
                    "secondary": "oklch(74.51% 0.167 183.61)",
                    "secondary-content": "oklch(100% 0 0)",
                    "accent": "oklch(74.51% 0.167 183.61)",
                    "accent-content": "oklch(100% 0 0)",
                    "neutral": "oklch(22.389% 0.031 278.072)",
                    "neutral-content": "oklch(100% 0 0)",
                    "error": "oklch(70% 0.191 22.216)",
                    "error-content": "oklch(0% 0 0)",
                },
                "background": "#faf0e6",
            },
            "dark": {
                "name": "Dark",
                "colors": {
                    "base-100": "oklch(25.3% 0.015 252.417)",
                    "base-200": "oklch(22.2% 0.013 252.417)",
                    "base-300": "oklch(19.1% 0.011 252.417)",
                    "base-content": "oklch(74.6% 0.019 83.916)",
                    "primary": "oklch(65.69% 0.196 275.75)",
                    "primary-content": "oklch(100% 0 0)",
                    "secondary": "oklch(74.51% 0.167 183.61)",
                    "secondary-content": "oklch(100% 0 0)",
                    "accent": "oklch(74.51% 0.167 183.61)",
                    "accent-content": "oklch(100% 0 0)",
                    "neutral": "oklch(25.3% 0.015 252.417)",
                    "neutral-content": "oklch(74.6% 0.019 83.916)",
                    "error": "oklch(70% 0.191 22.216)",
                    "error-content": "oklch(0% 0 0)",
                },
                "background": "#1f2937",
            },
            "emerald": {
                "name": "Emerald",
                "colors": {
                    "base-100": "oklch(100% 0 0)",
                    "base-200": "oklch(96% 0.014 154.77)",
                    "base-300": "oklch(92% 0.021 154.77)",
                    "base-content": "oklch(22.389% 0.031 278.072)",
                    "primary": "oklch(65.69% 0.196 162.55)",
                    "primary-content": "oklch(100% 0 0)",
                    "secondary": "oklch(74.51% 0.167 183.61)",
                    "secondary-content": "oklch(100% 0 0)",
                    "accent": "oklch(74.51% 0.167 183.61)",
                    "accent-content": "oklch(100% 0 0)",
                    "neutral": "oklch(22.389% 0.031 278.072)",
                    "neutral-content": "oklch(100% 0 0)",
                    "error": "oklch(70% 0.191 22.216)",
                    "error-content": "oklch(0% 0 0)",
                },
                "background": "#ecfdf5",
            },
        }

    def preprocess(self, payload: Dict[str, Any] | None) -> Dict[str, Any] | None:
        """
        Parameters:
            payload: The theme configuration data from the frontend.
        Returns:
            Passes the theme configuration as a dict into the function.
        """
        if payload is None:
            return None

        # Ensure we have the expected structure
        if isinstance(payload, dict):
            # Handle different input formats
            result = {
                "themeInput": payload.get("themeInput", ""),
                "themeConfig": payload.get("themeConfig"),
                "generatedCSS": payload.get("generatedCSS", ""),
            }

            # Include additional fields if present
            if "currentTheme" in payload:
                result["currentTheme"] = payload["currentTheme"]
            if "type" in payload:
                result["type"] = payload["type"]

            return result

        return None

    def postprocess(self, value: Dict[str, Any] | None) -> Dict[str, Any] | None:
        """
        Parameters:
            value: Expects a dict with theme configuration data.
        Returns:
            The value to display in the component, including user themes.
        """
        if value is None:
            result = self._get_default_value()
        elif isinstance(value, dict):
            # Handle different input formats
            if "currentTheme" in value:
                # Handle theme selection format
                theme_name = value.get("currentTheme", "light")
                result = {
                    "currentTheme": theme_name,
                    "themeInput": value.get("themeInput", ""),
                    "themeConfig": value.get("themeConfig"),
                    "generatedCSS": value.get("generatedCSS", ""),
                    "type": value.get("type", "builtin"),
                    "font": value.get(
                        "font",
                        {"family": "Inter", "weights": ["400", "500", "600", "700"]},
                    ),
                    "removeBorders": value.get("removeBorders", True),
                }
            else:
                # Handle raw theme configuration format
                result = {
                    "themeInput": value.get("themeInput", ""),
                    "themeConfig": value.get("themeConfig"),
                    "generatedCSS": value.get("generatedCSS", ""),
                    "font": value.get(
                        "font",
                        {"family": "Inter", "weights": ["400", "500", "600", "700"]},
                    ),
                    "removeBorders": value.get("removeBorders", True),
                }
        else:
            result = self._get_default_value()

        # Inject user themes into the result for frontend consumption
        result["available_themes"] = self.user_themes

        return result

    def _get_default_value(self) -> Dict[str, Any]:
        """Get the default theme configuration"""
        emerald_theme = """@theme "emerald" {
  name: "emerald";
  default: true;
  prefersdark: false;
  color-scheme: "light";
  --color-base-100: oklch(100% 0 0);
  --color-base-200: oklch(93% 0 0);
  --color-base-300: oklch(86% 0 0);
  --color-base-content: oklch(35.519% 0.032 262.988);
  --color-primary: oklch(76.662% 0.135 153.45);
  --color-primary-content: oklch(33.387% 0.04 162.24);
  --color-secondary: oklch(61.302% 0.202 261.294);
  --color-secondary-content: oklch(100% 0 0);
  --color-accent: oklch(72.772% 0.149 33.2);
  --color-accent-content: oklch(0% 0 0);
  --color-neutral: oklch(35.519% 0.032 262.988);
  --color-neutral-content: oklch(98.462% 0.001 247.838);
  --color-info: oklch(72.06% 0.191 231.6);
  --color-info-content: oklch(0% 0 0);
  --color-success: oklch(64.8% 0.15 160);
  --color-success-content: oklch(0% 0 0);
  --color-warning: oklch(84.71% 0.199 83.87);
  --color-warning-content: oklch(0% 0 0);
  --color-error: oklch(71.76% 0.221 22.18);
  --color-error-content: oklch(0% 0 0);
  --radius-selector: 1rem;
  --radius-field: 0.5rem;
  --radius-box: 1rem;
  --size-selector: 0.25rem;
  --size-field: 0.25rem;
  --border: 1px;
  --depth: 1;
  --noise: 1;
}"""

        return {"themeInput": emerald_theme, "themeConfig": None, "generatedCSS": ""}

    def example_payload(self) -> Any:
        return {
            "themeInput": "sample theme",
            "generatedCSS": ":root { --color-primary: blue; }",
        }

    def example_value(self) -> Any:
        return {
            "themeInput": "sample theme",
            "generatedCSS": ":root { --color-primary: blue; }",
        }

    def api_info(self) -> dict[str, Any]:
        return {"type": {}, "description": "Gradio theme configuration object"}
