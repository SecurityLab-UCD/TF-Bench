from funcy import lfilter

from .common import BenchmarkTask
from .hs_parser import AST


def _is_type(code: str, type_name: str) -> bool:
    ast = AST(code)
    decl = ast.get_all_nodes_of_type(ast.root, "declarations")[0]
    decl_fst_child = decl.child(0)
    return decl_fst_child is not None and decl_fst_child.type == type_name


def is_data_type(code: str) -> bool:
    """check if the given line of code is a data type definition"""
    return _is_type(code, "data_type")


def is_class(code: str) -> bool:
    """check if the given line of code is a type class definition"""
    return _is_type(code, "class")


def def_new_type(type_name: str) -> str:
    """construct a new, empty yet unique type definition for a given Monomorphic type name"""
    return f"data {type_name} = {type_name}"


def def_new_type_class(class_name: str, type_vars: list[str]) -> str:
    """construct a new, empty yet unique type class definition for a given Ad-hoc type class name"""
    return f"class {class_name} {' '.join(type_vars)}"


def is_type_def(code: str) -> bool:
    """check if the given line of code is a type definition (data type or type class)"""
    return is_data_type(code) or is_class(code)


def is_type_defined(type_name: str, type_defs: list[str]) -> bool:
    """check if a type name is defined in the given list of type definitions"""
    return any(type_name in td for td in type_defs)


def get_type_defs(task: BenchmarkTask) -> list[str]:
    """Get Haskell type definitions from a BenchmarkTask"""
    existing_defs = lfilter(is_type_def, task.dependencies)
    ast = AST(task.signature)
    sig = ast.get_all_nodes_of_type(ast.root, "signature")[0]

    for node in ast.get_all_nodes_of_type(sig, "name"):
        ty = ast.get_src_from_node(node)
        if is_type_defined(ty, existing_defs):
            continue

        if node.parent and node.parent.type == "apply":  # type class
            existing_defs.append(def_new_type_class(ty, ["a"]))
        else:  # data type
            existing_defs.append(def_new_type(ty))

    return list(existing_defs)
