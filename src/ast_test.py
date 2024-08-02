# importing the requests library
from src.hs_parser.ast_util import AST
import json
from dacite import from_dict
import fire
from funcy_chain import Chain
import requests
from urllib.parse import quote
from src.common import BenchmarkTask
from src.filter2complete import extract_function_name
from src.hs_parser import HASKELL_LANGUAGE
from functools import lru_cache
from pprint import pprint
from tree_sitter import Node

"""
Idea to Solve 
1. Take everything after go and create an AST
2. Grab any "functions" type, and variables using the same algorithm to normally get functions
3. Thus we are able to remove any blacklist ones that are defined in where
"""

def main():
    # code = "until p f = go\n where\n go x | p x = x\n | otherwise = go (f x)"
    # where_index = code.index("where")
    # where_code = code[where_index + 5:].strip()
    # print(where_code)

    code = "lines \"\" = []\nlines s = cons (case break (== '\\n') s of\n (l, s') -> (l, case s' of\n [] -> []\n _:s'' -> lines s''))\n where\n cons ~(h, t) = h : t"
    # code = "words s = case dropWhile isSpace s of\n \"\" -> []\n s' -> w : words s''\n where (w, s'') =\n break isSpace s'"
    # code2 = "go x | p x = x\n | otherwise = go (f x)"
    ast = AST(code, HASKELL_LANGUAGE)
    root = ast.root

    # Get both types and type classes
    types_classes = (
        Chain(ast.get_all_nodes_of_type(root, "case"))
        .map(lambda d: [d, 
                        ast.get_src_from_node(d),
                        Chain(ast.get_all_nodes_of_type(d, None)).map(ast.get_src_from_node).value
                        ])
        .value
    )

    pprint(types_classes)
    # print(bindings)

main()