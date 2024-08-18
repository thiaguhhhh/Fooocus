import gradio as gr
import random
import os
import json
import time
import shared
import modules.config
import fooocus_version
import modules.html
import modules.async_worker as worker
import modules.constants as constants
import modules.flags as flags
import modules.gradio_hijack as grh
import modules.style_sorter as style_sorter
import modules.meta_parser
import args_manager
import copy
import launch
from extras.inpaint_mask import SAMOptions

from modules.sdxl_styles import legal_style_names
from modules.private_logger import get_current_html_path
from modules.ui_gradio_extensions import reload_javascript
from modules.auth import auth_enabled, check_auth
from modules.util import is_json
from tkinter import Tk, filedialog


def process_directories(directory_paths):
    if not directory_paths:
        return "No directories selected."

    results = []
    for directory in directory_paths:
        # List files in the directory
        files = os.listdir(directory)
        results.append(f"Contents of {directory}:\n" + "\n".join(files))

    return "\n\n".join(results)


def update_visibility(x):
    # Add more updates for other components
    return [gr.update(visible=x), gr.update(visible=x)]


def list_to_string(filenames):
    # Join the filenames list into a comma-separated string
    file_list = ', '.join(filenames)
    return file_list


def on_browse(data_type):
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    if data_type == "Files":
        filenames = filedialog.askopenfilenames()
        if len(filenames) > 0:
            root.destroy()
            file_list = list_to_string(filenames)
            return file_list
        else:
            filename = "Files not seleceted"
            root.destroy()
            return None

    elif data_type == "Folder":
        filename = filedialog.askdirectory()
        if filename:
            if os.path.isdir(filename):
                root.destroy()
                return str(filename)
            else:
                root.destroy()
                return str(filename)
        else:
            filename = "Folder not seleceted"
            root.destroy()
            return None


def on_file_change(files, data_type):
    if files and data_type == "Files":
        return gr.update(visible=True), gr.update(), gr.update(value=True)

    # If no files are selected, hide file explorer and clear input_path
    if not files and data_type == "Files":
        return gr.update(visible=False), gr.update(value=""), gr.update(value=False)

    if data_type == "Folder":
        return gr.update(visible=False), gr.update(), gr.update(value=True)

    return gr.update(visible=False), gr.update(), gr.update(value=False)


def on_input_change(input_path, file_explorer):
    if os.path.isdir(input_path):
        # Return an empty list if input_path is a directory or empty
        return None, gr.update(visible=True), gr.update(value=True)

    if not input_path:
        # Return an empty list if input_path is a directory or empty
        return None, gr.update(visible=False), gr.update(value=False)

    # Initialize a dictionary to track unique file names and their paths
    unique_file_paths = {}

    # Process the input_path string
    if input_path:
        # Clean up the input path string and split it into a list of file paths
        file_paths_list = input_path.strip("()").replace("'", "").split(", ")
        # Extract file names and ensure uniqueness
        for path in file_paths_list:
            file_name = os.path.basename(path)
            unique_file_paths[file_name] = path

    # Process file_explorer items if provided
    if file_explorer:
        # Extract 'orig_name' from each file_explorer object and ensure uniqueness
        for item in file_explorer:
            file_name = os.path.basename(item.orig_name)
            # Store the path, replacing any existing path with the same file name
            unique_file_paths[file_name] = item.orig_name

    # Convert the dictionary values back to a list of unique file paths
    if len(unique_file_paths.values()) > 0:
        return list(unique_file_paths.values()), gr.update(visible=False), gr.update(value=True)
    else:
        return None, gr.update(visible=False), gr.update(value=False)


def on_click_clear():
    return None, None, gr.update(visible=False), gr.update(visible=False)

# Function to set prompts based on the selected type


def update_prompts(selected_type):
    # Ensure selected_type is a valid key and exists in the dictionary
    if selected_type in modules.config.default_enhance_prompts:
        positive_prompt = modules.config.default_enhance_prompts[selected_type]['positive']
        negative_prompt = modules.config.default_enhance_prompts[selected_type]['negative']
        return positive_prompt, negative_prompt
    else:
        # Returning default or empty values
        return "Default positive prompt", "Default negative prompt"


def on_selection_change(selected_type):
    # Get prompts based on selected_type
    positive_prompt, negative_prompt = update_prompts(selected_type[0])

    # Return the prompts
    return positive_prompt, negative_prompt
