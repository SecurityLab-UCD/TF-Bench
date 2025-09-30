# importing the requests library
from funcy_chain import Chain
from pprint import pprint
from tfbench.hs_parser import AST

"""
This is a test file for seeing all the Nodes in the AST of certain pieces of code
"""


def main():
    assert True
    code = "lines \"\" = []\nlines s = cons (case break (== '\\n') s of\n (l, s') -> (l, case s' of\n [] -> []\n _:s'' -> lines s''))\n where\n cons ~(h, t) = h : t"
    ast = AST(code)
    root = ast.root

    # Get both types and type classes
    types_classes = (
        Chain(ast.get_all_nodes_of_type(root, None))
        .map(
            lambda d: [
                d,
                ast.get_src_from_node(d),
                Chain(ast.get_all_nodes_of_type(d, None))
                .map(ast.get_src_from_node)
                .value,
            ]
        )
        .value
    )

    pprint(types_classes)


main()
