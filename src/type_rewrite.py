import re
import fire
import tree_sitter
from tree_sitter import Language
import tree_sitter_haskell
import json
from dacite import from_dict
from dataclasses import asdict
import string
from typing import Callable
from src.hs_parser.ast_util import AST
from src.common import BenchmarkTask
from src.postprocessing import postprocess
from typing import Optional


def preprocess(code: str) -> str:
    """
    Preprocess a line of code by adding spaces around parentheses, brackets, and the "::" symbol.

    Args:
        line (str): The line of code to preprocess.

    Returns:
        str: The preprocessed line of code with added spaces.
    """
    code = re.sub(r"\(", r"( ", code)
    code = re.sub(r"\)", r" )", code)

    code = re.sub(r"\[", r"[ ", code)
    code = re.sub(r"\]", r" ]", code)

    code = re.sub(r"::", r" :: ", code)
    code = re.sub(r"\,", " , ", code)
    return code


def reverse_process(code: str) -> str:
    """
    Reverse the preprocessing of a line of code by removing extra spaces around
    parentheses, brackets, commas, and the "::" symbol.

    Args:
        line (str): The line of code to reverse preprocess.

    Returns:
        str: The line of code with spaces removed around specific symbols.
    """
    code = re.sub(r"\(\s+", r"(", code)
    code = re.sub(r"\s+\)", r")", code)

    code = re.sub(r"\[\s+", r"[", code)
    code = re.sub(r"\s+\]", r"]", code)

    code = re.sub(r"\s*::\s*", r"::", code)
    code = re.sub(r"\s*,\s*", r",", code)

    return code


def convert_upper_to_lower(code: str) -> str:
    def convert_upper_to_lower_line(line: str, func_list: list[str]) -> str:
        """
        Process a line of code by converting certain elements to lowercase, replacing operators, and
        preserving leading spaces.

        Args:
            line (str): The line of code to process.
            func_list (List[str]): The list of function names to be modified.

        Returns:
            str: The processed line of code.
        """
        leading_spaces = ""
        while line and line[0].isspace():
            leading_spaces += line[0]
            line = line[1:]

        lst = line.split()
        for i, elem in enumerate(lst):
            # the first letter of a function cannot be capitalized
            if elem[0].isupper() and '"' not in elem and i == 0:
                func_list.append(elem)
                lst[i] = elem.lower() + "#"
            elif elem in func_list:
                lst[i] = elem.lower() + "#"

        return leading_spaces + " ".join(lst)

    lines = code.split("\n")
    func_list: list[str] = []
    for i, line in enumerate(lines):
        lines[i] = convert_upper_to_lower_line(line, func_list)
    return "\n".join(lines)


def remove_string_content(code: str) -> str:
    return re.sub(r"(?<!')\".*?\"(?!')", r'""', code)


def manual_change(code: str) -> str:
    code = re.sub(r"List\.foldl", r"foldll", code)  # Escape '.' to match literal '.'
    return code


def get_monomorphic_names(root: tree_sitter.Node) -> dict[str, int]:
    name_nodes = AST.get_all_nodes_of_type(root, "name")
    nothing_nodes = AST.get_all_nodes_of_name(root, "Nothing")

    return AST.get_nodes_start_bytes(name_nodes + nothing_nodes)


def get_parametric_names(root: tree_sitter.Node) -> dict[str, int]:
    param_nodes = []
    sig_nodes = AST.get_all_nodes_of_type(root, "signature")
    for node in sig_nodes:
        param_nodes += AST.get_all_nodes_of_type(node, "variable")

    return AST.get_nodes_start_bytes(param_nodes)


def get_function_names(root: tree_sitter.Node) -> dict[str, int]:
    func_nodes = AST.get_all_nodes_of_type(root, "function")
    sig_nodes = AST.get_all_nodes_of_type(root, "signature")
    app_nodes = AST.get_all_nodes_of_type(root, "apply")

    child_nodes = []
    for node in func_nodes + sig_nodes:
        if child_name_node := node.child_by_field_name("name"):
            child_nodes.append(child_name_node)

    for node in app_nodes:
        if app_child_nodes := node.children:
            child_nodes.append(app_child_nodes[0])

    return AST.get_nodes_start_bytes(child_nodes)


def get_variable_names(root: tree_sitter.Node) -> dict[str, int]:
    var_nodes = AST.get_all_nodes_of_type(root, "variable")
    return AST.get_nodes_start_bytes(var_nodes)


def replace_names(
    node: tree_sitter.Node,
    combined_map: dict[str, str],
) -> list[tuple[int, int, str]]:
    """
    Recursively replace function and variable names in the syntax tree using provided mappings.

    Args:
        node (tree_sitter.Node): The current node in the syntax tree.
        combined_map (dict): A dictionary mapping original function and variable names to replacement names.

    Returns:
        List[Tuple[int, int, str]]: A list of tuples containing the start byte,
                                    end byte, and replacement string.
    """
    replacements = []

    if node.type in ["variable", "constructor", "operator", "type", "name"]:
        if node.text is not None:  # Ensure node.text is not None before decoding
            name = node.text.decode("utf-8")
            if name in combined_map:
                replacements.append(
                    (node.start_byte, node.end_byte, combined_map[name])
                )
            else:
                print(
                    f"Warning: Name '{name}' not found in combined_map, skipping replacement."
                )

    for child in node.children:
        replacements.extend(replace_names(child, combined_map))

    return replacements


