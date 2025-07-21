import gradio as gr
from generate_questions import generate

def run(subject, year, count):
    return generate(subject, year, int(count))

gr.Interface(
    fn=run,
    inputs=[
        gr.Dropdown(["GS1", "GS2", "GS3", "GS4", "Essay"], label="Paper"),
        gr.Dropdown(choices=["2024"], label="Year"), 
        gr.Slider(1, 10, step=1, label="Number of Questions")
    ],
    outputs="text",
    title="UPSC Question Paper Generator AI"
).launch()