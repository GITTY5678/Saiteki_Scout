import ast
from sympy import symbols, log


class Time_Complexity:

    TIME_CONTRIBUTORS = {
        # Loops
        "For": ["iter"],
        "AsyncFor": ["iter"],
        "While": ["test", "body"],

        # Function Calls
        "Call": ["func", "args"],

        # Comprehensions
        "ListComp": [],
        "SetComp": [],
        "DictComp": [],
        "GeneratorExp": [],
        "comprehension": ["iter"],

        # Functions
        "FunctionDef": ["body"],
        "AsyncFunctionDef": ["body"],
        "Lambda": ["body"],

        # Conditional Structures
        "If": ["test", "body", "orelse"],
        "IfExp": ["test", "body", "orelse"],
        "Match": ["cases"],

        # Exception Handling
        "Try": ["body", "handlers", "finalbody"],
        "TryStar": ["body", "handlers", "finalbody"],
        "ExceptHandler": ["body"],

        # Data Structures
        "List": ["elts"],
        "Tuple": ["elts"],
        "Set": ["elts"],
        "Dict": ["keys", "values"],

        # Access Operations
        "Subscript": ["value", "slice"],
        "Slice": ["lower", "upper", "step"],

        # Expressions
        "BinOp": ["left", "right"],
        "UnaryOp": ["operand"],
        "BoolOp": ["values"],
        "Compare": ["left", "comparators"],

        # Assignment
        "Assign": ["value"],
        "AnnAssign": ["value"],
        "AugAssign": ["value"],

        # Return/Yield
        "Return": ["value"],
        "Yield": ["value"],
        "YieldFrom": ["value"],

        # Context Managers
        "With": ["items", "body"],
        "AsyncWith": ["items", "body"],

        # Classes
        "ClassDef": ["body"]
    }

    COMPLEXITY_KNOWLEDGE_BASE = {
    "len": "O(1)",
    "max": "O(n)",
    "min": "O(n)",
    "sum": "O(n)",
    "sorted": "O(n log n)",

    "append": "O(1)",
    "clear": "O(n)",
    "copy": "O(n)",
    "count": "O(n)",
    "extend": "O(k)",
    "index": "O(n)",
    "insert": "O(n)",
    "pop": "O(1)",
    "remove": "O(n)",
    "reverse": "O(n)",
    "sort": "O(n log n)",

    "fromkeys": "O(n)",
    "get": "O(1)",
    "items": "O(n)",
    "keys": "O(n)",
    "popitem": "O(1)",
    "setdefault": "O(1)",
    "update": "O(m)",
    "values": "O(n)",

    "add": "O(1)",
    "difference": "O(n)",
    "difference_update": "O(n)",
    "discard": "O(1)",
    "intersection": "O(min(n,m))",
    "intersection_update": "O(min(n,m))",
    "isdisjoint": "O(min(n,m))",
    "issubset": "O(n)",
    "issuperset": "O(m)",
    "symmetric_difference": "O(n+m)",
    "symmetric_difference_update": "O(n+m)",
    "union": "O(n+m)"
}
    FIELD_RESOLVERS = {
    "iter": "resolve_iter",
    "func": "resolve_func",
    "generators": "resolve_generators"
}
    def __init__(self, code):
        self.code = code
        self.tree = None
        self.node_stack = []
        self.n, self.m, self.k = symbols("n m k")

    def get_contributor_info(self, node):
        node_name = type(node).__name__

        info = {"node": node_name}

        for field in self.TIME_CONTRIBUTORS[node_name]:
            value = getattr(node, field, None)

            try:
                if isinstance(value, list):
                    info[field] = [
                        ast.unparse(item) if isinstance(item, ast.AST)
                        else str(item)
                        for item in value
                    ]

                elif isinstance(value, ast.AST):
                    info[field] = ast.unparse(value)

                else:
                    info[field] = value

            except Exception:
                info[field] = str(value)

        return info
    def resolve_iter(self, value):
    
        if "range(" in value:
            return self.n

        return 1
    
    def resolve_func(self, value):
    
        complexity_map = {
            "O(1)": 1,
            "O(n)": self.n,
            "O(m)": self.m,
            "O(k)": self.k,
            "O(n log n)": self.n * log(self.n),
            "O(n+m)": self.n + self.m
        }

        if value in self.COMPLEXITY_KNOWLEDGE_BASE:

            complexity = self.COMPLEXITY_KNOWLEDGE_BASE[value]

            return complexity_map.get(complexity, 1)

        if "." in value:

            method = value.split(".")[-1]

            if method in self.COMPLEXITY_KNOWLEDGE_BASE:

                complexity = self.COMPLEXITY_KNOWLEDGE_BASE[method]

                return complexity_map.get(complexity, 1)

        return 1
    
    def resolve_generators(self, value):
    
        return self.n
    
    def resolve_complexity(self, contributor):
    
        total_complexity = 1

        for field, value in contributor.items():

            if field == "node":
                continue

            resolver_name = self.FIELD_RESOLVERS.get(field)

            if resolver_name is None:
                continue

            resolver = getattr(self, resolver_name)

            contribution = resolver(value)

            total_complexity *= contribution

        return total_complexity
    
    def visit(self, node):
        node_name = type(node).__name__
        pushed = False

        if node_name in self.TIME_CONTRIBUTORS:
            pushed = True

            contributor_info = self.get_contributor_info(node)

            contributor_info["complexity"] = (
                self.resolve_complexity(contributor_info)
            )

            self.node_stack.append(contributor_info)

            print("\nENTER")
            print(contributor_info)

            print("\nSTACK")
            for item in self.node_stack:
                print(item)

            print("-" * 60)

        for child in ast.iter_child_nodes(node):
            self.visit(child)

        if pushed:
            popped = self.node_stack.pop()

            print("\nEXIT")
            print(popped)

            print("\nSTACK")
            for item in self.node_stack:
                print(item)

            print("=" * 60)

    def analyzer(self):
        self.tree = ast.parse(self.code)
        self.visit(self.tree)


if __name__ == "__main__":

    code = """
a = sorted(arr)

for i in range(n):
    if i > 5:
        x = [j for j in range(n)]
        print(x)
"""

    tc = Time_Complexity(code)
    tc.analyzer()