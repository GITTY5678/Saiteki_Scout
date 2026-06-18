import ast

code = """
n=int(input)
for i in range(n):
    print(i)
"""

tree = ast.parse(code)

print(ast.dump(tree, indent=4))