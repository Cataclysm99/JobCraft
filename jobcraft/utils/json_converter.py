"""
JSON conversion utilities for resume and cover letter data.
"""

import json
from typing import Dict, Any
from pathlib import Path


class JSONConverter:
    """Convert Python dictionaries to/from JSON format."""
    
    @staticmethod
    def dict_to_json(data: Dict[str, Any], output_path: str = None, pretty: bool = True) -> str:
        """
        Convert dictionary to JSON string or file.
        
        Args:
            data: Dictionary to convert
            output_path: Optional path to save JSON file
            pretty: Whether to pretty-print the JSON
            
        Returns:
            JSON string
        """
        if pretty:
            json_str = json.dumps(data, indent=2, ensure_ascii=False)
        else:
            json_str = json.dumps(data, ensure_ascii=False)
        
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str
    
    @staticmethod
    def json_to_dict(json_input: str) -> Dict[str, Any]:
        """
        Convert JSON string or file to dictionary.
        
        Args:
            json_input: JSON string or path to JSON file
            
        Returns:
            Dictionary
        """
        # Check if input is a file path
        if Path(json_input).exists():
            with open(json_input, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Assume it's a JSON string
            return json.loads(json_input)
