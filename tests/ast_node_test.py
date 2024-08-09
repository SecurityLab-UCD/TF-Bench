# importing the requests library
from src.hs_parser.ast_util import AST
import json
from dacite import from_dict
import fire
from funcy_chain import Chain
import requests
from urllib.parse import quote
from src.common import BenchmarkTask
from src.common import extract_function_name
from src.hs_parser import HASKELL_LANGUAGE
from functools import lru_cache
from pprint import pprint
from tree_sitter import Node

"""
This is a test file for seeing all the Nodes in the AST of certain pieces of code
"""


def main():
    assert True
    code = "lines \"\" = []\nlines s = cons (case break (== '\\n') s of\n (l, s') -> (l, case s' of\n [] -> []\n _:s'' -> lines s''))\n where\n cons ~(h, t) = h : t"
    ast = AST(code, HASKELL_LANGUAGE)
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
