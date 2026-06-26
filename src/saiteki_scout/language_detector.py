import re


class LanguageDetector:
    """
    Detects the programming language from source code.
    Currently supports:
        - Python
        - Java
    """

    @staticmethod
    def detect(code: str) -> str:
        code = code.strip()

        # ---------- Java ----------
        java_patterns = [
            r"\bpublic\s+class\b",
            r"\bclass\b",
            r"\bpublic\s+static\s+void\s+main\b",
            r"\bSystem\.out\.println\b",
            r"\bimport\s+java\.",
            r"\bpackage\s+[a-zA-Z0-9_.]+;",
        ]

        # ---------- Python ----------
        python_patterns = [
            r"\bdef\b",
            r"\bimport\b",
            r"\bfrom\s+\w+\s+import\b",
            r"\bif\s+__name__\s*==\s*['\"]__main__['\"]",
            r"\bprint\s*\(",
        ]

        java_score = sum(
            bool(re.search(pattern, code))
            for pattern in java_patterns
        )

        python_score = sum(
            bool(re.search(pattern, code))
            for pattern in python_patterns
        )

        if java_score > python_score:
            return "java"

        return "python"
    
code = """
def add(a,b):
    return a+b
"""

print(LanguageDetector.detect(code))