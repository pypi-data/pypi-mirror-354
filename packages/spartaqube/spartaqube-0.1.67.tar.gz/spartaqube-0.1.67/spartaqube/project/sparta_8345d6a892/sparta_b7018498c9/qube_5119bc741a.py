import ast


def sparta_fe50a7e371(code):
    """
    This function returns the list of all the variables found in a code string (we'll then cross check on the 
    plotted variable list to check if we must reload some variables or not)
    """
    tree = ast.parse(code)
    all_variables = set()


    class VariableVisitor(ast.NodeVisitor):

        def visit_Name(self, node):
            all_variables.add(node.id)
            self.generic_visit(node)
    visitor = VariableVisitor()
    visitor.visit(tree)
    return list(all_variables)


def sparta_b73a88c789(script_text) ->list:
    """
    Returns the list of variables that'll be updated from the execution of script_text
    """
    return sparta_fe50a7e371(script_text)

#END OF QUBE
