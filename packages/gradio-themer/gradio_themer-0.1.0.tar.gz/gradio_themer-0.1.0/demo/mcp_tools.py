import os
import json
import random
import colorsys
import re
import subprocess
import sys
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
import requests

# CRITICAL: Enable MCP server mode
os.environ["GRADIO_MCP_SERVER"] = "True"

# Model API configuration for CSS to theme conversion
AVAILABLE_MODELS = {
    "qwen": {
        "hf_model": "Qwen/Qwen2.5-Coder-7B",
        "nebius_model": "Qwen/Qwen2.5-Coder-7B",
        "name": "Qwen2.5-Coder-7B",
    },
    "llama": {
        "hf_model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "nebius_model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "name": "Meta-Llama-3.1-8B-Instruct",
    },
}

# Nebius Studio API configuration
NEBIUS_API_URL = "https://api.studio.nebius.ai/v1/chat/completions"


def setup_package() -> Dict[str, Any]:
    """
    Install and verify the gradio-themer package is available and working.

    Returns:
        Dict[str, Any]: Status information about package installation
    """
    try:
        # Test import to verify package is available
        from gradio_themer import GradioThemer

        return {
            "status": "success",
            "message": "✅ gradio-themer package is installed and working",
            "package_info": {
                "name": "gradio_themer",
                "class": "GradioThemer",
                "version": "0.1.0",
            },
            "usage_example": """
import gradio as gr
from gradio_themer import GradioThemer

with gr.Blocks() as demo:
    themer = GradioThemer(label="Theme Selector")
    themer.change(fn=handle_theme_change, inputs=[themer])
""",
        }
    except ImportError as e:
        return {
            "status": "error",
            "message": f"❌ gradio-themer package not found: {str(e)}",
            "solution": "Install with: pip install gradio-themer",
        }
    except Exception as e:
        return {"status": "error", "message": f"❌ Error testing package: {str(e)}"}


