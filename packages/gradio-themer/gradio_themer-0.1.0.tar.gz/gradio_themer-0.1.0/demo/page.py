import gradio as gr
from gradio.themes.utils import fonts
import json
import random
import subprocess
import sys
from pathlib import Path
import requests
import os

# CRITICAL: Enable MCP server mode (as per GRADIO_MCP_HF_SPACES_GUIDE.md)
os.environ["GRADIO_MCP_SERVER"] = "True"

# Import MCP tools from mcp_tools.py to make them available for the MCP server
try:
    from mcp_tools import (
        setup_package,
        generate_theme,
        convert_css_to_theme,
        generate_app_code,
    )

    print("✅ MCP tools imported successfully")
except ImportError as e:
    print(f"⚠️ Could not import MCP tools: {e}")

# New imports for HuggingFace Inference API
try:
    import requests

    HF_REQUESTS_AVAILABLE = True
    print("✅ HuggingFace Inference API available")
except ImportError:
    HF_REQUESTS_AVAILABLE = False
    print("⚠️ requests library not available")

try:
    from gradio_themer import GradioThemer

    THEMER_AVAILABLE = True
    print("✅ Using renamed GradioThemer package (gradio_themer-0.1.0)")
except ImportError:
    print("⚠️ GradioThemer not available, themes will not work")
    THEMER_AVAILABLE = False

# Model API configuration
# Available models for both HF Zero and Nebius inference
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


def query_ai_api(prompt, user_token=None, model_choice="qwen"):
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


def convert_css_to_theme_json_ai(input_text, user_token="", model_choice="qwen"):
    # Internal UI function - not for MCP discovery
    if not input_text.strip():
        return "Please provide CSS code or describe your desired style."

    if not HF_REQUESTS_AVAILABLE:
        return "❌ requests library is required for API calls. Please install with: pip install requests"

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

        prompt = ALPACA_PROMPT.format(schema=SCHEMA, input_text=input_text)

        model_name = AVAILABLE_MODELS[model_choice]["name"]
        api_type = "Nebius" if user_token and user_token.strip() else "HuggingFace Zero"
        print(f"🤖 Generating theme with {model_name} via {api_type}...")

        try:
            result = query_ai_api(prompt, user_token, model_choice)

            # Handle different response formats
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
                            or "invalid authentication token" in str(error_msg).lower()
                        ):
                            return "❌ Invalid Nebius API token provided. Please check your Nebius API key and try again."
                        else:
                            return f"❌ Nebius API error: {error_msg}"
                    elif "choices" in result and len(result["choices"]) > 0:
                        generated_text = (
                            result["choices"][0].get("message", {}).get("content", "")
                        )
                    else:
                        return "❌ Unexpected Nebius API response format"
                else:
                    return "❌ Unexpected Nebius API response format"
            else:
                # Handle HuggingFace API response
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                elif isinstance(result, dict):
                    if "error" in result:
                        if "loading" in str(result["error"]).lower():
                            return "⏳ Model is loading on HuggingFace. Please try again in a few moments."
                        return f"❌ HuggingFace API error: {result['error']}"
                    else:
                        generated_text = result.get("generated_text", "")

            if not generated_text.strip():
                return "❌ No response received from AI model. Please try again."

            # Try to extract JSON from the response
            try:
                # Look for JSON in the response
                start_idx = generated_text.find("{")
                if start_idx == -1:
                    return f"❌ No valid JSON found in response:\n\n{generated_text}"

                # Find the matching closing brace
                brace_count = 0
                end_idx = -1
                for i in range(start_idx, len(generated_text)):
                    if generated_text[i] == "{":
                        brace_count += 1
                    elif generated_text[i] == "}":
                        brace_count -= 1
                        if brace_count == 0:
                            end_idx = i + 1
                            break

                if end_idx == -1:
                    return f"❌ Incomplete JSON in response:\n\n{generated_text}"

                json_str = generated_text[start_idx:end_idx]

                # Validate JSON
                parsed_json = json.loads(json_str)

                # Pretty format the JSON
                formatted_json = json.dumps(parsed_json, indent=2)

                return formatted_json

            except json.JSONDecodeError as e:
                return f"❌ Invalid JSON generated:\n\nJSON Error: {str(e)}\n\nRaw Response:\n{generated_text}"

        except requests.exceptions.RequestException as e:
            return f"❌ Network error: {str(e)}"
        except Exception as e:
            return f"❌ Unexpected error during AI processing: {str(e)}"

    except Exception as e:
        return f"❌ Error: {str(e)}"


