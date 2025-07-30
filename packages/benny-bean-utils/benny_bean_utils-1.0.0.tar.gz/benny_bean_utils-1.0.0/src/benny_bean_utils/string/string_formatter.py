import unicodedata
import re

class StringFormatter:
    """
    Utility class for string formatting operations.
    """
    @staticmethod
    def get_snake_case_of_text(text: str) -> str:
        """
        Convert a string to snake_case, removing accents and special characters.

        Args:
            text (str): The input string to convert.

        Returns:
            str: The snake_case version of the input string.
        """
        normalized = unicodedata.normalize('NFKD', text)
        ascii_text = ''.join([c for c in normalized if not unicodedata.combining(c)])
        ascii_text = re.sub(r"['’]", '', ascii_text)
        return ascii_text.replace(" ", "_").lower()