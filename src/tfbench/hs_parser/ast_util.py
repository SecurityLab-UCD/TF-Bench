from typing import Optional
from dataclasses import dataclass

from tree_sitter import Language, Parser, Tree, Node
import tree_sitter_haskell as ts_haskell
from returns.maybe import Maybe, Nothing, Some
from funcy_chain import Chain
from funcy import lmap

HASKELL_LANGUAGE = Language(ts_haskell.language())


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
        """
        Creates a `HaskellFunction` object from a tuple containing a type signature node and a list of function nodes.

        Args:
            p (tuple[Node, list[Node]]): A tuple with a type signature node and a list of function nodes.

        Returns:
            HaskellFunction: A new `HaskellFunction` object.
        """
        return HaskellFunction(*p)


class AST:
    """Helper class to build, read, and manipulate ASTs using tree-sitter."""

    def __init__(self, source_code: str) -> None:
        """
        Initializes an AST object with the given source code and language.

        Args:
            source_code (str): The source code to parse.
            lang (Language): The tree-sitter language used for parsing.
        """
        self.src = source_code
        self.parser = Parser()
        self.parser.language = HASKELL_LANGUAGE
        self.tree: Tree = self.parser.parse(bytes(self.src, "utf8"))

    @property
    def root(self) -> Node:
        """
        Gets the root node of the AST.

        Returns:
            Node: The root node of the AST.
        """
        return self.tree.root_node

    def get_src_from_node(self, node: Node) -> str:
        """
        Retrieves the source code corresponding to a given node.

        Args:
            node (Node): The AST node to extract source code from.

        Returns:
            str: The source code corresponding to the given node.
        """
        start = node.start_byte
        end = node.end_byte
        src_bytes = self.src.encode()
        node_bytes = src_bytes[start:end]
        return node_bytes.decode()

    def get_fn_name(self, node: Node) -> Maybe[str]:
        """
        Retrieves the name of a function or type signature from a node.

        Args:
            node (Node): The AST node representing a function or type signature.

        Returns:
            Maybe[str]: A Maybe containing the function name if found, or Nothing otherwise.
        """
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

    def func2src(self, func: HaskellFunction) -> tuple[str, str]:
        """
        Converts a `HaskellFunction` object into its corresponding type signature and code source.

        Args:
            func (HaskellFunction): The `HaskellFunction` object to convert.

        Returns:
            tuple[str, str]: A tuple containing the type signature and function code as strings.
        """
        type_src = self.get_src_from_node(func.type_signature)
        code_src = lmap(self.get_src_from_node, func.functions)
        code_src.sort()
        return type_src, "\n".join(code_src)

    def get_functions(self) -> list[HaskellFunction]:
        """
        Extracts all functions defined in the source code.

        Returns:
            list[HaskellFunction]: A list of `HaskellFunction` objects representing the functions in the source code.
        """
        signatures = AST.get_all_nodes_of_type(self.root, "signature")
        functions: dict[str, list[Node]] = (
            Chain(AST.get_all_nodes_of_type(self.root, "function"))
            .group_by_keys(self.get_fn_name)
            .value
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
            .filter(None)
            .map(HaskellFunction.from_pair)
            .value
        )
        return pairs

    def all_node_types(self, node: Optional[Node] = None) -> set[str]:
        """
        Collect all unique node types in the syntax tree.

        Args:
            node (Optional[Node]): The current node in the syntax tree.

        Returns:
            Set[str]: A set containing all unique node types found in the tree.
        """
        if node is None:
            node = self.root

        node_types: set[str] = set()

        for child in node.children:
            node_types |= self.all_node_types(child)  # Use |= to merge sets

        node_types.add(node.type)  # Add the current node's type

        return node_types

    def is_valid_code(self) -> bool:
        """
        Checks whether the parsed source code contains any syntax errors.

        Returns:
            bool: True if the code is valid, False if there are syntax errors.
        """
        return "ERROR" not in self.all_node_types()

    @staticmethod
    def get_all_nodes_of_type(
        root: Node, node_type: Optional[str], max_level=50
    ) -> list[Node]:
        """
        Recursively retrieves all nodes of a given type from the AST.

        Args:
            root (Node): The root node to start the search from.
            node_type (Optional[str]): The type of node to search for. If None, retrieves all nodes.
            max_level (int): The maximum recursion depth. Default is 50.

        Returns:
            list[Node]: A list of nodes matching the specified type.
        """
        nodes: list[Node] = []
        if max_level == 0:
            return nodes
        if node_type is None or root.type == node_type:
            nodes.append(root)

        for child in root.children:
            nodes += AST.get_all_nodes_of_type(
                child, node_type, max_level=max_level - 1
            )
        return nodes

    @staticmethod
    def get_all_nodes_of_name(
        root: Node, node_name: Optional[str], max_level=50
    ) -> list[Node]:
        """
        Recursively retrieves all nodes of a given name from the AST.

        Args:
            root (Node): The root node to start the search from.
            node_name (Optional[str]): The name of node to search for.
            max_level (int): The maximum recursion depth. Default is 50.

        Returns:
            list[Node]: A list of nodes matching the specified name.
        """
        nodes: list[Node] = []
        if max_level == 0:
            return nodes

        for child in root.children:
            if child.text and child.text.decode("utf-8") == node_name:
                nodes.append(child)
            nodes += AST.get_all_nodes_of_name(
                child, node_name, max_level=max_level - 1
            )
        return nodes

    @staticmethod
    def get_nodes_start_bytes(nodes: list[Node]) -> dict[str, int]:
        """Get the start byte positions of nodes by their names."""
        start_bytes: dict[str, int] = {}

        for node in nodes:
            if node.text and (node_name := node.text.decode("utf-8")):
                start_bytes[node_name] = min(
                    start_bytes.get(node_name, node.start_byte), node.start_byte
                )

        return start_bytes

    @staticmethod
    def has_any_child_of_type(
        root: Node, node_type: Optional[str], max_level: int = 50
    ) -> bool:
        """
        Checks whether any child of the root node has a specified type.

        Args:
            root (Node): The root node to search from.
            node_type (Optional[str]): The type of node to search for. If None, returns True if there are any children.
            max_level (int): The maximum recursion depth. Default is 50.

        Returns:
            bool: True if a child of the specified type is found, False otherwise.
        """
        if max_level == 0:
            return False

        has_child = False
        for child in root.children:
            if node_type is None or child.type == node_type:
                return True
            has_child |= AST.has_any_child_of_type(
                child, node_type, max_level=max_level - 1
            )
        return has_child
