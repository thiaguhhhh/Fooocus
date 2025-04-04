import gradio as gr
saved_character = {}

def save_character_fn(image, prompt, seed):
    global saved_character
    saved_character = {
        "image": image,
        "prompt": prompt,
        "seed": seed
    }
    print("💾 Character saved:", saved_character)
    return "✅ Character saved!"

def generate_fn(prompt, seed, use_saved):
    if use_saved and saved_character:
        prompt = saved_character.get("prompt", prompt)
        seed = saved_character.get("seed", seed)
        print("⚡ Using saved character:", prompt, seed)

    return f"Generated image for: '{prompt}' with seed {seed}"  # Replace with actual Fooocus function

with gr.Blocks() as ui:
    prompt_input = gr.Textbox(label="Prompt", value="a futuristic warrior")
    seed_input = gr.Number(label="Seed", value=42)
    use_saved_checkbox = gr.Checkbox(label="Use Saved Character", value=False)
    
    generate_btn = gr.Button("Generate")
    image_output = gr.Textbox(label="Output Image Placeholder")

    with gr.Accordion("Advanced", open=False):
        save_character_btn = gr.Button("💾 Save Character")

    generate_btn.click(
        fn=generate_fn,
        inputs=[prompt_input, seed_input, use_saved_checkbox],
        outputs=[image_output]
    )

    save_character_btn.click(
        fn=save_character_fn,
        inputs=[image_output, prompt_input, seed_input],
        outputs=[]
    )
