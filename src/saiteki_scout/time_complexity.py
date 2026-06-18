import ast


class Time_Complexity:

    TIME_CONTRIBUTORS = {

        # Loops
        "For": ["iter"],
        "AsyncFor": ["iter"],
        "While": ["test", "body"],

        # Function Calls
        "Call": ["func", "args"],

        # Comprehensions
        "ListComp": ["generators"],
        "SetComp": ["generators"],
        "DictComp": ["generators"],
        "GeneratorExp": ["generators"],
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

    def __init__(self, code):

        self.code = code

        self.tree = None

        self.node_stack = []

    def visit(self, node):

        node_name = type(node).__name__

        pushed = False

        if node_name in self.TIME_CONTRIBUTORS:

            pushed = True

            self.node_stack.append(
                {
                    "node": node_name,
                    "fields": self.TIME_CONTRIBUTORS[node_name]
                }
            )

            print("\nENTER")
            print("NODE  :", node_name)
            print("FIELDS:", self.TIME_CONTRIBUTORS[node_name])
            print("STACK :")

            for item in self.node_stack:
                print(item)

            print("-" * 50)

        for child in ast.iter_child_nodes(node):
            self.visit(child)

        if pushed:

            popped = self.node_stack.pop()

            print("\nEXIT")
            print("NODE :", popped["node"])
            print("STACK :")

            for item in self.node_stack:
                print(item)

            print("=" * 50)

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