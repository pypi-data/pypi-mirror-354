"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Dict, Any


class ConfigBase:
    """Base Configuration Class"""

    def __init__(self, enabled: bool = True):
        self.enabled: bool = enabled

    def load(self, test_config: Dict[str, Any]):
        """Load the configuration from a dictionary"""
        self.enabled = test_config.get("enabled", True)
