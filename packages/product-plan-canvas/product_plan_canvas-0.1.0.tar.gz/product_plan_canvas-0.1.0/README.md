
# `product_plan_canvas`
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.1.0%20-%20orange">  

A custom Gradio component for product planning with a 4-column drag-and-drop board

## Installation

```bash
pip install product_plan_canvas
```

## Usage

```python
import gradio as gr
from product_plan_canvas import ProductPlanCanvas

def main():
    initial_data = [
        {"id": 0, "content": "Sample idea 1", "column": "idea"},
        {"id": 1, "content": "Sample feature 1", "column": "features"},
        {"id": 2, "content": "Sample timeline 1", "column": "timeline"},
        {"id": 3, "content": "Sample story 1", "column": "stories"}
    ]
    with gr.Blocks() as demo:
        gr.Markdown("# Product Plan Canvas Demo")
        canvas = ProductPlanCanvas(
            value=initial_data,
            label="Product Planning Board",
            show_label=True,
            interactive=True
        )
        state_display = gr.JSON(label="Current State")
        canvas.state.change(
            fn=lambda x: x,
            inputs=[canvas.state],
            outputs=[state_display]
        )
    demo.launch()

if __name__ == "__main__":
    main() 
```

## `ProductPlanCanvas`

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
typing.Optional[typing.List[typing.Dict[str, typing.Any]]][
    typing.List[typing.Dict[str, typing.Any]][
        typing.Dict[str, typing.Any][str, typing.Any]
    ],
    None,
]
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Initial state of the board</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
typing.Optional[str][str, None]
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Label for the component</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">Whether to show the label</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">Whether the component is interactive</td>
</tr>
</tbody></table>




