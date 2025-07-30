
import gradio as gr
from app import demo as app
import os

_docs = {'WorkflowBuilder': {'description': 'Professional Workflow Builder component with support for 25+ node types\ninspired by n8n and Langflow for AI agent development and MCP integration.', 'members': {'__init__': {'value': {'type': 'typing.Optional[typing.Dict[str, typing.Any]][\n    typing.Dict[str, typing.Any][str, typing.Any], None\n]', 'default': 'None', 'description': 'Default workflow data with nodes and edges'}, 'label': {'type': 'typing.Optional[str][str, None]', 'default': 'None', 'description': 'Component label'}, 'info': {'type': 'typing.Optional[str][str, None]', 'default': 'None', 'description': 'Additional component information'}, 'show_label': {'type': 'typing.Optional[bool][bool, None]', 'default': 'None', 'description': 'Whether to show the label'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'Whether to use container styling'}, 'scale': {'type': 'typing.Optional[int][int, None]', 'default': 'None', 'description': 'Relative width scale'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'Minimum width in pixels'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'Whether component is visible'}, 'elem_id': {'type': 'typing.Optional[str][str, None]', 'default': 'None', 'description': 'HTML element ID'}, 'elem_classes': {'type': 'typing.Optional[typing.List[str]][\n    typing.List[str][str], None\n]', 'default': 'None', 'description': 'CSS classes'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'Whether to render immediately'}}, 'postprocess': {'value': {'type': 'typing.Dict[str, typing.Any][str, typing.Any]', 'description': None}}, 'preprocess': {'return': {'type': 'typing.Dict[str, typing.Any][str, typing.Any]', 'description': None}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the WorkflowBuilder changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the WorkflowBuilder.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'WorkflowBuilder': []}}}

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
# `gradio_workflowbuilder`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

workflow builder
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_workflowbuilder
```

## Usage

```python
import gradio as gr
from gradio_workflowbuilder import WorkflowBuilder
import json


def export_workflow(workflow_data):
    \"\"\"Export workflow as formatted JSON\"\"\"
    if not workflow_data:
        return "No workflow to export"
    return json.dumps(workflow_data, indent=2)


# Create the main interface
with gr.Blocks(
    title="🎨 Visual Workflow Builder", 
    theme=gr.themes.Soft(),
    css=\"\"\"
    .main-container { max-width: 1600px; margin: 0 auto; }
    .workflow-section { margin-bottom: 2rem; }
    .button-row { display: flex; gap: 1rem; justify-content: center; margin: 1rem 0; }
    
    .component-description {
        padding: 24px;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        margin: 16px 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    .component-description p {
        margin: 10px 0;
        line-height: 1.6;
        color: #374151;
    }

    .base-description {
        font-size: 17px;
        font-weight: 600;
        color: #1e293b;
    }

    .base-description strong {
        color: #3b82f6;
        font-weight: 700;
    }

    .feature-description {
        font-size: 16px;
        color: #1e293b;
        font-weight: 500;
    }

    .customization-note {
        font-size: 15px;
        color: #64748b;
        font-style: italic;
    }

    .sample-intro {
        font-size: 15px;
        color: #1e293b;
        font-weight: 600;
        margin-top: 16px;
        border-top: 1px solid #e2e8f0;
        padding-top: 16px;
    }
    \"\"\"
) as demo:
    
    with gr.Column(elem_classes=["main-container"]):
        gr.Markdown(\"\"\"
        # 🎨 Visual Workflow Builder
        
        **Create sophisticated workflows with drag and drop simplicity.**
        \"\"\")
        
        # Simple description section with styling
        gr.HTML(\"\"\"
        <div class="component-description">
            <p class="base-description">Base custom component powered by <strong>svelteflow</strong>.</p>
            <p class="feature-description">Create custom workflows.</p>
            <p class="customization-note">You can customise the nodes as well as the design of the workflow.</p>
            <p class="sample-intro">Here is a sample:</p>
        </div>
        \"\"\")
        
        # Main workflow builder section
        with gr.Column(elem_classes=["workflow-section"]):
            workflow_builder = WorkflowBuilder(
                label="🎨 Visual Workflow Designer",
                info="Drag components from the sidebar → Connect nodes by dragging from output (right) to input (left) → Click nodes to edit properties"
            )
        
        # Export section below the workflow
        gr.Markdown("## 💾 Export Workflow")
        
        with gr.Row():
            with gr.Column():
                export_output = gr.Code(
                    language="json", 
                    label="Workflow Configuration",
                    lines=10
                )
        
        # Action button
        with gr.Row(elem_classes=["button-row"]):
            export_btn = gr.Button("💾 Export JSON", variant="primary", size="lg")
        
        # Instructions
        with gr.Accordion("📖 How to Use", open=False):
            gr.Markdown(\"\"\"
            ### 🚀 Getting Started
            
            1. **Add Components**: Drag items from the left sidebar onto the canvas
            2. **Connect Nodes**: Drag from the blue circle on the right of a node to the left circle of another
            3. **Edit Properties**: Click any node to see its editable properties on the right panel
            4. **Organize**: Drag nodes around to create a clean workflow layout
            5. **Delete**: Use the ✕ button on nodes or click the red circle on connections
            
            ### 🎯 Component Types
            
            - **📥 Inputs**: Text fields, file uploads, number inputs
            - **⚙️ Processing**: Language models, text processors, conditionals
            - **📤 Outputs**: Text displays, file exports, charts
            - **🔧 Tools**: API calls, data transformers, validators
            
            ### 💡 Pro Tips
            
            - **Collapsible Panels**: Use the arrow buttons to hide/show sidebars
            - **Live Updates**: Properties update in real-time as you edit
            - **Export Options**: Get JSON config for your workflow
            \"\"\")
    
    # Event handlers
    export_btn.click(
        fn=export_workflow,
        inputs=[workflow_builder],
        outputs=[export_output]
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        show_error=True
    )

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `WorkflowBuilder`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["WorkflowBuilder"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["WorkflowBuilder"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.



 ```python
def predict(
    value: typing.Dict[str, typing.Any][str, typing.Any]
) -> typing.Dict[str, typing.Any][str, typing.Any]:
    return value
```
""", elem_classes=["md-custom", "WorkflowBuilder-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          WorkflowBuilder: [], };
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
