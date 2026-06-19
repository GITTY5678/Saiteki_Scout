import ast
from sympy import symbols

class Space_Complexity:
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
    