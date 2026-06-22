import ast
from sympy import symbols

class Space_Complexity:
    """
    Static space complexity analyzer for Python source code.

    This class parses Python code into an Abstract Syntax Tree
    (AST) and estimates memory growth by analyzing container
    allocations and comprehension constructs.

    Supported structures include:

    - List
    - ListComprehension
    - Dictionary
    - DictionaryComprehension
    - Set
    - SetComprehension
    - Tuple
    - GeneratorExpression

    Examples
    --------
    >>> sc = Space_Complexity(code)
    >>> sc.analyzer()
        """
    SPACE_CONTRIBUTORS = {

    "List": "O(n)",

    "ListComp": "O(n)",

    "Set": "O(n)",

    "SetComp": "O(n)",

    "Dict": "O(n)",

    "DictComp": "O(n)",

    "Tuple": "O(n)",

    "GeneratorExp": "O(1)"
}
    def __init__(self, code):

        self.code = code

        self.tree = None

        self.space_contributions = []
        

        self.n = symbols("n")
    def resolve_space(self, node):
    
        if isinstance(node, ast.List):

            size = len(node.elts)

            return 1 if size < 20 else self.n

        if isinstance(node, ast.ListComp):
    
            return self.resolve_listcomp_space(
                node
            )

        if isinstance(node, ast.DictComp):

            return self.n

        if isinstance(node, ast.SetComp):

            return self.n

        if isinstance(node, ast.GeneratorExp):

            return 1

        return 1
    def resolve_listcomp_space(self, node):
    
        total = self.n

        element = node.elt

        if isinstance(element, ast.List):

            total *= self.n

        elif isinstance(element, ast.BinOp):

            total *= self.n

        return total
    def detect_space(self, node):
    
        node_name = type(node).__name__

        if node_name in self.SPACE_CONTRIBUTORS:

            contribution = {

                "node": node_name,

                "space": self.resolve_space(node)
            }

            self.space_contributions.append(
                contribution
            )
    def visit(self):
    
        for node in ast.walk(self.tree):

            self.detect_space(node)
    def dominant_space(self):
    
        if not self.space_contributions:

            return 1

        return max(
            item["space"]
            for item in self.space_contributions
        )
    def analyzer(self):
        """
    Analyze the supplied Python source code and determine
    its overall space complexity.

    This method performs the complete space analysis pipeline:

    1. Parse source code into an AST.
    2. Traverse all AST nodes.
    3. Detect memory-allocating structures such as:
       - Lists
       - List Comprehensions
       - Dictionaries
       - Dictionary Comprehensions
       - Sets
       - Set Comprehensions
       - Tuples
       - Generator Expressions
    4. Estimate the space contribution of each structure.
    5. Identify the dominant space term.
    6. Produce a space complexity report.

    Outputs
    -------
    Space Contributions:
        Individual memory allocations detected in the code.

    Space Complexity:
        Estimated asymptotic space complexity.

    Notes
    -----
    The analysis is static and based on AST inspection.
    Actual runtime memory usage may differ depending on
    interpreter behavior and input characteristics.

    Returns
    -------
    None

    Examples
    --------
    >>> code = '''
    ... arr = [i for i in range(n)]
    ... '''
    >>> sc = Space_Complexity(code)
    >>> sc.analyzer()

    SPACE COMPLEXITY
    ----------------
    O(n)
    """
        self.tree = ast.parse(
            self.code
        )

        self.visit()

        print(
            "\nSPACE CONTRIBUTIONS"
        )

        print("-" * 30)

        for idx, item in enumerate(
            self.space_contributions,
            start=1
        ):

            print(
                f"{idx}. "
                f"{item['node']} "
                f"-> "
                f"{item['space']}"
            )

        final_space = self.dominant_space()

        print("\nSPACE COMPLEXITY")
        print("-" * 30)

        print(f"O({final_space})")
    