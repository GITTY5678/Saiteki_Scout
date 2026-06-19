import ast
from sympy import symbols, log, simplify, Add, Mul,sympify


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
        #"List": ["elts"],
        #"Tuple": ["elts"],
        #"Set": ["elts"],
        #"Dict": ["keys", "values"],

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
    RECURRENCE_KNOWLEDGE_BASE = {

    "T(n-1)+O(1)": "O(n)",

    "T(n-1)+O(n)": "O(n**2)",

    "T(n-1)+T(n-2)+O(1)": "O(2**n)",

    "2T(n/2)+O(n)": "O(n*log(n))",

    "2T(n/2)+O(1)": "O(n)",

    "T(n/2)+O(1)": "O(log(n))"
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
        self.complexity_stack = []

        self.result_tree = []
        self.tree_stack = []

        self.n, self.m, self.k = symbols("n m k")
        self.contributions = []
        self.current_function = None

        self.recursion_info = {
    "detected": False,
    "function": None,
    "calls": 0,
    "recursive_calls": [],
    "recurrence": None
}
        self.binary_search_info = {
    "detected": False
}   
        self.two_pointer_info = {
    "detected": False
}
        self.sliding_window_info = {
    "detected": False
}
    def detect_binary_search(self, node):
    
        if not isinstance(node, ast.While):
            return

        found_mid = False

        found_left_update = False

        found_right_update = False

        for child in ast.walk(node):

            # mid = (...)
            if isinstance(child, ast.Assign):

                for target in child.targets:

                    if (
                        isinstance(target, ast.Name)
                        and target.id == "mid"
                    ):
                        found_mid = True

            # left = mid + 1
            if isinstance(child, ast.Assign):

                if (
                    len(child.targets) == 1
                    and isinstance(
                        child.targets[0],
                        ast.Name
                    )
                ):

                    target_name = (
                        child.targets[0].id
                    )

                    try:

                        value = ast.unparse(
                            child.value
                        )

                        if (
                            target_name == "left"
                            and "mid" in value
                        ):
                            found_left_update = True

                        if (
                            target_name == "right"
                            and "mid" in value
                        ):
                            found_right_update = True

                    except:
                        pass

        if (
            found_mid
            and found_left_update
            and found_right_update
        ):

            self.binary_search_info[
                "detected"
            ] = True
    def detect_sliding_window(self, node):
    
        if not isinstance(node, ast.For):
            return

        left_moves = False

        for child in ast.walk(node):

            if isinstance(child, ast.AugAssign):

                if (
                    isinstance(child.target, ast.Name)
                    and child.target.id == "left"
                ):
                    left_moves = True

            if isinstance(child, ast.Assign):

                if (
                    len(child.targets) == 1
                    and isinstance(
                        child.targets[0],
                        ast.Name
                    )
                ):

                    target = child.targets[0].id

                    try:

                        value = ast.unparse(
                            child.value
                        )

                        if (
                            target == "left"
                            and "left" in value
                        ):
                            left_moves = True

                    except:
                        pass

        if left_moves:

            self.sliding_window_info[
                "detected"
            ] = True
    def detect_two_pointers(self, node):
    
        if not isinstance(node, ast.While):
            return

        left_moves = False
        right_moves = False

        for child in ast.walk(node):

            if isinstance(child, ast.AugAssign):

                if (
                    isinstance(child.target, ast.Name)
                    and child.target.id == "left"
                ):
                    left_moves = True

                if (
                    isinstance(child.target, ast.Name)
                    and child.target.id == "right"
                ):
                    right_moves = True

            if isinstance(child, ast.Assign):

                if (
                    len(child.targets) == 1
                    and isinstance(
                        child.targets[0],
                        ast.Name
                    )
                ):

                    target = child.targets[0].id

                    try:

                        value = ast.unparse(
                            child.value
                        )

                        if (
                            target == "left"
                            and "left" in value
                        ):
                            left_moves = True

                        if (
                            target == "right"
                            and "right" in value
                        ):
                            right_moves = True

                    except:
                        pass

        if left_moves and right_moves:

            self.two_pointer_info[
                "detected"
            ] = True
    def normalize_recurrence(self, recurrence):
    
        recurrence = recurrence.replace(" ", "")

        return recurrence
    def solve_recurrence(self):
    
        recurrence = self.recursion_info["recurrence"]

        if recurrence is None:
            return None

        recurrence = self.normalize_recurrence(
            recurrence
        )

        return self.RECURRENCE_KNOWLEDGE_BASE.get(
            recurrence,
            "Unknown"
        )
    def build_recurrence(self):
    
        if not self.recursion_info["detected"]:
            return None

        calls = self.recursion_info["recursive_calls"]

        recurrence_parts = []

        for call in calls:

            arg = call[0]

            recurrence_parts.append(
                f"T({arg})"
            )

        recurrence = " + ".join(
            recurrence_parts
        )

        recurrence += " + O(1)"

        return recurrence
    def get_dominant_term(self, expr):
    
        expr = expr.expand()

        if not isinstance(expr, Add):
            return expr

        terms = expr.as_ordered_terms()

        def rank(term):

            powers = term.as_powers_dict()

            n_power = powers.get(self.n, 0)

            has_log = log(self.n) in powers

            return (
                n_power,
                1 if has_log else 0
            )

        return max(terms, key=rank)
    def detect_recursion(self, node):
        if isinstance(node, ast.FunctionDef):
    
            previous_function = self.current_function

            self.current_function = node.name

            for child in ast.iter_child_nodes(node):
                self.detect_recursion(child)

            self.current_function = previous_function

            return
        # Entering a function
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and self.current_function is not None
            and node.func.id == self.current_function
        ):

            self.recursion_info["detected"] = True

            self.recursion_info["function"] = self.current_function

            self.recursion_info["calls"] += 1

            args = []

            for arg in node.args:
                args.append(
                    ast.unparse(arg)
                )

            self.recursion_info["recursive_calls"].append(
                args
            )
            return

        # Function call
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and self.current_function is not None
            and node.func.id == self.current_function
        ):

            self.recursion_info["detected"] = True

            self.recursion_info["function"] = self.current_function

            self.recursion_info["calls"] += 1

        for child in ast.iter_child_nodes(node):
            self.detect_recursion(child)
    
    def classify_recursion(self):
    
        calls = self.recursion_info["calls"]

        if calls == 0:
            return None

        if calls == 1:
            return "Linear Recursion"

        if calls == 2:
            return "Binary Recursion"

        return "Multiple Recursion"
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

        SIZE_MAP = {
            "arr": self.n,
            "nums": self.n,
            "data": self.n,
            "lst": self.n
        }

        value = value.strip()

        # range(...)
        if value.startswith("range("):

            inside = value[6:-1].strip()

            try:

                expr = sympify(
                    inside,
                    locals={
                        "n": self.n,
                        "m": self.m,
                        "k": self.k
                    }
                )

                if expr.is_number:
                    return 1

                return expr

            except Exception:
                return 1

        # known iterable variables
        if value in SIZE_MAP:
            return SIZE_MAP[value]

        # unknown iterable variables
        if value.isidentifier():
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
        if (
            node_name == "Call"
            and isinstance(node.func, ast.Name)
            and node.func.id == "range"
        ):
            return
        pushed = False

        if node_name in self.TIME_CONTRIBUTORS:
            pushed = True

            contributor_info = self.get_contributor_info(node)

            contributor_info["complexity"] = (
                self.resolve_complexity(contributor_info)
            )
            self.contributions.append(
            (
                contributor_info["node"],
                contributor_info["complexity"]
            )
)

            tree_node = {
                "info": contributor_info,
                "children": []
            }

            if self.tree_stack:
                parent = self.tree_stack[-1]
                parent["children"].append(tree_node)
            else:
                self.result_tree.append(tree_node)

            self.tree_stack.append(tree_node)

            self.node_stack.append(contributor_info)

            

        for child in ast.iter_child_nodes(node):
            self.visit(child)

        if pushed:

            finished_tree_node = self.tree_stack.pop()

            popped = self.node_stack.pop()
    def reduce_tree(self, node):
    
        current_complexity = node["info"]["complexity"]

        if not node["children"]:
            return current_complexity

        children = [
            self.reduce_tree(child)
            for child in node["children"]
        ]

        children_complexity = Add(
            *children,
            evaluate=False
        )

        return Mul(
            current_complexity,
            children_complexity,
            evaluate=False
        )
    
    def reduce_forest(self):
    
        expressions = [
            self.reduce_tree(root)
            for root in self.result_tree
        ]

        return Add(
            *expressions,
            evaluate=False
        )
    
    def analyzer(self):
    
        # -------------------------
        # PARSE
        # -------------------------
        self.tree = ast.parse(self.code)

        # -------------------------
        # DETECT RECURSION
        # -------------------------
        self.detect_recursion(self.tree)

        # -------------------------
        # DETECT BINARY SEARCH
        # -------------------------
        for node in ast.walk(self.tree):
            self.detect_binary_search(node)
            self.detect_two_pointers(node)
            self.detect_sliding_window(node)
        # -------------------------
        # BUILD CONTRIBUTION TREE
        # -------------------------
        self.visit(self.tree)

        # -------------------------
        # AST COMPLEXITY
        # -------------------------
        basic_expression = self.reduce_forest()

        simplified_expression = simplify(
            basic_expression
        )

        dominant_term = self.get_dominant_term(
            simplified_expression
        )

        ast_complexity = f"O({dominant_term})"

        # -------------------------
        # RECURSION COMPLEXITY
        # -------------------------
        recurrence = self.build_recurrence()

        self.recursion_info["recurrence"] = recurrence

        recursive_complexity = None

        if self.recursion_info["detected"]:

            recursive_complexity = (
                self.solve_recurrence()
            )

        # -------------------------
        # FINAL COMPLEXITY DECISION
        # -------------------------
        final_complexity = ast_complexity

        if self.binary_search_info["detected"]:
    
            final_complexity = "O(log(n))"

        elif self.two_pointer_info["detected"]:

            final_complexity = "O(n)"

        elif self.sliding_window_info["detected"]:

            final_complexity = "O(n)"

        elif recursive_complexity:

            final_complexity = recursive_complexity

        # -------------------------
        # CONTRIBUTIONS
        # -------------------------
        print("\nCONTRIBUTIONS")
        print("-" * 30)

        for idx, (node, comp) in enumerate(
            self.contributions,
            start=1
        ):
            print(
                f"{idx}. {node} -> {comp}"
            )

        # -------------------------
        # AST REPORT
        # -------------------------
        print("\nBASIC EXPRESSION")
        print("-" * 30)
        print(basic_expression)

        print("\nSIMPLIFIED EXPRESSION")
        print("-" * 30)
        print(simplified_expression)

        print("\nDOMINANT TERM")
        print("-" * 30)
        print(dominant_term)

        # -------------------------
        # BINARY SEARCH REPORT
        # -------------------------
        print("\nBINARY SEARCH REPORT")
        print("-" * 30)

        print(
            f"Detected : "
            f"{self.binary_search_info['detected']}"
        )

        # -------------------------
        # RECURSION REPORT
        # -------------------------
        print("\nRECURSION REPORT")
        print("-" * 30)

        print(
            f"Detected : "
            f"{self.recursion_info['detected']}"
        )
        print("\nTWO POINTER REPORT")
        print("-" * 30)

        print(
            f"Detected : "
            f"{self.two_pointer_info['detected']}"
        )
        print("\nSLIDING WINDOW REPORT")
        print("-" * 30)

        print(
            f"Detected : "
            f"{self.sliding_window_info['detected']}"
        )
        if self.recursion_info["detected"]:

            print(
                f"Function : "
                f"{self.recursion_info['function']}"
            )

            print(
                f"Recursive Calls : "
                f"{self.recursion_info['calls']}"
            )

            print(
                f"Type : "
                f"{self.classify_recursion()}"
            )

            print("\nRECURRENCE")
            print("-" * 30)
            print(recurrence)

            print("\nRECURSIVE COMPLEXITY")
            print("-" * 30)
            print(recursive_complexity)

        # -------------------------
        # FINAL RESULT
        # -------------------------
        print("\nFINAL COMPLEXITY")
        print("-" * 30)
        print(final_complexity)
if __name__ == "__main__":

    code = """
left = 0
right = len(arr)-1

while left < right:

    if arr[left] + arr[right] == target:
        break

    elif arr[left] + arr[right] < target:
        left += 1

    else:
        right -= 1
"""

    tc = Time_Complexity(code)
    tc.analyzer()