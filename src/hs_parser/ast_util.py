"""Helper Class and Functions for tree-sitter AST"""

from tree_sitter import Language, Parser, Tree, Node
from returns.maybe import Maybe, Nothing, Some
from dataclasses import dataclass
from funcy_chain import Chain


@dataclass
class ASTLoc:
    lineno: int  # line number in the source file
    col: int  # column offset in the source file


@dataclass
class HaskellFunction:
    type_signature: Node
    functions: list[Node]

    @staticmethod
    def from_pair(p: tuple[Node, list[Node]]):
        return HaskellFunction(*p)


class AST:
    """Helper Class to build/read/manipulate AST with tree-sitter"""

    def __init__(self, source_code: str, lang: Language) -> None:
        self.src = source_code
        self.parser = Parser()
        self.parser.set_language(lang)
        self.tree: Tree = self.parser.parse(bytes(self.src, "utf8"))

    @property
    def root(self) -> Node:
        return self.tree.root_node

    def get_src_from_node(self, node: Node) -> str:
        start = node.start_byte
        end = node.end_byte
        return self.src[start:end]

    def get_fn_name(self, node: Node) -> Maybe[str]:
        fn_name: str
        match node.type:
            case "signature":
                signature_src = self.get_src_from_node(node)
                fn_name = signature_src.split("::")[0]
            case "function":
                func_src = self.get_src_from_node(node)
                fn_name = func_src.split(" ")[0]
            case _:
                return Nothing
        return Some(fn_name.strip())

    def get_fn_docstring(self, node: Node) -> Maybe[str]:
        # todo: implement docstring finder
        raise NotImplementedError

    def func2src(self, func: HaskellFunction) -> str:
        type_src = self.get_src_from_node(func.type_signature)
        code_src = Chain(func.functions).map(self.get_src_from_node).value
        code_src.sort()
        return "\n".join([type_src, *code_src])

    def get_functions(self) -> list[HaskellFunction]:
        """extract functions from an AST

        Args:
            root (Node): root node of the AST

        Returns:
            list[HaskellFunction]: [(type signature, [function code])]
        """
        signatures = AST.get_all_nodes_of_type(self.root, "signature")
        functions: dict[str, list[Node]] = (
            Chain(AST.get_all_nodes_of_type(self.root, "function")).group_by_keys(self.get_fn_name).value
        )

        def make_ty_fn_pair(type_signature: Node):
            return (
                self.get_fn_name(type_signature)
                .map(lambda fn_name: (type_signature, functions[fn_name]))
                .value_or(None)
            )

        pairs: list[HaskellFunction] = (
            Chain(signatures)
            .map(make_ty_fn_pair)
            .filter(None)  # short for filter(lambda x: x is not None)
            .map(HaskellFunction.from_pair)
            .value
        )
        return pairs

    @staticmethod
    def get_all_nodes_of_type(root: Node, node_type: str | None, max_level=50) -> list[Node]:
        """walk on AST and collect all nodes of the given type

        Args:
            root (Node): root node of tree or subtree
            node_type (str | None): type of node to collect, if None collect all Node
            max_level (int, optional): maximum recursion level. Defaults to 50.

        Returns:
            list[Node]: collected nodes
        """
        nodes: list[Node] = []
        if max_level == 0:
            return nodes

        for child in root.children:
            if type is None or child.type == node_type:
                nodes.append(child)
            nodes += AST.get_all_nodes_of_type(child, node_type, max_level=max_level - 1)
        return nodes

    @staticmethod
    def has_any_child_of_type(root: Node, node_type: str | None, max_level: int = 50) -> bool:
        """walk on AST and check if a node of `node_type` exists

        Args:
            root (Node): root node of tree or subtree
            node_type (str | None): type of node to collect, if None collect all Node
            max_level (int, optional): maximum recursion level. Defaults to 50.

        Returns:
            bool: `root` has and child of type `node_type`
        """
        if max_level == 0:
            return False

        has_child = False
        for child in root.children:
            if type is None or child.type == node_type:
                return True
            has_child |= AST.has_any_child_of_type(child, node_type, max_level=max_level - 1)
        return has_child