def apply_random_theme():
    # Internal UI function - not for MCP discovery
    # Load the actual theme data to get all available themes
    themes_file = Path(__file__).parent / "user_themes.json"

    try:
        with open(themes_file, "r", encoding="utf-8") as f:
            theme_data = json.load(f)

        if not theme_data.get("themes"):
            return (
                {"currentTheme": "default", "type": "builtin"},
                "❌ No themes found in user_themes.json",
            )

        # Get all available theme keys
        theme_keys = list(theme_data["themes"].keys())
        if not theme_keys:
            return (
                {"currentTheme": "default", "type": "builtin"},
                "❌ No themes available",
            )

        # Select a random theme
        random_theme_key = random.choice(theme_keys)
        random_theme = theme_data["themes"][random_theme_key]

        print(f"🎲 Randomly selected theme: {random_theme_key}")

        # Update the component state
        new_state = {
            "currentTheme": random_theme_key,
            "type": "custom",
            "themeConfig": random_theme,
            "font": random_theme.get("font", {"family": "Inter", "weights": ["400"]}),
            "removeBorders": True,
        }

        return (
            new_state,
            f"✅ Applied random theme: {random_theme.get('name', random_theme_key)}",
        )

    except FileNotFoundError:
        return (
            {"currentTheme": "default", "type": "builtin"},
            "❌ Theme file not found: user_themes.json",
        )
    except json.JSONDecodeError as e:
        return (
            {"currentTheme": "default", "type": "builtin"},
            f"❌ Invalid JSON in theme file: {str(e)}",
        )
    except Exception as e:
        return (
            {"currentTheme": "default", "type": "builtin"},
            f"❌ Error loading theme: {str(e)}",
        )


# def start_mcp_server():
#     """Start the MCP server in background"""
#     try:
#         mcp_process = subprocess.Popen(
#             [sys.executable, "mcp_server.py"],
#             cwd=Path(__file__).parent,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#         )
#         return "✅ MCP Server started successfully! Use stdio transport to connect."
#     except Exception as e:
#         return f"❌ Failed to start MCP server: {str(e)}"


# Custom CSS for minimal design (no @import allowed in Gradio)
custom_css = """
.header-container {
    text-align: center;
    padding: 1rem 1rem;
    border-bottom: 1px solid #e5e7eb;
    margin-bottom: 1rem;
}

.main-sections {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 1rem 0rem 1rem;
}

.section {
    margin-bottom: 0.75rem;
    padding: 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    background: #fafafa;
}

.mcp-info {
    background: #f0f9ff;
    border-color: #0ea5e9;
}

/* Override Gradio's default spacing and remove nested borders */
.gradio-container .block {
    margin: 0.5rem 0 !important;
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

.gradio-container .gr-column {
    gap: 0.5rem !important;
}

/* Remove nested styling from textbox containers */
.section .gradio-container .gr-textbox,
.section .gradio-container .gr-code {
    border: 1px solid #d1d5db !important;
    border-radius: 6px !important;
    background: white !important;
}

/* Ensure code output is selectable and copy button works */
.gr-code .language-json,
.gr-code pre,
.gr-code code {
    user-select: text !important;
    -webkit-user-select: text !important;
    -moz-user-select: text !important;
    -ms-user-select: text !important;
}

/* Make sure copy button is visible and functional */
.gr-code .copy-button,
.gr-code button[aria-label*="copy"],
.gr-code button[title*="copy"] {
    opacity: 1 !important;
    visibility: visible !important;
    pointer-events: auto !important;
}

/* Add margin to bottom footer/button area */
.gradio-container footer,
.gradio-container .footer,
.gradio-container > div:last-child,
footer {
    margin-bottom: 2rem !important;
    padding-bottom: 2rem !important;
}

/* Add bottom margin to the entire Gradio container */
.gradio-container {
    margin-bottom: 3rem !important;
    padding-bottom: 2rem !important;
}
"""