def replace_in_code(code: str, replacements: list[tuple[int, int, str]]) -> str:
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


def rewrite(code: str) -> str:
    lang = Language(tree_sitter_haskell.language())
    root_node = AST(code, lang).root

    param_names = get_parametric_names(root_node)
    type_names = get_monomorphic_names(root_node)
    func_names = get_function_names(root_node)
    var_names = get_variable_names(root_node)

    func_names = {
        name: pos for name, pos in func_names.items() if name not in type_names
    }
    param_names = {
        name: pos
        for name, pos in param_names.items()
        if name not in type_names and name not in func_names
    }
    var_names = {
        name: pos
        for name, pos in var_names.items()
        if name not in func_names and name not in param_names
    }  # Ensure var_names does not contain func_names

    # Sort the function and variable names by their first appearance in the code (start byte)
    type_names_list = [
        name for name, _ in sorted(type_names.items(), key=lambda x: x[1])
    ]
    func_names_list = [
        name for name, _ in sorted(func_names.items(), key=lambda x: x[1])
    ]
    var_names_list = [name for name, _ in sorted(var_names.items(), key=lambda x: x[1])]

    print("type names: ", type_names_list)
    print("function names: ", func_names_list)
    print("variable names: ", var_names_list)
    print("\n" * 2)

    # not to rewrite otherwise
    if "otherwise" in var_names_list:
        var_names_list.remove("otherwise")

    letters = string.ascii_uppercase  # 'A' to 'Z'
    type_map = {typ: letters[i % 26] for i, typ in enumerate(type_names_list)}
    func_map = {func: f"f{i + 1}" for i, func in enumerate(func_names_list)}
    var_map = {var: f"v{i + 1}" for i, var in enumerate(var_names_list)}

    print("type_map: ", type_map)
    print("func_map: ", func_map)
    print("var_map: ", var_map)
    print("\n" * 2)

    combined_map = {**type_map, **func_map, **var_map}
    replacements = replace_names(root_node, combined_map)
    modified_code = replace_in_code(code, replacements)

    return modified_code


def main(
    dataset_path: str = "Benchmark-F.json",
    output_path: str = "Benchmark-F.removed.json",
) -> None:
    lang = Language(tree_sitter_haskell.language())

    with open(dataset_path, "r") as fp:
        tasks = [from_dict(data_class=BenchmarkTask, data=d) for d in json.load(fp)]

    process_wrong_item = []
    rewrite_wrong_item = []
    for i, task in enumerate(tasks):
        # Ensure that task.dependencies, task.signature, and task.code are not None
        dependencies = task.dependencies if task.dependencies is not None else []
        signature = task.signature if task.signature is not None else ""
        code = task.code if task.code is not None else ""

        # put all code together
        combined_code = (
            "\n".join(dependencies)
            + "\n"
            + "-" * 20
            + "\n"
            + signature
            + "\n"
            + "-" * 20
            + "\n"
            + code
        )

        # print the raw code
        print("#" * 50)
        print(f"Start rewriting item {i}:")
        print(f"Task id is {task.task_id}")
        print("#" * 50)
        print(combined_code)
        print("\n" * 2)

        process_strategy: list[Callable[[str], str]] = [
            preprocess,
            manual_change,
            convert_upper_to_lower,
            remove_string_content,
            reverse_process,
        ]
        combined_code = postprocess(combined_code, process_strategy)

        # print the processed code
        print("#" * 50)
        print("processed code:")
        print("#" * 50)
        print(combined_code)
        print("\n" * 2)
        # check if the processed code is valid
        ast = AST(combined_code, lang)
        if not ast.is_valid_code():
            process_wrong_item.append(i)

        # print the rewritten code
        rewritten_code = rewrite(combined_code)
        print("#" * 50)
        print("rewritten code:")
        print("#" * 50)
        print(rewritten_code)
        print("\n" * 2)
        # check if the rewritten code is valid
        ast = AST(rewritten_code, lang)
        if not ast.is_valid_code():
            rewrite_wrong_item.append(i)
        # update the code to the rewritten version
        rewritten_parts = rewritten_code.split("\n" + "-" * 20 + "\n")
        task.dependencies = rewritten_parts[0].split("\n")
        task.signature = rewritten_parts[1]
        task.code = rewritten_parts[2]

    print("ERROR while processing items:")
    print(process_wrong_item)

    print("ERROR while rewriting items:")
    print(rewrite_wrong_item)

    # If you need to dump the objects as dictionaries into a JSON file, do this step right before saving to the JSON file
    task_dicts = [asdict(task) for task in tasks]

    with open(output_path, "w") as fp:
        json.dump(task_dicts, fp)


if __name__ == "__main__":
    fire.Fire(main)
