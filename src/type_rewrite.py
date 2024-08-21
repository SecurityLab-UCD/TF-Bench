import re
import fire
import tree_sitter
from tree_sitter import Language, Parser
import tree_sitter_haskell
import json
from typing import List, Tuple, Set, Optional


# This is for replace the operators starting with ":", since these operator are not allowed in current tree_sitter_haskell
double_letters = [chr(i) * 2 for i in range(ord("a"), ord("z") + 1)]


def extract_and_modify_operators(input_string: str) -> str:
    """
    Extract infix operators within parentheses that appear before "::" and add spaces around these
    operators everywhere else in the string. This is to avoid the case when rewriting x+y to v1f1v2.
    So the spaces around an operator is necessary for readability.

    Args:
        input_string (str): The input string containing code.

    Returns:
        str: The modified string with spaces added around the operators.
    """
    # Step 1: Extract infix operators inside parentheses but before "::"
    operator_pattern = re.compile(r"\((.*?)\)\s*::")
    operators = operator_pattern.findall(input_string)

    # Step 2: Add spaces around the extracted operators everywhere else in the string
    for operator in operators:
        spaced_operator = f" {operator} "
        input_string = re.sub(
            rf"(?<!\()\b{re.escape(operator)}\b(?!\))", spaced_operator, input_string
        )

    return input_string


def move_line_up_after_arrow(text: str) -> str:
    """
    Move the next line up if the current line ends with "->" and the next line exists.
    tree_sitter_haskell doesn't allow the parts before and after "->" to be in two different lines.

    Args:
        text (str): The input string containing multiple lines of code.

    Returns:
        str: The modified string with lines moved up where applicable.
    """
    lines = text.splitlines()
    new_lines = []
    i = 0
    while i < len(lines):
        current_line = lines[i]
        if re.search(r"->\s*$", current_line) and i + 1 < len(lines):
            # If the current line ends with "->" and the next line exists, move it up
            current_line += " " + lines[i + 1].strip()
            i += 1  # Skip the next line as it's moved up
        new_lines.append(current_line)
        i += 1
    return "\n".join(new_lines)


def preprocess(line: str) -> str:
    """
    Preprocess a line of code by adding spaces around parentheses, brackets, and the "::" symbol.

    Args:
        line (str): The line of code to preprocess.

    Returns:
        str: The preprocessed line of code with added spaces.
    """
    line = re.sub(r"\(", r"( ", line)
    line = re.sub(r"\)", r" )", line)

    line = re.sub(r"\[", r"[ ", line)
    line = re.sub(r"\]", r" ]", line)

    line = re.sub(r"::", r" :: ", line)
    line = re.sub(r"\,", " , ", line)
    return line


def process(line: str) -> str:
    """
    Process a line of code by converting certain elements to lowercase, replacing operators, and
    preserving leading spaces.

    Args:
        line (str): The line of code to process.

    Returns:
        str: The processed line of code.
    """
    line = preprocess(line)
    leading_spaces = ""
    while line and line[0].isspace():
        leading_spaces += line[0]
        line = line[1:]

    lst = line.split()
    for i, elem in enumerate(lst):
        if elem[0].isupper() and '"' not in elem:
            lst[i] = elem.lower() + "#"
        elif elem[0] == ":" and len(elem) > 1 and elem[1] != ":":
            lst[i] = double_letters[ord(elem[1]) % 26]

    return leading_spaces + " ".join(lst)


def postprocess(line: str) -> str:
    """
    Post-process a line of code by removing spaces around certain characters and replacing double
    letters in parentheses.

    Args:
        line (str): The line of code to post-process.

    Returns:
        str: The post-processed line of code.
    """
    line = re.sub(r"\( ", r"(", line)
    line = re.sub(r" \)", r")", line)

    line = re.sub(r"\[ ", r"[", line)
    line = re.sub(r" \]", r"]", line)

    # Avoid replacing double quotes surrounded by single quotes
    line = re.sub(r"(?<!')\".*?\"(?!')", r'""', line)

    line = re.sub(r"\((\w)\1\)", r"\1\1", line)

    return line


def get_root(code: str) -> tree_sitter.Node:
    """
    Parse Haskell code and return the root node of the syntax tree.

    Args:
        code (str): The Haskell code to parse.

    Returns:
        tree_sitter.Node: The root node of the parsed syntax tree.
    """
    parser = Parser()
    parser.language = Language(tree_sitter_haskell.language())
    return parser.parse(code.encode("utf-8")).root_node


def get_byte_offset(code: str, line: int, column: int) -> int:
    """
    Calculate the byte offset for a given line and column in the code.

    Args:
        code (str): The Haskell code as a string.
        line (int): The line number (0-based).
        column (int): The column number (0-based).

    Returns:
        int: The byte offset corresponding to the line and column.
    """
    lines = code.splitlines(keepends=True)
    return sum(len(lines[i]) for i in range(line)) + column


def replace_in_code(code: str, replacements: List[Tuple[int, int, str]]) -> str:
    """
    Apply a list of replacements to the code, modifying specific byte ranges.

    Args:
        code (str): The original Haskell code as a string.
        replacements (List[Tuple[int, int, str]]): A list of tuples containing the start byte,
                                                   end byte, and replacement string.

    Returns:
        str: The modified code with replacements applied.
    """
    code_bytes = code.encode("utf-8")
    for start, end, replacement in sorted(
        replacements, key=lambda x: x[0], reverse=True
    ):
        code_bytes = code_bytes[:start] + replacement.encode("utf-8") + code_bytes[end:]
    return code_bytes.decode("utf-8")


