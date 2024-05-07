from enum import Enum
from tree_sitter.binding import Node
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


def get_polymorphic_type(type_signature: Node) -> PolymorphicType:
    """Determine the polymorphic type of a given type signature node.

    Args:
        type_signature (Node): The type signature node to evaluate.

    Returns:
        PolymorphicType: The identified polymorphic type based on the node's characteristics.
    """
    assert type_signature.type == "signature", "Node must be of type 'signature'."

    if AST.has_any_child_of_type(type_signature, "forall"):
        return PolymorphicType.RANK_N
    if AST.has_any_child_of_type(type_signature, "constraint"):
        return PolymorphicType.AD_HOC
    if AST.has_any_child_of_type(type_signature, "type_variable"):
        return PolymorphicType.PARAMETRIC

    return PolymorphicType.MONO
