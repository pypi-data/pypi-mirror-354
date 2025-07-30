---
tags: [gradio-custom-component, SimpleTextbox, designer, drag and drop, custom designs]
title: gradio_gradiodesigner
short_description: gradio designer
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_gradiodesigner`
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  

gradio designer

## Installation

```bash
pip install gradio_gradiodesigner
```

## Usage

```python
import gradio as gr
from gradio_gradiodesigner import GradioDesigner
import json

def analyze_design(design_config):
    """Analyze the design configuration"""
    if not design_config or not isinstance(design_config, dict):
        return "No design configuration provided"
    
    components = design_config.get('components', [])
    
    # Count components by type
    component_types = {}
    for comp in components:
        comp_type = comp.get('type', 'Unknown')
        component_types[comp_type] = component_types.get(comp_type, 0) + 1
    
    # Calculate coverage area
    if components:
        positions = [(comp['position']['x'], comp['position']['y']) for comp in components]
        min_x, min_y = min(pos[0] for pos in positions), min(pos[1] for pos in positions)
        max_x, max_y = max(pos[0] for pos in positions), max(pos[1] for pos in positions)
        coverage = f"{max_x - min_x} x {max_y - min_y} pixels"
    else:
        coverage = "No components"
    
    analysis = f"""📊 **Design Analysis**

**Component Summary:**
• Total components: {len(components)}
• Component types: {dict(component_types)}
• Canvas coverage: {coverage}

**Component Details:**
"""
    
    for i, comp in enumerate(components, 1):
        analysis += f"\n{i}. **{comp['type']}** (`{comp['id']}`)"
        analysis += f"\n   - Position: ({comp['position']['x']}, {comp['position']['y']})"
        analysis += f"\n   - Size: {comp['size']['width']}×{comp['size']['height']}"
        if comp.get('props', {}).get('label'):
            analysis += f"\n   - Label: \"{comp['props']['label']}\""
    
    return analysis

def generate_gradio_code(design_config):
    """Generate complete Gradio code from design"""
    if not design_config or not isinstance(design_config, dict):
        return "# No design to generate code from"
    
    components = design_config.get('components', [])
    
    code = '''import gradio as gr

def process_input(*args):
    """Process the inputs from your app"""
    return "Hello from your generated app!"

with gr.Blocks(title="Generated Gradio App") as demo:
    gr.Markdown("# 🚀 Generated Gradio App")
    gr.Markdown("This app was generated from your visual design!")
    
'''
    
    # Sort components by position (top to bottom, left to right)
    sorted_components = sorted(components, key=lambda c: (c['position']['y'], c['position']['x']))
    
    component_vars = []
    
    for comp in sorted_components:
        comp_type = comp.get('type', 'Textbox')
        comp_id = comp.get('id', 'component')
        props = comp.get('props', {})
        
        # Build component declaration
        prop_parts = []
        for key, value in props.items():
            if key in ['label', 'placeholder', 'value'] and isinstance(value, str):
                prop_parts.append(f'{key}="{value}"')
            elif key in ['minimum', 'maximum', 'step', 'lines', 'max_length', 'precision'] and isinstance(value, (int, float)):
                prop_parts.append(f'{key}={value}')
            elif key == 'choices' and isinstance(value, list):
                prop_parts.append(f'{key}={value}')
            elif isinstance(value, bool):
                prop_parts.append(f'{key}={value}')
        
        prop_string = ", ".join(prop_parts) if prop_parts else ""
        
        code += f"    {comp_id} = gr.{comp_type}({prop_string})\n"
        component_vars.append(comp_id)
    
    # Add a simple interaction if there are components
    if component_vars:
        inputs = [var for var in component_vars if not var.startswith('button')]
        outputs = [var for var in component_vars if var.startswith('button')]
        
        if not outputs:
            outputs = inputs[:1]  # Use first input as output if no buttons
        
        if inputs and outputs:
            code += f"\n    # Add interactions\n"
            code += f"    # Example: connect inputs to outputs\n"
            code += f"    # {outputs[0]}.click(process_input, inputs=[{', '.join(inputs)}], outputs=[{outputs[0]}])\n"
    
    code += '''
if __name__ == "__main__":
    demo.launch()
'''
    
    return code

with gr.Blocks(title="Gradio Visual Designer Pro", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎨 Gradio Visual Designer Pro
    
    **Build your Gradio apps visually!** Drag and drop components, customize properties, and generate production-ready code.
    
    **Features:** 25+ Gradio components • Real-time editing • Code generation • Export options
    """)
    
    with gr.Row():
        designer = GradioDesigner(
            label="Visual App Designer",
            value={"components": [], "layout": "blocks"}
        )
    
    with gr.Row():
        with gr.Column(scale=1):
            analysis_output = gr.Markdown(
                value="Design analysis will appear here...",
                label="Design Analysis"
            )
        
        with gr.Column(scale=1):
            code_output = gr.Code(
                label="Generated Gradio Code",
                language="python",
                value="# Design your app above to see generated code",
                lines=20
            )
    
    with gr.Row():
        analyze_btn = gr.Button("📊 Analyze Design", variant="secondary")
        generate_btn = gr.Button("🚀 Generate Code", variant="primary")
        clear_btn = gr.Button("🗑️ Clear All", variant="stop")
    
    # Event handlers
    designer.change(
        fn=analyze_design,
        inputs=[designer], 
        outputs=[analysis_output]
    )
    
    analyze_btn.click(
        fn=analyze_design,
        inputs=[designer],
        outputs=[analysis_output]
    )
    
    generate_btn.click(
        fn=generate_gradio_code,
        inputs=[designer],
        outputs=[code_output]
    )
    
    clear_btn.click(
        fn=lambda: {"components": [], "layout": "blocks"},
        outputs=[designer]
    )

if __name__ == "__main__":
    demo.launch()

```

## `GradioDesigner`

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
dict | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `change` | Triggered when the value of the GradioDesigner changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |
| `input` | This listener is triggered when the user changes the value of the GradioDesigner. |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.



 ```python
 def predict(
     value: dict | None
 ) -> dict | None:
     return value
 ```
 