def generate_theme(
    theme_name: str,
    primary_color: str = "#3b82f6",
    theme_style: str = "light",
    accent_color: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a complete theme JSON configuration with intelligent color harmonies.

    Args:
        theme_name (str): Name for the new theme
        primary_color (str): Primary color in hex format (e.g., "#3b82f6")
        theme_style (str): Theme style - "light", "dark", or "auto"
        accent_color (Optional[str]): Optional accent color, auto-generated if not provided

    Returns:
        Dict[str, Any]: Complete theme configuration ready for use
    """
    try:
        # Generate intelligent color palette based on primary color
        colors = _generate_color_palette(primary_color, theme_style, accent_color)

        # Create theme configuration
        theme_config = {
            theme_name.lower().replace(" ", "_"): {
                "name": theme_name,
                "colors": colors,
                "background": colors["base-200"],
                "style": theme_style,
                "generated": True,
                "font": {
                    "family": "Inter",
                    "type": "google_font",
                    "name": "Inter",
                },
            }
        }

        return {
            "status": "success",
            "message": f"✅ Generated theme '{theme_name}' with {theme_style} style",
            "theme_config": theme_config,
            "usage_instructions": f"""
1. Save this JSON to your user_themes.json file
2. Use in your Gradio app:
   themer = GradioThemer(
       value={{"currentTheme": "{theme_name.lower().replace(' ', '_')}"}},
       theme_config_path="user_themes.json"
   )
""",
            "color_info": {
                "primary": colors["primary"],
                "background": colors["base-200"],
                "text": colors["base-content"],
                "accent": colors["accent"],
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"❌ Error generating theme: {str(e)}",
            "suggestion": "Check that primary_color is in valid hex format (e.g., '#3b82f6')",
        }


def convert_css_to_theme(
    css_input: str,
    theme_name: str = "converted_theme",
    user_token: str = "",
    model_choice: str = "qwen",
) -> str:
    """
    Convert CSS styles or style descriptions into standardized theme JSON format using HF hosted LLM.

    Args:
        css_input (str): CSS code or natural language style description
        theme_name (str): Name for the converted theme
        user_token (str): Optional Nebius API token for better performance
        model_choice (str): AI model to use ("qwen" or "llama")

    Returns:
        str: JSON string of converted theme configuration
    """
    if not css_input.strip():
        return json.dumps(
            {
                "status": "error",
                "message": "Please provide CSS code or describe your desired style.",
            },
            indent=2,
        )

    try:
        # Create the prompt with schema definition
        SCHEMA = """{
  "themes": {
    "generated_theme": {
      "name": "Generated Theme",
      "colors": {
        "base-100": "#ffffff",
        "base-200": "#f8fafc", 
        "base-300": "#e2e8f0",
        "base-content": "#1e293b",
        "primary": "#3b82f6",
        "primary-content": "#ffffff",
        "secondary": "#64748b",
        "secondary-content": "#ffffff",
        "accent": "#f59e0b",
        "accent-content": "#000000",
        "neutral": "#374151",
        "neutral-content": "#ffffff",
        "error": "#ef4444",
        "error-content": "#ffffff"
      },
      "background": "#f1f5f9",
      "font": {
        "family": "Inter",
        "type": "google_font",
        "name": "Inter"
      }
    }
  }
}"""

        ALPACA_PROMPT = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
Convert the provided CSS code or style description into a JSON theme configuration that follows the exact schema structure. Extract colors from CSS variables, class names, or generate appropriate colors based on the description. Return ONLY valid JSON that matches the schema format.

Expected JSON Schema:
{schema}

### Input:
{input_text}

### Response:
"""

        prompt = ALPACA_PROMPT.format(schema=SCHEMA, input_text=css_input)

        # Use the AI API to convert CSS to theme
        result = _query_ai_api(prompt, user_token, model_choice)

        # Process the AI response
        generated_text = ""

        if user_token and user_token.strip():
            # Handle Nebius API response (OpenAI format)
            if isinstance(result, dict):
                if "error" in result or "detail" in result:
                    error_msg = result.get(
                        "error", result.get("detail", "Unknown error")
                    )
                    if (
                        "authentication" in str(error_msg).lower()
                        or "unauthorized" in str(error_msg).lower()
                    ):
                        return json.dumps(
                            {
                                "status": "error",
                                "message": "❌ Invalid Nebius API token provided. Please check your Nebius API key.",
                            },
                            indent=2,
                        )
                    else:
                        return json.dumps(
                            {
                                "status": "error",
                                "message": f"❌ Nebius API error: {error_msg}",
                            },
                            indent=2,
                        )
                elif "choices" in result and len(result["choices"]) > 0:
                    generated_text = (
                        result["choices"][0].get("message", {}).get("content", "")
                    )
                else:
                    return json.dumps(
                        {
                            "status": "error",
                            "message": f"❌ Unexpected Nebius API response format",
                        },
                        indent=2,
                    )
        else:
            # Handle HuggingFace Zero API response
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get("generated_text", "")
            elif isinstance(result, dict):
                if "error" in result:
                    if "loading" in result["error"].lower():
                        return json.dumps(
                            {
                                "status": "error",
                                "message": f"🔄 Model is still loading on HuggingFace servers. Please try again in a few moments.",
                            },
                            indent=2,
                        )
                    else:
                        return json.dumps(
                            {
                                "status": "error",
                                "message": f"❌ HuggingFace API error: {result['error']}",
                            },
                            indent=2,
                        )
                generated_text = result.get("generated_text", "")

        if not generated_text:
            return json.dumps(
                {
                    "status": "error",
                    "message": "❌ No response generated. Please try again or rephrase your request.",
                },
                indent=2,
            )

        # Clean up and extract JSON from response
        json_part = _extract_json_from_response(generated_text)

        if json_part.startswith("❌"):
            return json.dumps({"status": "error", "message": json_part}, indent=2)

        # Try to parse and validate the JSON
        try:
            parsed_json = json.loads(json_part)

            # Ensure proper structure
            if "themes" in parsed_json:
                for theme_key, theme_data in parsed_json["themes"].items():
                    if "background" not in theme_data:
                        theme_data["background"] = theme_data.get("colors", {}).get(
                            "base-100", "#ffffff"
                        )
                    if "font" not in theme_data:
                        theme_data["font"] = {
                            "family": "Inter",
                            "type": "google_font",
                            "name": "Inter",
                        }

            return json.dumps(parsed_json, indent=2)

        except json.JSONDecodeError as e:
            return json.dumps(
                {
                    "status": "error",
                    "message": f"❌ AI model generated invalid JSON. Please try rephrasing your request.\n\nError: {str(e)}",
                },
                indent=2,
            )

    except Exception as e:
        return json.dumps(
            {
                "status": "error",
                "message": f"❌ Error converting CSS to theme: {str(e)}",
            },
            indent=2,
        )


def generate_app_code(
    theme_names: str = "ocean_breeze,sunset_orange",
    app_title: str = "My Themed App",
    include_components: str = "button,textbox,slider",
) -> str:
    """
    Generate complete Gradio application code with integrated theming system.

    Args:
        theme_names (str): Comma-separated list of theme names to include
        app_title (str): Title for the generated application
        include_components (str): Comma-separated list of components to include

    Returns:
        str: Complete Python code for a themed Gradio application
    """
    try:
        # Parse input parameters
        themes = [t.strip() for t in theme_names.split(",") if t.strip()]
        components = [
            c.strip().lower() for c in include_components.split(",") if c.strip()
        ]

        # Generate the complete app code
        app_code = f'''"""
{app_title}
A themed Gradio application generated with gradio-themer
"""

import gradio as gr
from gradio_themer import GradioThemer
import json

def handle_theme_change(theme_data):
    """Handle theme changes from the GradioThemer component"""
    print(f"Theme changed to: {{theme_data.get('currentTheme', 'default')}}")
    return theme_data

# Custom CSS for enhanced styling
custom_css = """
.theme-container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}}

.section {{
    margin-bottom: 2rem;
    padding: 1.5rem;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    background: #fafafa;
}}
"""

# Build the {app_title}
with gr.Blocks(css=custom_css, title="{app_title}") as demo:
    
    # Header
    with gr.Column(elem_classes="theme-container"):
        gr.Markdown("# {app_title}")
        gr.Markdown("**Powered by gradio-themer** - Dynamic theme system")
    
    # Theme Controller
    themer = GradioThemer(
        value={{
            "currentTheme": "{themes[0] if themes else 'ocean_breeze'}",
            "type": "custom",
            "removeBorders": True
        }},
        label="🎨 Theme Selector",
        theme_config_path="user_themes.json"
    )
    
    # Main content sections
    with gr.Column(elem_classes="theme-container"):
'''

        # Add components based on user selection
        if "button" in components:
            app_code += """
        # Button demonstration
        with gr.Column(elem_classes="section"):
            gr.Markdown("### Button Components")
            with gr.Row():
                btn_primary = gr.Button("Primary Action", variant="primary")
                btn_secondary = gr.Button("Secondary Action", variant="secondary") 
                btn_stop = gr.Button("Stop Action", variant="stop")
"""

        if "textbox" in components:
            app_code += """
        # Text input demonstration  
        with gr.Column(elem_classes="section"):
            gr.Markdown("### Text Input Components")
            text_input = gr.Textbox(
                label="Enter your text", 
                placeholder="Type something here...",
                lines=3
            )
            text_output = gr.Textbox(label="Output", interactive=False)
"""

        if "slider" in components:
            app_code += """
        # Slider demonstration
        with gr.Column(elem_classes="section"):
            gr.Markdown("### Slider Components")
            slider_value = gr.Slider(
                minimum=0, 
                maximum=100, 
                value=50,
                label="Adjust Value"
            )
            slider_output = gr.Number(label="Current Value", value=50)
"""

        if "dropdown" in components:
            app_code += """
        # Dropdown demonstration
        with gr.Column(elem_classes="section"):
            gr.Markdown("### Selection Components")
            dropdown = gr.Dropdown(
                choices=["Option 1", "Option 2", "Option 3"],
                label="Choose an option",
                value="Option 1"
            )
            radio = gr.Radio(
                choices=["Choice A", "Choice B", "Choice C"],
                label="Select one",
                value="Choice A"
            )
"""

        # Add event handlers
        app_code += """
    # Event handlers
    themer.change(fn=handle_theme_change, inputs=[themer])
    
"""

        # Add simple interactions if textbox is included
        if "textbox" in components:
            app_code += """    # Simple text processing
    def process_text(text):
        return f"Processed: {text.upper()}"
    
    text_input.change(fn=process_text, inputs=[text_input], outputs=[text_output])
"""

        # Add slider interaction if slider is included
        if "slider" in components:
            app_code += """    # Slider value update
    slider_value.change(fn=lambda x: x, inputs=[slider_value], outputs=[slider_output])
"""

        # Launch configuration
        app_code += """
# Launch the application
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )
"""

        return app_code

    except Exception as e:
        return f"""# Error generating app code
# {str(e)}

import gradio as gr

with gr.Blocks(title="Error") as demo:
    gr.Markdown("❌ Failed to generate app code. Please check your parameters.")

if __name__ == "__main__":
    demo.launch()
"""


# Helper functions for theme generation and API calls


def _generate_color_palette(
    primary_color: str, style: str, accent_color: Optional[str] = None
) -> Dict[str, str]:
    """Generate a complete color palette based on primary color and style"""
    try:
        # Convert primary color to RGB for calculations
        rgb = _hex_to_rgb(primary_color)
        hsl = _rgb_to_hsl(rgb)

        # Generate base colors based on style
        if style == "dark":
            base_100 = "#1a1a1a"
            base_200 = "#2d2d2d"
            base_300 = "#404040"
            base_content = "#ffffff"
        else:  # light style
            base_100 = "#ffffff"
            base_200 = "#f8fafc"
            base_300 = "#e2e8f0"
            base_content = "#1e293b"

        # Generate accent color if not provided
        if not accent_color:
            accent_color = _generate_complementary_color(primary_color, 0.1)

        # Generate secondary color (triadic)
        secondary_color = _generate_triadic_color(primary_color)

        # Create complete color palette
        colors = {
            "base-100": base_100,
            "base-200": base_200,
            "base-300": base_300,
            "base-content": base_content,
            "primary": primary_color,
            "primary-content": "#ffffff" if style == "light" else "#000000",
            "secondary": secondary_color,
            "secondary-content": "#ffffff",
            "accent": accent_color,
            "accent-content": "#ffffff",
            "neutral": "#374151",
            "neutral-content": "#ffffff",
            "error": "#ef4444",
            "error-content": "#ffffff",
        }

        return colors

    except Exception:
        # Fallback to default colors
        return {
            "base-100": "#ffffff",
            "base-200": "#f8fafc",
            "base-300": "#e2e8f0",
            "base-content": "#1e293b",
            "primary": primary_color,
            "primary-content": "#ffffff",
            "secondary": "#64748b",
            "secondary-content": "#ffffff",
            "accent": "#f59e0b",
            "accent-content": "#000000",
            "neutral": "#374151",
            "neutral-content": "#ffffff",
            "error": "#ef4444",
            "error-content": "#ffffff",
        }


def _query_ai_api(prompt: str, user_token: str = "", model_choice: str = "qwen"):
    """Query AI API - Use Nebius if token provided, otherwise HF Zero inference"""
    model_config = AVAILABLE_MODELS.get(model_choice, AVAILABLE_MODELS["qwen"])

    if user_token and user_token.strip():
        # Use Nebius Studio API with provided token
        headers = {
            "Authorization": f"Bearer {user_token.strip()}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model_config["nebius_model"],
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.3,
            "top_p": 0.9,
        }

        response = requests.post(NEBIUS_API_URL, headers=headers, json=payload)
        return response.json()

    else:
        # Use HuggingFace Zero Inference API (no token required)
        hf_inference_url = (
            f"https://api-inference.huggingface.co/models/{model_config['hf_model']}"
        )

        headers = {"Content-Type": "application/json"}

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1000,
                "temperature": 0.3,
                "top_p": 0.9,
                "do_sample": True,
                "return_full_text": False,
            },
        }

        response = requests.post(hf_inference_url, headers=headers, json=payload)
        return response.json()


