from enum import Enum
from tree_sitter import Node
from funcy_chain import Chain
from .ast_util import AST


class PolymorphicType(str, Enum):
    """Polymorphism types based on Haskell's polymorphism.
    https://wiki.haskell.org/Polymorphism

    NO - No polymorphism. \n
    PARAMETRIC - Parametric polymorphism, allowing type parameters/variable.\n
    AD_HOC - Ad-hoc polymorphism, or constrained polymorphism\n
    RANK_N - Arbitrary-rank polymorphism, with universal quantification in types.\n
    """

    MONO = "Monomorphic"
    PARAMETRIC = "Parametric"
    AD_HOC = "Ad-hoc"
    RANK_N = "Arbitrary-rank"


def to_type_node(type_signature: Node) -> Node:
    """Get the type node from a type signature."""
    type_nodes = type_signature.children_by_field_name("type")
    assert len(type_nodes) == 1, "each type signature should has only 1 `type` child"
    return type_nodes[0]


def get_polymorphic_type(type_signature: Node) -> PolymorphicType:
    """Determine the polymorphic type of a given type signature node.

    Args:
        type_signature (Node): The type signature node to evaluate.

    Returns:
        PolymorphicType: The identified polymorphic type based on the node's characteristics.
    """
    assert type_signature.type == "signature", "Node must be of type 'signature'."

    type_node = to_type_node(type_signature)
    match type_node.type:
        case "forall":
            return PolymorphicType.RANK_N
        case "context":
            return PolymorphicType.AD_HOC
        case "function":
            if AST.has_any_child_of_type(type_node, "variable"):
                return PolymorphicType.PARAMETRIC

    return PolymorphicType.MONO


def get_type_vars(source_code: str) -> list[str]:
    """extract type variables from a type signature source code.

    NOTE: since GHC proves the `forall` quantification of type variables,
    the order of type variables does not really matter
    as long as they are **consistent**.

    Args:
        source_code (str): the source code of the type signature

    Returns:
        list[str]: type variables
    """
    ast = AST(source_code=source_code)
    sig = ast.get_all_nodes_of_type(ast.root, "signature")[0]
    type_node = to_type_node(sig)

    ty_vars = [
        ast.get_src_from_node(n)
        for n in ast.get_all_nodes_of_type(type_node, "variable")
    ]
    return list(dict.fromkeys(ty_vars))  # remove duplicates while preserving order


def get_type_constraints(source_code: str) -> list[str]:
    """extract type class constraints from a type signature source code"""
    assert "=>" in source_code, "no type class constraints found"

    ast = AST(source_code)
    signature = ast.get_all_nodes_of_type(ast.root, "signature")[0]

    # context node is the body of type signature
    context = ast.get_all_nodes_of_type(signature, "context")[0]

    type_constrains: list[str] = (
        Chain(ast.get_all_nodes_of_type(context.children[0], "apply"))
        .map(ast.get_src_from_node)
        .map(str.strip)
        .filter(lambda c: c[0].isupper())
        .value
    )
    return type_constrains
