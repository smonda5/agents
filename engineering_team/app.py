import gradio as gr
import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(ROOT, "src"))

# from src.engineering_team.main import run
from src.engineering_team.main import run

def run_homework(grade, to_email):
    return run(grade, to_email)

with gr.Blocks() as demo:
    gr.Markdown("# Homework Automation UI")

    grade = gr.Dropdown(
        choices=["One", "Two", "Three", "Four", "Five"],
        label="Select Grade"
    )

    to_email = gr.Textbox(
        label="Recipient Email",
        placeholder="name@example.com"
    )

    submit_btn = gr.Button("Run Homework Crew")
    output = gr.Textbox(label="Output")
    submit_btn.click(fn=run_homework, inputs=[grade, to_email], outputs=output)

demo.launch()