def _extract_json_from_response(generated_text: str) -> str:
    """Extract and clean JSON from AI response"""
    json_part = generated_text.strip()

    # Handle the case where AI returns explanation + JSON
    if "Here is the JSON theme configuration" in json_part:
        json_start = json_part.find("{")
        if json_start != -1:
            json_part = json_part[json_start:]

    # Remove code block markers
    if json_part.startswith("```json"):
        json_part = json_part[7:]
    elif json_part.startswith("```"):
        json_part = json_part[3:]
    if json_part.endswith("```"):
        json_part = json_part[:-3]
    json_part = json_part.strip()

    # Find the first { and last } to extract clean JSON
    start_idx = json_part.find("{")
    if start_idx == -1:
        return f"❌ No valid JSON found in response.\n\n**Raw response:**\n{generated_text}"

    # Find the matching closing brace
    brace_count = 0
    end_idx = -1
    for i in range(start_idx, len(json_part)):
        if json_part[i] == "{":
            brace_count += 1
        elif json_part[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break

    if end_idx == -1:
        return f"❌ Incomplete JSON found.\n\n**Raw response:**\n{generated_text}"

    return json_part[start_idx:end_idx]


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hsl(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    """Convert RGB to HSL"""
    r, g, b = [x / 255.0 for x in rgb]
    return colorsys.rgb_to_hls(r, g, b)


def _hsl_to_rgb(hsl: Tuple[float, float, float]) -> Tuple[int, int, int]:
    """Convert HSL to RGB"""
    h, l, s = hsl
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return tuple(int(x * 255) for x in (r, g, b))


def _rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def _generate_complementary_color(base_color: str, lightness_adjust: float = 0) -> str:
    """Generate complementary color"""
    try:
        rgb = _hex_to_rgb(base_color)
        h, l, s = _rgb_to_hsl(rgb)

        # Shift hue by 180 degrees for complementary
        comp_h = (h + 0.5) % 1.0
        comp_l = max(0, min(1, l + lightness_adjust))

        comp_rgb = _hsl_to_rgb((comp_h, comp_l, s))
        return _rgb_to_hex(comp_rgb)
    except:
        return "#f59e0b"  # Fallback color


def _generate_triadic_color(base_color: str) -> str:
    """Generate triadic color (120 degrees hue shift)"""
    try:
        rgb = _hex_to_rgb(base_color)
        h, l, s = _rgb_to_hsl(rgb)

        # Shift hue by 120 degrees for triadic
        triadic_h = (h + 0.33) % 1.0

        triadic_rgb = _hsl_to_rgb((triadic_h, l, s))
        return _rgb_to_hex(triadic_rgb)
    except:
        return "#64748b"  # Fallback color
