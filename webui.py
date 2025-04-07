import gradio as gr
import os

SAVE_PATH = "saved_character.txt"

def save_character(character_description):
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        f.write(character_description)
    return f"✅ Character saved!"

def load_character():
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ""

with gr.Blocks() as demo:
    with gr.Accordion("Advanced", open=False):
        character_input = gr.Textbox(label="Character Description", value=load_character())
        save_button = gr.Button("Save Character")
        save_output = gr.Markdown()

        save_button.click(fn=save_character, inputs=character_input, outputs=save_output)

demo.launch(share=True)

