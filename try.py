import ast

for name in dir(ast):
    obj = getattr(ast, name)

    if isinstance(obj, type) and issubclass(obj, ast.AST):
        print(name)