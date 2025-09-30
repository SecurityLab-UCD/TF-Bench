from funcy import lfilter

from .common import BenchmarkTask
from .hs_parser import AST, get_type_constraints
from .hs_parser.extractor import TypeExtractor


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


def def_new_type_constructor(constructor_name: str, type_vars: list[str]) -> str:
    """construct a new, empty yet unique type constructor definition for a given type constructor name"""
    return f"data {constructor_name} {' '.join(type_vars)}"


def is_type_def(code: str) -> bool:
    """check if the given line of code is a type definition (data type or type class)"""
    return is_data_type(code) or is_class(code)


def is_type_defined(type_name: str, type_defs: list[str]) -> bool:
    """check if a type name is defined in the given list of type definitions"""
    return any(type_name in td for td in type_defs)


def get_type_defs(task: BenchmarkTask) -> list[str]:
    """Get Haskell type definitions from a BenchmarkTask"""
    existing_defs = lfilter(is_type_def, task.dependencies)

    if "=>" in task.signature:
        constrains = get_type_constraints(task.signature)
        for c in constrains:
            [ty_class, *ty_vars] = c.split(" ")
            if is_type_defined(ty_class, existing_defs):
                continue
            existing_defs.append(def_new_type_class(ty_class, ty_vars))

    extractor = TypeExtractor(task.signature)
    for ctor_name, arity in extractor.type_constructors.items():
        if is_type_defined(ctor_name, existing_defs):
            continue
        type_vars = [f"t{i}" for i in range(arity)]
        existing_defs.append(def_new_type_constructor(ctor_name, type_vars))

    for type_name in extractor.names:
        if is_type_defined(type_name, existing_defs):
            continue
        existing_defs.append(def_new_type(type_name))

    return list(existing_defs)
