import requests
import json
from typing import Dict, Any
class Grocmock:
    def __init__(self, tool_config: Dict[str, Any]):
        """
        Initialize Grocmock connection with tool configuration.
        
        """
        self.tool_config = tool_config
       

    