import ast
def sparta_8ea57302fa(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_4d4e6c9f5e(script_text):return sparta_8ea57302fa(script_text)