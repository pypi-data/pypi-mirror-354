"""
Gradio Themer - MCP Server Entry Point
Clean entry point that exposes only the 4 intended MCP tools.
"""

import os
import gradio as gr

# CRITICAL: Enable MCP server mode (as per GRADIO_MCP_HF_SPACES_GUIDE.md)
os.environ["GRADIO_MCP_SERVER"] = "True"

# Import the 4 MCP tools - these will be exposed by the MCP server
from mcp_tools import (
    setup_package,
    generate_theme,
    convert_css_to_theme,
    generate_app_code,
)

if __name__ == "__main__":
    try:
        import page

        # Add hidden MCP endpoints to the existing demo
        with page.demo:
            # Add hidden MCP tool endpoints (invisible to users, visible to MCP)

            # Hidden setup_package endpoint
            setup_btn = gr.Button("Setup Package", visible=False)
            setup_output = gr.JSON(visible=False)
            setup_btn.click(
                fn=setup_package, outputs=setup_output, api_name="setup_package"
            )

            # Hidden generate_theme endpoint
            theme_name_input = gr.Textbox(visible=False)
            primary_color_input = gr.Textbox(visible=False, value="#3b82f6")
            theme_style_input = gr.Textbox(visible=False, value="light")
            accent_color_input = gr.Textbox(visible=False, value="")
            generate_theme_btn = gr.Button("Generate Theme", visible=False)
            generate_theme_output = gr.JSON(visible=False)
            generate_theme_btn.click(
                fn=generate_theme,
                inputs=[
                    theme_name_input,
                    primary_color_input,
                    theme_style_input,
                    accent_color_input,
                ],
                outputs=generate_theme_output,
                api_name="generate_theme",
            )

            # Hidden convert_css_to_theme endpoint
            css_input = gr.Textbox(visible=False)
            convert_theme_name_input = gr.Textbox(
                visible=False, value="converted_theme"
            )
            user_token_input = gr.Textbox(visible=False, value="")
            model_choice_input = gr.Textbox(visible=False, value="qwen")
            convert_css_btn = gr.Button("Convert CSS", visible=False)
            convert_css_output = gr.Textbox(visible=False)
            convert_css_btn.click(
                fn=convert_css_to_theme,
                inputs=[
                    css_input,
                    convert_theme_name_input,
                    user_token_input,
                    model_choice_input,
                ],
                outputs=convert_css_output,
                api_name="convert_css_to_theme",
            )

            # Hidden generate_app_code endpoint
            app_theme_names_input = gr.Textbox(
                visible=False, value="ocean_breeze,sunset_orange"
            )
            app_title_input = gr.Textbox(visible=False, value="My Themed App")
            include_components_input = gr.Textbox(
                visible=False, value="button,textbox,slider"
            )
            generate_app_btn = gr.Button("Generate App", visible=False)
            generate_app_output = gr.Textbox(visible=False)
            generate_app_btn.click(
                fn=generate_app_code,
                inputs=[
                    app_theme_names_input,
                    app_title_input,
                    include_components_input,
                ],
                outputs=generate_app_output,
                api_name="generate_app_code",
            )

        # Launch the demo with MCP server enabled
        page.demo.launch(
            mcp_server=True,  # CRITICAL: Enable MCP server functionality
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            debug=True,
            allowed_paths=["./"],
        )

    except ImportError as e:
        print(f"❌ Error importing demo interface: {e}")
        print("Make sure page.py exists and contains the 'demo' variable")
        exit(1)
    except AttributeError as e:
        print(f"❌ Error accessing demo object: {e}")
        print("Make sure page.py contains a 'demo' variable")
        exit(1)
