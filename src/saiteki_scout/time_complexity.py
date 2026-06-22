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
    CLASSIFICATION_KNOWLEDGE_BASE = {

    "Binary Search": {
        "best": "O(1)",
        "average": "O(log n)",
        "worst": "O(log n)"
    },

    "Quick Sort": {
        "best": "O(n log n)",
        "average": "O(n log n)",
        "worst": "O(n²)"
    },

    "Merge Sort": {
        "best": "O(n log n)",
        "average": "O(n log n)",
        "worst": "O(n log n)"
    },

    "Heap": {
        "best": "O(log n)",
        "average": "O(log n)",
        "worst": "O(log n)"
    },

    "DFS": {
        "best": "O(V+E)",
        "average": "O(V+E)",
        "worst": "O(V+E)"
    },

    "BFS": {
        "best": "O(V+E)",
        "average": "O(V+E)",
        "worst": "O(V+E)"
    },

    "Sliding Window": {
        "best": "O(n)",
        "average": "O(n)",
        "worst": "O(n)"
    },

    "Two Pointers": {
        "best": "O(n)",
        "average": "O(n)",
        "worst": "O(n)"
    },

    "Dynamic Programming": {
        "best": "O(n)",
        "average": "O(n)",
        "worst": "O(n)"
    }
}
    NODE_DISPLAY_NAMES = {

    "For": "For Loop",

    "While": "While Loop",

    "Call": "Function Call",

    "Assign": "Assignment",

    "AugAssign": "Assignment",

    "Compare": "Comparison",

    "BinOp": "Arithmetic Operation",

    "Subscript": "Array/List Access",

    "FunctionDef": "Function Definition",

    "Return": "Return Statement",

    "ListComp": "List Comprehension",

    "DictComp": "Dictionary Comprehension",

    "SetComp": "Set Comprehension",

    "GeneratorExp": "Generator Expression",

    "If": "Conditional Statement",

    "Lambda": "Lambda Function",

    "Yield": "Yield Statement"
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
    COMPLEXITY_GRAPHS = {

    "O(1)": lambda n: 1,

    "O(log(n))": lambda n: math.log2(n),

    "O(n)": lambda n: n,

    "O(n*log(n))": lambda n: n * math.log2(n),

    "O(n**2)": lambda n: n**2,

    "O(2**n)": lambda n: 2**n
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
        self.heap_info = {
    "detected": False,
    "operations": []
}
        self.dfs_info = {
    "detected": False
}
        self.bfs_info = {
    "detected": False
}
        self.merge_sort_info = {
    "detected": False
}
        self.quick_sort_info = {
    "detected": False
}
        self.dp_info = {
    "detected": False,
    "type": None
}
        self.insertion_sort_info = {
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
    def detect_insertion_sort(self, node):
    
        if not isinstance(node, ast.For):
            return

        has_while = False
        has_decrement = False

        for child in ast.walk(node):

            if isinstance(child, ast.While):
                has_while = True

                for grandchild in ast.walk(child):

                    if isinstance(grandchild, ast.AugAssign):

                        if (
                            isinstance(grandchild.op, ast.Sub)
                            and isinstance(
                                grandchild.target,
                                ast.Name
                            )
                        ):
                            has_decrement = True

                    elif isinstance(grandchild, ast.Assign):

                        try:

                            text = ast.unparse(
                                grandchild.value
                            )

                            if "-" in text:
                                has_decrement = True

                        except:
                            pass

        if has_while and has_decrement:

            self.insertion_sort_info["detected"] = True
    def detect_dp(self, node):
    
    # DP Array
        if isinstance(node, ast.Assign):

            try:

                target = ast.unparse(
                    node.targets[0]
                )

                if target == "dp":

                    self.dp_info["detected"] = True

                    self.dp_info["type"] = (
                        "Tabulation"
                    )

            except:
                pass

        # Memo Dictionary
        if isinstance(node, ast.Assign):

            try:

                target = ast.unparse(
                    node.targets[0]
                )

                value = ast.unparse(
                    node.value
                )

                if (
                    target == "memo"
                    and value == "{}"
                ):

                    self.dp_info["detected"] = True

                    self.dp_info["type"] = (
                        "Memoization"
                    )

            except:
                pass
    def detect_quick_sort(self, node):
    
        if not isinstance(node, ast.FunctionDef):
            return

        recursive_calls = 0

        has_pivot = False

        for child in ast.walk(node):

            # recursive calls
            if (
                isinstance(child, ast.Call)
                and isinstance(child.func, ast.Name)
                and child.func.id == node.name
            ):
                recursive_calls += 1

            # pivot variable
            if isinstance(child, ast.Assign):

                try:

                    for target in child.targets:

                        if (
                            isinstance(target, ast.Name)
                            and target.id == "pivot"
                        ):
                            has_pivot = True

                except:
                    pass

        if (
            recursive_calls == 2
            and has_pivot
        ):

            self.quick_sort_info[
                "detected"
            ] = True
    def detect_merge_sort(self, node):
    
        if not isinstance(node, ast.FunctionDef):
            return

        recursive_calls = 0

        has_mid = False

        has_slice = False

        for child in ast.walk(node):

            # recursive calls
            if (
                isinstance(child, ast.Call)
                and isinstance(child.func, ast.Name)
                and child.func.id == node.name
            ):
                recursive_calls += 1

            # mid variable
            if isinstance(child, ast.Assign):

                try:

                    for target in child.targets:

                        if (
                            isinstance(target, ast.Name)
                            and target.id == "mid"
                        ):
                            has_mid = True

                except:
                    pass

            # arr[:mid]
            if isinstance(child, ast.Slice):

                has_slice = True

        if (
            recursive_calls == 2
            and has_mid
            and has_slice
        ):

            self.merge_sort_info[
                "detected"
            ] = True
    def detect_dfs(self, node):
    
        if not isinstance(node, ast.FunctionDef):
            return

        function_name = node.name

        recursive_call = False

        graph_traversal = False

        for child in ast.walk(node):

            if (
                isinstance(child, ast.Call)
                and isinstance(child.func, ast.Name)
                and child.func.id == function_name
            ):
                recursive_call = True

            if isinstance(child, ast.For):

                try:

                    iterator = ast.unparse(
                        child.iter
                    )

                    if "[" in iterator:
                        graph_traversal = True

                except:
                    pass

        if recursive_call and graph_traversal:

            self.dfs_info["detected"] = True
    def detect_bfs(self, node):
    
        if not isinstance(node, ast.While):
            return

        found_popleft = False

        found_append = False

        for child in ast.walk(node):

            if isinstance(child, ast.Call):

                try:

                    func = ast.unparse(
                        child.func
                    )

                    if ".popleft" in func:
                        found_popleft = True

                    if ".append" in func:
                        found_append = True

                except:
                    pass

        if found_popleft and found_append:

            self.bfs_info["detected"] = True
    def detect_heap(self, node):
    
        if not isinstance(node, ast.Call):
            return

        try:

            func_name = ast.unparse(node.func)

        except:
            return

        heap_operations = {

            "heapq.heappush": "O(log n)",

            "heapq.heappop": "O(log n)",

            "heapq.heapreplace": "O(log n)",

            "heapq.heappushpop": "O(log n)",

            "heapq.heapify": "O(n)"
        }

        if func_name in heap_operations:

            self.heap_info["detected"] = True

            self.heap_info["operations"].append(
                (
                    func_name,
                    heap_operations[func_name]
                )
            )
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
    contributor_info.copy()
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

            self.detect_heap(node)

            self.detect_bfs(node)

            self.detect_dfs(node)

            self.detect_merge_sort(node)

            self.detect_quick_sort(node)

            self.detect_dp(node)

            self.detect_insertion_sort(node)
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
        elif self.heap_info["detected"]:
    
            complexities = [
                complexity
                for _, complexity
                in self.heap_info["operations"]
            ]

            if "O(n)" in complexities:
                final_complexity = "O(n)"
            else:
                final_complexity = "O(log n)"
        elif self.bfs_info["detected"]:
    
            final_complexity = "O(V+E)"

        elif self.dfs_info["detected"]:

            final_complexity = "O(V+E)"
        elif self.merge_sort_info["detected"]:
    
            final_complexity = "O(n*log(n))"
        elif self.quick_sort_info["detected"]:
    
            final_complexity = (
                "Average: O(n*log(n)), "
                "Worst: O(n**2)"
            )
        elif self.dp_info["detected"]:
    
            final_complexity = "O(n)"
        elif self.insertion_sort_info["detected"]:
    
            final_complexity = "O(n²)"
        elif recursive_complexity:

            final_complexity = recursive_complexity

        # -------------------------
        # CONTRIBUTIONS
        # -------------------------
        print("\nCONTRIBUTIONS")
        print("-" * 30)

        for idx, item in enumerate(
            self.contributions,
            start=1
        ):

            node = item["node"]

            display_name = (
                self.NODE_DISPLAY_NAMES.get(
                    node,
                    node
                )
            )

            complexity = item["complexity"]

            if node == "Call":

                func_name = item.get(
                    "func",
                    "unknown"
                )

                print(
                    f"{idx}. Function Call: "
                    f"{func_name}() "
                    f"-> O({complexity})"
                )

            else:

                print(
                    f"{idx}. "
                    f"{display_name} "
                    f"-> {complexity}"
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
        # DETECTED PATTERNS
        # -------------------------
        print("\nDETECTED PATTERNS")
        print("-" * 30)

        found_pattern = False
        if self.insertion_sort_info["detected"]:
    
            print(
                "Insertion Sort"
            )
        if self.binary_search_info["detected"]:

            found_pattern = True

            print("Binary Search")

        if self.two_pointer_info["detected"]:

            found_pattern = True

            print("Two Pointers")

        if self.sliding_window_info["detected"]:

            found_pattern = True

            print("Sliding Window")

        if self.heap_info["detected"]:

            found_pattern = True

            print("Heap")

            for op, complexity in (
                self.heap_info["operations"]
            ):

                print(
                    f"  {op} -> {complexity}"
                )

        if self.dfs_info["detected"]:

            found_pattern = True

            print("DFS")

        if self.bfs_info["detected"]:

            found_pattern = True

            print("BFS")

        if self.merge_sort_info["detected"]:

            found_pattern = True

            print("Merge Sort")

        if self.quick_sort_info["detected"]:

            found_pattern = True

            print("Quick Sort")

        if self.dp_info["detected"]:

            found_pattern = True

            print(
                f"Dynamic Programming "
                f"({self.dp_info['type']})"
            )

        if self.recursion_info["detected"]:

            found_pattern = True

            print("Recursion")

            print(
                f"  Function : "
                f"{self.recursion_info['function']}"
            )

            print(
                f"  Calls : "
                f"{self.recursion_info['calls']}"
            )

            print(
                f"  Type : "
                f"{self.classify_recursion()}"
            )

            if recurrence:

                print(
                    f"  Recurrence : "
                    f"{recurrence}"
                )

            if recursive_complexity:

                print(
                    f"  Complexity : "
                    f"{recursive_complexity}"
                )

        if not found_pattern:

            print(
                "No special algorithm pattern detected."
            )

        # -------------------------
        # FINAL RESULT
        # -------------------------
        print("\nFINAL COMPLEXITY")
        print("-" * 30)
        print(final_complexity)
        
        self.final_complexity=final_complexity
    def get_detected_algorithm(self):
    
        if self.binary_search_info["detected"]:
            return "Binary Search"

        if self.quick_sort_info["detected"]:
            return "Quick Sort"

        if self.merge_sort_info["detected"]:
            return "Merge Sort"

        if self.heap_info["detected"]:
            return "Heap"

        if self.bfs_info["detected"]:
            return "BFS"

        if self.dfs_info["detected"]:
            return "DFS"

        if self.sliding_window_info["detected"]:
            return "Sliding Window"

        if self.two_pointer_info["detected"]:
            return "Two Pointers"

        if self.dp_info["detected"]:
            return "Dynamic Programming"

        return None
    def classifier(self):
    
        algorithm = self.get_detected_algorithm()

        if algorithm is None:

            print("\nCLASSIFICATION")
            print("-" * 30)

            print(
                "No algorithm classification available."
            )

            return

        info = self.CLASSIFICATION_KNOWLEDGE_BASE[
            algorithm
        ]

        print("\nCLASSIFICATION")
        print("-" * 30)

        print(
            f"Algorithm : {algorithm}"
        )

        print(
            f"Best Case : {info['best']}"
        )

        print(
            f"Average Case : {info['average']}"
        )

        print(
            f"Worst Case : {info['worst']}"
        )
    def graph(self):
    
        import math
        import matplotlib.pyplot as plt

        complexity = self.final_complexity

        graph_map = {

            "O(1)": lambda n: 1,

            "O(log(n))": lambda n: math.log2(n),

            "O(n)": lambda n: n,

            "O(n*log(n))":
                lambda n: n * math.log2(n),

            "O(n**2)":
                lambda n: n**2,

            "O(2**n)":
                lambda n: 2**n
        }

        if complexity not in graph_map:

            print(
                "Graph unavailable "
                "for this complexity."
            )

            return

        x = [1,2,5,10,20,50,100]

        y = [
            graph_map[complexity](n)
            for n in x
        ]

        plt.plot(x, y)

        plt.title(
            f"Growth of {complexity}"
        )

        plt.xlabel("Input Size (n)")
        plt.ylabel("Operations")

        plt.grid(True)

        plt.show()