# Build the demo interface with Gradio's built-in font system
with gr.Blocks(css=custom_css, title="Gradio Themer - Demo & MCP Server") as demo:

    # Header
    with gr.Column(elem_classes="header-container"):
        gr.Markdown("# 🎨 Gradio Themer")
        gr.Markdown(
            "**Demo & MCP Server** - Dynamic theme system for Gradio applications"
        )

    # Add the working GradioThemer component
    if THEMER_AVAILABLE:
        themer = GradioThemer(
            value={
                "currentTheme": "corporate",
                "type": "builtin",
                "font": {"family": "Poppins", "weights": ["400", "500", "600", "700"]},
                "removeBorders": True,
                "themeInput": "",
                "themeConfig": None,
                "generatedCSS": "",
            },
            visible=False,
            label="Theme Controller (for debugging)",
            scale=1,
        )
    else:
        themer = gr.HTML(visible=False)  # Dummy component if themer not available

    # Main content
    with gr.Column(elem_classes="main-sections"):

        # Top section - Random theme
        with gr.Column(elem_classes="section"):
            gr.Markdown("### 🎲 Random Theme")

            random_btn = gr.Button("Apply Random Theme", variant="primary", size="lg")
            theme_status = gr.Textbox(
                label="Theme Status",
                placeholder="Click button to apply random theme",
                interactive=False,
            )

        # Demo components to show theming
        with gr.Column(elem_classes="section"):
            gr.Markdown("### 🎨 Live Theme Preview")

            with gr.Row():
                gr.Button("Primary Button", variant="primary")
                gr.Button("Secondary Button", variant="secondary")
                gr.Button("Stop Button", variant="stop")

            with gr.Row():
                gr.Textbox("Sample text input", label="Text Input")
                gr.Slider(0, 100, value=50, label="Slider")

            with gr.Row():
                gr.Dropdown(["Option 1", "Option 2", "Option 3"], label="Dropdown")
                gr.Radio(["Choice A", "Choice B"], label="Radio")

        # Middle section - CSS converter
        with gr.Column(elem_classes="section"):
            gr.Markdown(
                """### 🔄 AI-Powered CSS to Theme Converter
🤖 Convert CSS code or describe your style to generate JSON themes using AI models"""
            )
            with gr.Row():
                model_selector = gr.Dropdown(
                    label="AI Model",
                    choices=[
                        ("Qwen2.5-Coder-7B", "qwen"),
                        ("Meta-Llama-3.1-8B-Instruct", "llama"),
                    ],
                    value="qwen",
                    info="Choose AI model for theme generation",
                    scale=1,
                )
                token_input = gr.Textbox(
                    label="Nebius API Token (Optional)",
                    placeholder="Leave empty for HF Zero inference, or provide Nebius token for better performance",
                    type="password",
                    lines=1,
                    scale=2,
                )

            css_input = gr.Textbox(
                label="Describe your style or paste CSS code here",
                placeholder="Examples:\n• 'Dark purple theme with neon accents'\n• 'Corporate blue and white design'\n• CSS code:\n.my-theme {\n  --primary: #3b82f6;\n  --background: #f8fafc;\n}",
                lines=8,
                max_lines=15,
            )

            convert_btn = gr.Button("Generate JSON", variant="primary", size="lg")

            json_output = gr.Code(
                label="Generated Theme JSON", language="json", lines=20
            )

        # Bottom section - MCP Server info
        with gr.Column(elem_classes="section mcp-info"):
            gr.Markdown("### 🤖 MCP Server Integration")
            gr.Markdown(
                """
            This Space functions as both a **Demo** and **MCP Server** for AI agents.
            
            **Available MCP Tools:**
            
            1. **`setup_package`** - Install and verify gradio-themer package
            2. **`generate_theme`** - Create theme JSON configuration
            3. **`convert_css_to_theme`** - Convert CSS to standardized JSON format (uses HF LLM)
            4. **`generate_app_code`** - Generate complete Gradio app with theming
            
            **For AI Agents:**
            - Connect to this Space as an MCP server
            - Use tools to help users create themed Gradio applications
            - Automate theme generation and application setup
            
            **For Developers:**
            - Install: `pip install gradio-themer`
            - Use the component in your Gradio apps
            - Create custom themes with JSON configuration
            
            **MCP Endpoint:** `/gradio_api/mcp/sse`
            """
            )

    # Event handlers
    random_btn.click(
        fn=apply_random_theme,
        outputs=[themer, theme_status],
        show_api=False,  # Hide from API docs but keep UI functional
    )

    convert_btn.click(
        fn=convert_css_to_theme_json_ai,
        inputs=[css_input, token_input, model_selector],
        outputs=[json_output],
        show_api=False,  # Hide from API docs but keep UI functional
    )


# Launch the demo
if __name__ == "__main__":
    # Configure for Google Fonts support and MCP server (as per GRADIO_MCP_HF_SPACES_GUIDE.md)
    demo.launch(
        mcp_server=True,  # CRITICAL: Enable MCP server functionality
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        # Allow external resources like Google Fonts
        allowed_paths=["./"],
    )
