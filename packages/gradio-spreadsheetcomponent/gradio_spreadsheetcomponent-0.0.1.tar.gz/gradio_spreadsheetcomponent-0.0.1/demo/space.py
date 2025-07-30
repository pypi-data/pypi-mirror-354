
import gradio as gr
from app import demo as app
import os

_docs = {'SpreadsheetComponent': {'description': 'Creates a spreadsheet component that can display and edit tabular data with question answering capabilities.', 'members': {'__init__': {'value': {'type': 'pandas.core.frame.DataFrame | list | dict | None', 'default': 'None', 'description': 'Default value to show in spreadsheet. Can be a pandas DataFrame, list of lists, or dictionary'}}, 'postprocess': {}, 'preprocess': {'return': {'type': 'typing.Any', 'description': "The preprocessed input data sent to the user's function in the backend."}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the SpreadsheetComponent changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the SpreadsheetComponent.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the SpreadsheetComponent. Uses event data gradio.SelectData to carry `value` referring to the label of the SpreadsheetComponent, and `selected` to refer to state of the SpreadsheetComponent. See EventData documentation on how to use this event data'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the SpreadsheetComponent.'}, 'download': {'type': None, 'default': None, 'description': 'This listener is triggered when the user downloads a file from the SpreadsheetComponent. Uses event data gradio.DownloadData to carry information about the downloaded file as a FileData object. See EventData documentation on how to use this event data'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'SpreadsheetComponent': []}}}

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
# `gradio_spreadsheetcomponent`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

This component is used to answer questions about spreadsheets.
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_spreadsheetcomponent
```

## Usage

```python
import gradio as gr
from gradio_spreadsheetcomponent import SpreadsheetComponent
from dotenv import load_dotenv
import os
import pandas as pd

def answer_question(file, question):
    if not file or not question:
        return "Please upload a file and enter a question."
    
    # Load the spreadsheet data
    df = pd.read_excel(file.name)
    
    # Create a SpreadsheetComponent instance
    spreadsheet = SpreadsheetComponent(value=df)
    
    # Use the component to answer the question
    return spreadsheet.answer_question(question)

with gr.Blocks() as demo:
    gr.Markdown("# Spreadsheet Question Answering")
    
    with gr.Row():
        file_input = gr.File(label="Upload Spreadsheet", file_types=[".xlsx"])
        question_input = gr.Textbox(label="Ask a Question")
    
    answer_output = gr.Textbox(label="Answer", interactive=False, lines=4)
    
    submit_button = gr.Button("Submit")
    submit_button.click(answer_question, inputs=[file_input, question_input], outputs=answer_output)

    
if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `SpreadsheetComponent`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["SpreadsheetComponent"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["SpreadsheetComponent"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, the preprocessed input data sent to the user's function in the backend.


 ```python
def predict(
    value: typing.Any
) -> Unknown:
    return value
```
""", elem_classes=["md-custom", "SpreadsheetComponent-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          SpreadsheetComponent: [], };
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
