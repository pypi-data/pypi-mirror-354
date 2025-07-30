---
tags: [gradio-custom-component, SimpleTextbox, gradio-spreadsheet-custom-component]
title: gradio_spreadsheetcomponent
short_description: This component is used to answer questions about spreadsheets.
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_spreadsheetcomponent`
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  

This component is used to answer questions about spreadsheets.

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

## `SpreadsheetComponent`

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
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
pandas.core.frame.DataFrame | list | dict | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Default value to show in spreadsheet. Can be a pandas DataFrame, list of lists, or dictionary</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `change` | Triggered when the value of the SpreadsheetComponent changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |
| `input` | This listener is triggered when the user changes the value of the SpreadsheetComponent. |
| `select` | Event listener for when the user selects or deselects the SpreadsheetComponent. Uses event data gradio.SelectData to carry `value` referring to the label of the SpreadsheetComponent, and `selected` to refer to state of the SpreadsheetComponent. See EventData documentation on how to use this event data |
| `upload` | This listener is triggered when the user uploads a file into the SpreadsheetComponent. |
| `download` | This listener is triggered when the user downloads a file from the SpreadsheetComponent. Uses event data gradio.DownloadData to carry information about the downloaded file as a FileData object. See EventData documentation on how to use this event data |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, the preprocessed input data sent to the user's function in the backend.


 ```python
 def predict(
     value: typing.Any
 ) -> Unknown:
     return value
 ```
 