def get_names(
    node: tree_sitter.Node, func_names: Set[str] = set(), var_names: Set[str] = set()
) -> Tuple[Set[str], Set[str]]:
    """
    Recursively traverse the syntax tree to collect function and variable names.

    Args:
        node (tree_sitter.Node): The current node in the syntax tree.
        func_names (Set[str]): A set to store function names.
        var_names (Set[str]): A set to store variable names.

    Returns:
        Tuple[Set[str], Set[str]]: Two sets containing the collected function and variable names.
    """
    if node.type == "function" or node.type == "signature":
        func_name = node.child_by_field_name("name")
        if func_name is not None and func_name.text is not None:
            func_names.add(func_name.text.decode("utf-8"))
    elif node.type == "apply":
        func_name = node.children[0] if node.children else None
        if func_name is not None and func_name.text is not None:
            func_names.add(func_name.text.decode("utf-8"))
    elif node.type == "operator":
        if node.text is not None:
            func_names.add(node.text.decode("utf-8"))
    elif node.type == "variable":
        if node.text is not None:
            var_names.add(node.text.decode("utf-8"))
    for child in node.children:
        get_names(child, func_names, var_names)

    return func_names, var_names


def replace_names(
    node: tree_sitter.Node,
    replacements: List[Tuple[int, int, str]],
    func_map: dict,
    var_map: dict,
) -> None:
    """
    Recursively replace function and variable names in the syntax tree using provided mappings.

    Args:
        node (tree_sitter.Node): The current node in the syntax tree.
        replacements (List[Tuple[int, int, str]]): A list to store replacement tuples.
        func_map (dict): A dictionary mapping original function names to replacement names.
        var_map (dict): A dictionary mapping original variable names to replacement names.
    """
    if node.type in ["variable", "constructor", "operator"]:
        if node.text is not None:
            name = node.text.decode("utf-8")
            if name in func_map:
                replacements.append((node.start_byte, node.end_byte, func_map[name]))
            elif name in var_map:
                replacements.append((node.start_byte, node.end_byte, var_map[name]))

    for child in node.children:
        replace_names(child, replacements, func_map, var_map)


def all_node_types(node: tree_sitter.Node, node_types: Set[str] = set()) -> Set[str]:
    """
    Collect all unique node types in the syntax tree.

    Args:
        node (tree_sitter.Node): The current node in the syntax tree.
        node_types (Set[str]): A set to store unique node types.

    Returns:
        Set[str]: A set containing all unique node types found in the tree.
    """
    node_types.add(node.type)

    for child in node.children:
        all_node_types(child, node_types)

    return node_types


def rewrite(code: str) -> str:
    """
    Rewrite the Haskell code by replacing function and variable names with standardized names.

    Args:
        code (str): The original Haskell code as a string.

    Returns:
        str: The rewritten Haskell code with standardized names.
    """
    root_node = get_root(code)

    func_names, var_names = get_names(root_node)

    var_names = var_names - func_names
    print("function names: ", func_names)
    print("variable names: ", var_names)
    print("\n" * 2)

    func_map = {
        func: f"f{i}"
        for i, func in enumerate(sorted(func_names, key=len, reverse=True))
    }
    var_map = {
        var: f"v{i}" for i, var in enumerate(sorted(var_names, key=len, reverse=True))
    }

    replacements: List[Tuple[int, int, str]] = []
    replace_names(root_node, replacements, func_map, var_map)
    modified_code = replace_in_code(code, replacements)

    return re.sub(r"\(([^)]+)\)\s*::", r"\1 ::", modified_code)


def main(
    dataset_path: str = "Benchmark-F.json",
    output_path: str = "Benchmark-F.removed.json",
) -> None:
    with open(dataset_path, "r") as file:
        data = json.load(file)

    for i, item in enumerate(data):
        # put all code together
        code = (
            "\n".join(item["dependencies"])
            + "\n"
            + "-" * 20
            + "\n"
            + item["signature"]
            + "\n"
            + "-" * 20
            + "\n"
            + item["code"]
        )

        # print the raw code
        print("#" * 50)
        print(f"Start rewriting item {i}:")
        print("#" * 50)
        print(code)
        print("\n" * 2)

        # process the raw code
        code = extract_and_modify_operators(code)
        code = move_line_up_after_arrow(code)
        code = "\n".join(
            [postprocess(process(preprocess(line))) for line in code.split("\n")]
        )

        # print the processed code
        print("#" * 50)
        print("processed code:")
        print("#" * 50)
        print(code)
        print("\n" * 2)

        root_node = get_root(code)
        assert "ERROR" not in all_node_types(
            root_node
        ), f"Error in the Process for item {i}"

        # print the rewritten code
        rewritten_code = rewrite(code)
        print("#" * 50)
        print("rewritten code:")
        print("#" * 50)
        print(rewritten_code)
        print("\n" * 2)

        root_node = get_root(rewritten_code)
        assert "ERROR" not in all_node_types(
            root_node
        ), f"Error in the Rewrite for item {i}"


if __name__ == "__main__":
    fire.Fire(main)
