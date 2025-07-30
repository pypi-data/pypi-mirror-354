import pytest
import gradio as gr
from gradio_themer import GradioThemer


class TestGradioThemer:
    """Test suite for Gradio Themer component"""

    def test_component_initialization(self):
        """Test that component initializes correctly"""
        component = GradioThemer()
        assert component is not None
        assert hasattr(component, "EVENTS")

    def test_component_with_label(self):
        """Test component initialization with custom label"""
        label = "Custom Theme Selector"
        component = GradioThemer(label=label)
        assert component.label == label

    def test_component_with_initial_value(self):
        """Test component initialization with initial theme value"""
        initial_value = {"currentTheme": "dark", "type": "builtin"}
        component = GradioThemer(value=initial_value)
        assert component.value == initial_value

    def test_component_in_gradio_blocks(self):
        """Test that component works within Gradio Blocks"""

        def handle_theme_change(data):
            return f"Theme changed to: {data.get('currentTheme', 'unknown')}"

        with gr.Blocks() as demo:
            themer = GradioThemer(label="Theme Selector")
            output = gr.Textbox(label="Status")

            themer.change(fn=handle_theme_change, inputs=[themer], outputs=[output])

        assert demo is not None
        assert themer in demo.blocks

    def test_component_event_handling(self):
        """Test that component properly handles events"""

        def mock_handler(data):
            return data

        component = GradioThemer()
        # Test that change event can be attached
        component.change(fn=mock_handler, inputs=[component])

    def test_component_with_custom_theme_data(self):
        """Test component with custom theme configuration"""
        custom_theme_data = {
            "currentTheme": "custom",
            "type": "custom",
            "colors": {
                "primary": "#3b82f6",
                "secondary": "#64748b",
                "accent": "#f97316",
            },
            "css": "[data-theme='custom'] { --color-primary: #3b82f6; }",
        }

        component = GradioThemer(value=custom_theme_data)
        assert component.value == custom_theme_data

    def test_theme_validation(self):
        """Test that valid theme names are accepted"""
        valid_themes = [
            "light",
            "dark",
            "cupcake",
            "bumblebee",
            "emerald",
            "corporate",
            "synthwave",
            "retro",
            "cyberpunk",
        ]

        for theme in valid_themes:
            theme_data = {"currentTheme": theme, "type": "builtin"}
            component = GradioThemer(value=theme_data)
            assert component.value["currentTheme"] == theme


class TestGradioThemerIntegration:
    """Integration tests for Gradio Themer component in real Gradio apps"""

    def test_demo_app_creation(self):
        """Test that the demo app can be created successfully"""

        def handle_theme_change(data):
            if data:
                return f"Theme updated: {data.get('currentTheme', 'unknown')}"
            return "No theme data received"

        with gr.Blocks(title="Gradio Themer Test") as demo:
            gr.Markdown("# Gradio Theme Test")

            themer = GradioThemer(
                label="Theme Selector",
                value={"currentTheme": "light", "type": "builtin"},
            )

            status = gr.Textbox(label="Status", value="Ready")

            themer.change(fn=handle_theme_change, inputs=[themer], outputs=[status])

        assert demo is not None

    def test_multiple_themers_in_app(self):
        """Test multiple theme components in one app"""
        with gr.Blocks() as demo:
            with gr.Row():
                themer1 = GradioThemer(label="Primary Themer")
                themer2 = GradioThemer(label="Secondary Themer")

        assert (
            len([b for b in demo.blocks.values() if isinstance(b, GradioThemer)]) == 2
        )

    def test_themer_with_other_components(self):
        """Test themer working alongside other Gradio components"""
        with gr.Blocks() as demo:
            themer = GradioThemer(label="App Theme")
            textbox = gr.Textbox(label="Sample Input")
            button = gr.Button("Sample Button")
            dropdown = gr.Dropdown(choices=["A", "B", "C"], label="Sample Dropdown")

        assert all(
            component in demo.blocks.values()
            for component in [themer, textbox, button, dropdown]
        )


class TestGradioThemerErrorHandling:
    """Test error handling and edge cases"""

    def test_invalid_theme_data(self):
        """Test component handles invalid theme data gracefully"""
        invalid_data = {"invalidKey": "invalidValue"}
        component = GradioThemer(value=invalid_data)
        # Component should still initialize without crashing
        assert component is not None

    def test_none_value(self):
        """Test component handles None value"""
        component = GradioThemer(value=None)
        assert component is not None

    def test_empty_value(self):
        """Test component handles empty value"""
        component = GradioThemer(value={})
        assert component is not None


if __name__ == "__main__":
    # Run basic smoke tests
    print("Running Gradio Themer component tests...")

    # Test 1: Basic initialization
    try:
        component = GradioThemer()
        print("✅ Component initialization: PASSED")
    except Exception as e:
        print(f"❌ Component initialization: FAILED - {e}")

    # Test 2: Gradio integration
    try:
        with gr.Blocks() as demo:
            themer = GradioThemer(label="Test Themer")
        print("✅ Gradio integration: PASSED")
    except Exception as e:
        print(f"❌ Gradio integration: FAILED - {e}")

    # Test 3: Value handling
    try:
        test_value = {"currentTheme": "dark", "type": "builtin"}
        component = GradioThemer(value=test_value)
        # Check that the component correctly handles the currentTheme value
        assert component.value["currentTheme"] == "dark"
        assert component.value["type"] == "builtin"
        assert "themeInput" in component.value  # Should have default structure
        print("✅ Value handling: PASSED")
    except Exception as e:
        print(f"❌ Value handling: FAILED - {e}")

    print("\n🎉 Basic smoke tests completed!")
    print("\nTo run full test suite, use: pytest tests/test_component.py")
