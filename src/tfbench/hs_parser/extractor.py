from collections import defaultdict, Counter
from dataclasses import dataclass
from tree_sitter import Node
from .ast_util import AST


class TypeExtractor(AST):
    """Static analyzer for Haskell type signatures.
    NOTE: this analyzer works on the body of a type signature only,
    i.e. the part after the `=>` symbol if it has constraints,
    or otherwise after the `::` symbol.
    The constraints (if any) are handled in other modules.
    """

    def __init__(self, code: str):
        super().__init__(code)
        self.constructors: dict[str, Counter] = defaultdict(Counter)
        self.names: set[str] = set()

        self._analysis_types()

    @property
    def type_constructors(self) -> dict[str, int]:
        """Get a mapping of type constructor names to their maximum observed arity (i.e. number of parameters)."""
        return {k: max(v.keys()) for k, v in self.constructors.items()}

    def _analysis_types(self):
        """analysis types in the function signature to fill out self.constructors and self.names"""
        sigs = self.get_all_nodes_of_type(self.root, "signature")
        functions = self.get_all_nodes_of_type(sigs[0], "function")
        if len(functions) > 0:
            self._visit(functions[0])

    def _collect_from_tuple(self, node: Node):
        # record tuple arity if you care: arity = count of element children
        # then continue walking children
        for ch in node.named_children:
            self._visit(ch)

    def _visit(self, n: Node):
        t = n.type

        if t == "apply":
            # Count this application chain once, at the top-most 'apply' only.
            parent = n.parent
            if not (
                parent
                and parent.type == "apply"
                and parent.child_by_field_name("constructor") is n
            ):
                apply_chain = _peel_apply_chain(n)
                ctor_name = self.get_src_from_node(apply_chain.constructor)
                self.constructors[ctor_name][apply_chain.arity] += 1
            # Recurse into children so we also catch nested names/applications.
            for ch in n.named_children:
                self._visit(ch)
            return

        if t == "constructor":
            # Zero-arity constructor occurrence (e.g., `Int`) not part of an apply
            parent = n.parent
            if not (
                parent
                and parent.type == "apply"
                and parent.child_by_field_name("constructor") is n
            ):
                name_node = n.child_by_field_name("name") or (
                    n.named_children[0] if n.named_children else None
                )
                if name_node:
                    constructor_name = self.get_src_from_node(name_node)
                    self.constructors[constructor_name][0] += 1
            # still walk inside
            for ch in n.named_children:
                self._visit(ch)
            return

        if t == "tuple":
            self._collect_from_tuple(n)
            return

        if t == "name":
            # Treat as a plain type variable/name when not under a constructor role.
            p = n.parent
            # If its parent is 'constructor', it's part of a constructor; skip here.
            if p is None or p.type != "constructor":
                self.names.add(self.get_src_from_node(n))
            return

        # default: recurse
        for ch in n.named_children:
            self._visit(ch)


@dataclass
class TypeApplyChain:
    constructor: Node
    arity: int
    arguments: list[Node]


def _peel_apply_chain(node: Node) -> TypeApplyChain:
    """
    Given an (apply ...) subtree, walk left through nested apply nodes to
    find the root constructor name and count how many arguments were applied.
    # Returns (arity, arg_nodes_list, constructor_node).
    """
    args = []
    arity = 0
    cur = node
    while cur.type == "apply":
        arity += 1
        arg = cur.child_by_field_name("argument")
        if arg is not None:
            args.append(arg)
        # could be 'constructor' or another 'apply'
        next_level = cur.child_by_field_name("constructor")
        if not next_level:
            break
        cur = next_level

    # now cur is either a 'constructor' node or a 'name' (rare)
    ctor_node = cur
    return TypeApplyChain(constructor=ctor_node, arity=arity, arguments=args)
