"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""


class HttpUtilities:
    """Http Utilties"""

    @staticmethod
    def get_headers(jwt: str) -> dict:
        """Get the Http Headers"""
        headers = {
            "Content-Type": "application/json",
        }

        if jwt:
            headers["Authorization"] = f"Bearer {jwt}"

        return headers
