---
title: 🎨 Gradio Themer - Demo & MCP Server
emoji: 🎨
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.31.0
app_file: app.py
pinned: true
license: mit
short_description: User-configurable themes for Gradio applications with MCP server integration
models:
  - MasterControlAIML/DeepSeek-R1-Qwen2.5-1.5b-SFT-R1-JSON-Unstructured-To-Structured
tags:
  - mcp-server-track
  - custom-component-track
  - Agents-MCP-Hackathon
  - gradio
  - theming
  - agent-ui
---

# 🎨 Gradio Themer - Demo & MCP Server

**Dual Track Hackathon Submission**: Custom Component + MCP Server

## 🚀 Features

- **Dynamic Theme System**: User-configurable themes via JSON
- **AI-Powered Conversion**: Convert CSS/descriptions to theme JSON using HuggingFace models
- **MCP Server Integration**: 4 practical tools for theme development
- **Production Ready**: Built and tested package

## 🤖 MCP Tools (Production-Focused)

### 1. `generate_theme`

**Purpose**: Create complete theme JSON with intelligent color harmonies
**Parameters**:

- `theme_name`: Name of the theme
- `primary_color`: Main color (hex format, default: "#3b82f6")
- `theme_style`: "light" or "dark" (default: "light")
- `color_harmony`: "complementary", "triadic", "analogous", "monochromatic" (default: "complementary")

**Output**: Complete theme JSON with harmonious colors and accessibility considerations

### 2. `convert_css_to_theme`

**Purpose**: Convert existing CSS or natural language descriptions to theme JSON
**Parameters**:

- `css_input`: CSS code or style description
- `theme_name`: Name for the converted theme (default: "converted_theme")

**Output**: Theme JSON extracted from CSS using AI and pattern matching

### 3. `apply_theme_preview`

**Purpose**: Generate CSS code for immediate theme preview in any Gradio app
**Parameters**:

- `theme_json`: Theme JSON configuration

**Output**: Ready-to-use CSS code for instant theme application

### 4. `export_theme_package`

**Purpose**: Export complete theme package with JSON, CSS, and usage instructions
**Parameters**:

- `theme_json`: Theme JSON configuration
- `package_name`: Name for the package files (default: "my_theme")

**Output**: Complete package with files, documentation, and sample code

## 🎯 Why These Tools?

**❌ Removed**: Package management tools (not useful for theme development)
**✅ Added**: Practical workflow tools that developers actually need:

1. **Smart Theme Generation**: Uses color theory for harmonious palettes
2. **CSS Migration**: Convert existing designs to Gradio themes
3. **Instant Preview**: Get CSS for immediate testing
4. **Complete Export**: Ready-to-use packages with documentation

## 🔧 Usage Examples

### Generate Theme with Color Harmony

```python
# Create complementary color scheme from blue primary
generate_theme("Ocean Theme", "#0ea5e9", "light", "complementary")
```

### Convert Existing CSS

```python
# Convert CSS variables to theme JSON
convert_css_to_theme("""
:root {
  --primary: #3b82f6;
  --background: #ffffff;
  --text: #1e293b;
}
""", "Converted Blue Theme")
```

### Get Preview CSS

```python
# Generate CSS for immediate application
apply_theme_preview('{"ocean_theme": {"colors": {...}}}')
```

### Export Complete Package

```python
# Create ready-to-use theme package
export_theme_package('{"my_theme": {...}}', "awesome_theme")
```

## 🏆 Production Benefits

1. **Workflow Efficiency**: Tools cover the complete theme development cycle
2. **Color Theory**: Automatic generation of harmonious color schemes
3. **Accessibility**: Built-in contrast considerations
4. **Migration Support**: Easy conversion from existing CSS
5. **Instant Testing**: Preview CSS for immediate application
6. **Complete Packages**: Everything needed for distribution

## 🛠 Setup & Installation

### For Demo Usage:

```bash
pip install gradio>=5.31.0
python app.py
```

### For MCP Client (Claude Desktop, Cursor):

```json
{
  "mcpServers": {
    "gradio-themer": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "/path/to/gradio-themer/demo"
    }
  }
}
```

## 📋 Hackathon Submission

**Track 1 (MCP Server)**:

- Tag: `mcp-server-track`
- 4 production-focused MCP tools
- Complete theme development workflow

**Track 2 (Custom Component)**:

- Tag: `custom-component-track`
- Published package: `gradio_themer`
- Interactive Gradio component

## 🎨 Demo Features

- **Random Theme Button**: Apply any of 13+ available themes
- **CSS to JSON Converter**: AI-powered conversion using HuggingFace models
- **Theme Showcase**: Live preview of different theme styles
- **MCP Integration**: Embedded MCP server functionality

## 📦 Package Information

- **Package**: `gradio_themer-0.1.0`
- **Class**: `GradioThemer`
- **Import**: `from gradio_themer import GradioThemer`
- **Status**: Production ready

## 🔗 Links

- **GitHub**: [Repository URL]
- **HuggingFace Space**: [Space URL]
- **Package**: [PyPI URL when published]

---

**Built for HuggingFace Gradio Hackathon 2024**
