
import gradio as gr
from app import demo as app
import os

_docs = {'TabulaLite': {'description': 'A base class for defining methods that all input/output components should have.', 'members': {'__init__': {}, 'postprocess': {}, 'preprocess': {}}, 'events': {}}, '__meta__': {'additional_interfaces': {}}}

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
# `gradio_tabulalite`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.6.22%20-%20orange">  
</div>

a lightweight, feature-rich Gradio custom component for displaying interactive data tables with built-in sorting, pagination, search, row selection, and CSV export — all wrapped in a beautiful light-orange theme
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_tabulalite
```

## Usage

```python

import gradio as gr
from gradio_tabulalite import TabulaLite
import pandas as pd

df = pd.read_csv("demo/large_data.csv")

with gr.Blocks() as demo:
    gr.Markdown("## Paginated Table Demo")
    table = TabulaLite(value=df.to_dict(orient="records"), rows_per_page=5)

if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `TabulaLite`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["TabulaLite"]["members"]["__init__"], linkify=[])







    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {};
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
