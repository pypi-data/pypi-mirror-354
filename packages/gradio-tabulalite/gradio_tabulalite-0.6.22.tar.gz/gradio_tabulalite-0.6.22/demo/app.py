
import gradio as gr
from gradio_tabulalite import TabulaLite
import pandas as pd

df = pd.read_csv("demo/large_data.csv")

with gr.Blocks() as demo:
    gr.Markdown("## Paginated Table Demo")
    table = TabulaLite(value=df.to_dict(orient="records"), rows_per_page=5)

if __name__ == "__main__":
    demo.launch()
