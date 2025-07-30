from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

import numpy as np
import os
import pandas as pd
import tempfile
from gradio.utils import FileData
from gradio.components.base import Component, FormComponent
from gradio.events import Events
from gradio.i18n import I18nData
from huggingface_hub import InferenceClient

if TYPE_CHECKING:
    from gradio.components import Timer

from gradio.events import Dependency

class SpreadsheetComponent(FormComponent):
    """
    Creates a spreadsheet component that can display and edit tabular data with question answering capabilities.
    """
    
    def __init__(
        self,
        value: pd.DataFrame | list | dict | None = None,
        **kwargs
    ):
        """
        Parameters:
            value: Default value to show in spreadsheet. Can be a pandas DataFrame, list of lists, or dictionary
            hf_token: Hugging Face API token for question answering functionality
        """
        # Initialize the default value first
        if isinstance(value, list):
            value = pd.DataFrame(value)
        elif isinstance(value, dict):
            value = pd.DataFrame.from_dict(value)
        elif not isinstance(value, pd.DataFrame):
            raise ValueError(f"Value must be DataFrame, list, dict or None. Got {type(value)}")

        
        super().__init__(
            value=value,
            **kwargs,
        )

        self.value = value
            
        # Initialize Hugging Face client if token provided

        self.hf_client = InferenceClient(provider="hf-inference", api_key=os.getenv("HF_TOKEN"))
        
    def answer_question(self, question: str) -> str:
        """Ask a question about the current spreadsheet data"""
        if self.hf_client is None:
            return "Error: Hugging Face API token not configured. Please provide a token through the hf_token parameter or HUGGINGFACE_API_TOKEN environment variable."
            
        try:
            if self.value.empty:
                return "Error: The spreadsheet is empty. Please add some data first."
                
            # Convert DataFrame to table format
            table = {col: [str(val) if pd.notna(val) else "" for val in self.value[col]] 
                    for col in self.value.columns}
            # Get answer using table question answering
            result = self.hf_client.table_question_answering(
                table=table,
                query=question,
                model="google/tapas-large-finetuned-wtq"
            )
            
            # Format the answer with more context
            parts = []
            parts.append(f"Answer: {result.answer}")
            
            if hasattr(result, 'cells') and result.cells:
                parts.append(f"Relevant cell values: {', '.join(result.cells)}")
                
            if hasattr(result, 'coordinates') and result.coordinates:
                parts.append("Location of relevant information:")
                for coords in result.coordinates:
                    row, col = coords
                    parts.append(f"- Row {row}, Column '{col}'")
                    
            return "\n".join(parts)
            
        except Exception as e:
            return f"Error processing question: {str(e)}\nPlease try rephrasing your question or verify the data format."
    
    def api_info(self) -> dict[str, Any]:
        """Define component's API information for documentation."""
        return {
            "name": "spreadsheet",
            "description": "A spreadsheet component for data manipulation with question answering capabilities",
            "inputs": [
                {
                    "name": "value",
                    "type": "DataFrame | list | dict | None",
                    "description": "Data to display in the spreadsheet",
                    "default": None,
                    "required": False
                },
                {
                    "name": "headers",
                    "type": "List[str]",
                    "description": "Column headers for the spreadsheet",
                    "default": None,
                    "required": False
                },
                {
                    "name": "row_count",
                    "type": "int",
                    "description": "Default number of rows if no value provided",
                    "default": 3,
                    "required": False
                },
                {
                    "name": "col_count",
                    "type": "int",
                    "description": "Default number of columns if no value provided",
                    "default": 3,
                    "required": False
                }
            ],
            "outputs": [
                {
                    "name": "value",
                    "type": "DataFrame",
                    "description": "The current state of the spreadsheet"
                }
            ],
            "dependencies": [
                {"name": "pandas", "type": "pip"},
                {"name": "openpyxl", "type": "pip"},
                {"name": "huggingface-hub", "type": "pip"}
            ]
        }
    from typing import Callable, Literal, Sequence, Any, TYPE_CHECKING
    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer
        from gradio.components.base import Component