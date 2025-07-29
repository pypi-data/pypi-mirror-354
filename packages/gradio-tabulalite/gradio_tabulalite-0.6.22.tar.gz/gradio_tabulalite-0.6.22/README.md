---
tags: [
    gradio-custom-component, 
    custom-component-track,
    gradio,
    gradio-component,
    gradio-ui,
    data-visualization,
    data-table,
    sortable,
    filterable,
    searchable,
    paginated,
    csv-export,
    row-selection,
    interactive-table,
    frontend,
    svelte,
    python,
    lightweight,
    ui-component,
    open-source,    
]
title: gradio_tabulalite
short_description: a lightweight Gradio custom component for displaying data tables with built-in sorting, pagination, search, row selection, and CSV export
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_tabulalite`
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.6.22%20-%20orange">  

a lightweight, feature-rich Gradio custom component for displaying interactive data tables with built-in sorting, pagination, search, row selection, and CSV export — all wrapped in a beautiful light-orange theme

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

## `TabulaLite`

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
<tbody></tbody></table>




