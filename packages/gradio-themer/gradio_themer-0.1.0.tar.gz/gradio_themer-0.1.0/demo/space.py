
import gradio as gr
from app import demo as app
import os

_docs = {'GradioThemer': {'description': 'A custom Gradio component for applying user-configurable themes to Gradio applications.\n\nThis component allows users to:\n- Configure unlimited custom themes via JSON configuration files\n- Preview themes with live Gradio components\n- Switch between themes dynamically\n- Export CSS for use in other projects', 'members': {'__init__': {'value': {'type': 'typing.Union[\n    typing.Dict[str, typing.Any], typing.Callable, NoneType\n][\n    typing.Dict[str, typing.Any][str, typing.Any],\n    Callable,\n    None,\n]', 'default': 'None', 'description': "Default theme configuration. Should be a dict with 'themeInput', 'themeConfig', and 'generatedCSS' keys."}, 'theme_config_path': {'type': 'typing.Optional[str][str, None]', 'default': 'None', 'description': 'Path to user themes configuration file (JSON). If None, searches for common filenames.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component, displayed above the component if `show_label` is `True`.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': 'Continously calls `value` to recalculate it if `value` is a function.'}, 'inputs': {'type': 'typing.Union[\n    gradio.components.base.FormComponent,\n    typing.Sequence[gradio.components.base.FormComponent],\n    set[gradio.components.base.FormComponent],\n    NoneType,\n][\n    gradio.components.base.FormComponent,\n    typing.Sequence[gradio.components.base.FormComponent][\n        gradio.components.base.FormComponent\n    ],\n    set[gradio.components.base.FormComponent],\n    None,\n]', 'default': 'None', 'description': 'Components that are used as inputs to calculate `value` if `value` is a function.'}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will display label.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'Relative size compared to adjacent Components.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'Minimum pixel width.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will be rendered as an editable component.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context.'}, 'key': {'type': 'int | str | None', 'default': 'None', 'description': 'A unique key for this component.'}}, 'postprocess': {'value': {'type': 'typing.Optional[typing.Dict[str, typing.Any]][\n    typing.Dict[str, typing.Any][str, typing.Any], None\n]', 'description': 'Expects a dict with theme configuration data.'}}, 'preprocess': {'return': {'type': 'typing.Optional[typing.Dict[str, typing.Any]][\n    typing.Dict[str, typing.Any][str, typing.Any], None\n]', 'description': 'Passes the theme configuration as a dict into the function.'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the GradioThemer changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the GradioThemer.'}, 'submit': {'type': None, 'default': None, 'description': 'This listener is triggered when the user presses the Enter key while the GradioThemer is focused.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'GradioThemer': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_themer`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.1.0%20-%20orange">  
</div>

User-configurable themes for Gradio applications - unlimited custom themes via JSON configuration
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_themer
```

## Usage

```python
\"\"\"
Gradio Themer - MCP Server Entry Point
Clean entry point that exposes only the 4 intended MCP tools.
\"\"\"

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

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `GradioThemer`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["GradioThemer"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["GradioThemer"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes the theme configuration as a dict into the function.
- **As output:** Should return, expects a dict with theme configuration data.

 ```python
def predict(
    value: typing.Optional[typing.Dict[str, typing.Any]][
    typing.Dict[str, typing.Any][str, typing.Any], None
]
) -> typing.Optional[typing.Dict[str, typing.Any]][
    typing.Dict[str, typing.Any][str, typing.Any], None
]:
    return value
```
""", elem_classes=["md-custom", "GradioThemer-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          GradioThemer: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
