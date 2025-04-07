import os
import gradio as gr
import modules.async_worker as worker
from modules.util import load_file
from modules.config import cfg
from modules.default_values import default_prompt, default_negative_prompt

SAVE_PATH = "saved_character.txt"

def save_character(character_description):
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        f.write(character_description)
    return "✅ Character saved!"

def load_character():
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def start_processing(prompt, negative_prompt):
    return worker.run_task(prompt, negative_prompt)

with gr.Blocks(css="style.css") as ui:
    gr.Markdown("## 🖼️ Fooocus - Advanced UI")

    with gr.Row():
        with gr.Column():
            prompt = gr.Textbox(label="Prompt", value=default_prompt)
            negative_prompt = gr.Textbox(label="Negative Prompt", value=default_negative_prompt)

            generate_btn = gr.Button("Generate")
            output = gr.Image(label="Result")

        with gr.Column():
            with gr.Accordion("Advanced", open=False):
                character_input = gr.Textbox(label="Character Description", value=load_character())
                save_button = gr.Button("💾 Save Character")
                save_output = gr.Markdown()
                save_button.click(fn=save_character, inputs=character_input, outputs=save_output)

    generate_btn.click(fn=start_processing, inputs=[prompt, negative_prompt], outputs=output)

ui.launch(share=True)


