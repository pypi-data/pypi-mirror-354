
# `gradio_themer`
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.1.0%20-%20orange">  

User-configurable themes for Gradio applications - unlimited custom themes via JSON configuration

## Installation

```bash
pip install gradio_themer
```

## Usage

```python
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

```

## `GradioThemer`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
typing.Union[
    typing.Dict[str, typing.Any], typing.Callable, NoneType
][
    typing.Dict[str, typing.Any][str, typing.Any],
    Callable,
    None,
]
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Default theme configuration. Should be a dict with 'themeInput', 'themeConfig', and 'generatedCSS' keys.</td>
</tr>

<tr>
<td align="left"><code>theme_config_path</code></td>
<td align="left" style="width: 25%;">

```python
typing.Optional[str][str, None]
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Path to user themes configuration file (JSON). If None, searches for common filenames.</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The label for this component, displayed above the component if `show_label` is `True`.</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Continously calls `value` to recalculate it if `value` is a function.</td>
</tr>

<tr>
<td align="left"><code>inputs</code></td>
<td align="left" style="width: 25%;">

```python
typing.Union[
    gradio.components.base.FormComponent,
    typing.Sequence[gradio.components.base.FormComponent],
    set[gradio.components.base.FormComponent],
    NoneType,
][
    gradio.components.base.FormComponent,
    typing.Sequence[gradio.components.base.FormComponent][
        gradio.components.base.FormComponent
    ],
    set[gradio.components.base.FormComponent],
    None,
]
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Components that are used as inputs to calculate `value` if `value` is a function.</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If True, will display label.</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Relative size compared to adjacent Components.</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>160</code></td>
<td align="left">Minimum pixel width.</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If True, will be rendered as an editable component.</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will be hidden.</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string that is assigned as the id of this component in the HTML DOM.</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional list of strings that are assigned as the classes of this component in the HTML DOM.</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will not render be rendered in the Blocks context.</td>
</tr>

<tr>
<td align="left"><code>key</code></td>
<td align="left" style="width: 25%;">

```python
int | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">A unique key for this component.</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `change` | Triggered when the value of the GradioThemer changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |
| `input` | This listener is triggered when the user changes the value of the GradioThemer. |
| `submit` | This listener is triggered when the user presses the Enter key while the GradioThemer is focused. |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, passes the theme configuration as a dict into the function.
- **As input:** Should return, expects a dict with theme configuration data.

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
 
