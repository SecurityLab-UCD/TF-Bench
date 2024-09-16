import re
import fire
import tree_sitter

# import tree_sitter_haskell
from src.hs_parser.ast_util import AST
from tree_sitter import Language
import tree_sitter_haskell
import json
from dacite import from_dict
from src.common import BenchmarkTask
from typing import Optional
from dataclasses import asdict


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
        # a special case when the infix operator is .
        if operator == ".":
            pattern = r"(?<=\s|\()(\.)(?=\s|\))"
            input_string = re.sub(pattern, double_letters[ord(".") % 26], input_string)
            continue

        spaced_operator = f" {operator} "
        input_string = re.sub(
            rf"(?<!\()\b{re.escape(operator)}\b(?!\))", spaced_operator, input_string
        )

    return input_string


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
    leading_spaces = ""
    while line and line[0].isspace():
        leading_spaces += line[0]
        line = line[1:]

    func_list = []

    lst = line.split()
    for i, elem in enumerate(lst):
        # the first letter of a function cannot be capitalized
        if elem[0].isupper() and '"' not in elem and i == 0:
            func_list.append(elem)
            lst[i] = elem.lower() + "#"
        elif elem in func_list:
            lst[i] = elem.lower() + "#"
        # the first letter of a function cannot be ":"
        elif elem[0] == ":" and len(elem) > 1 and elem[1] != ":":
            lst[i] = double_letters[(ord(elem[0]) + ord(elem[1])) % 26]

        # for items such as List.foldl
        pattern = r"\b\w+\.\w+\b"
        lst[i] = re.sub(
            pattern, double_letters[sum([ord(l) for l in lst[i]]) % 26], lst[i]
        )

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
    # remove () for double letter functions (previous infix operators)
    line = re.sub(r"\((\w)\1\)", r"\1\1", line)

    return line


def get_names(
    node: tree_sitter.Node,
    func_names: Optional[dict[str, int]] = None,
    var_names: Optional[dict[str, int]] = None,
) -> tuple[dict[str, int], dict[str, int]]:
    if func_names is None:
        func_names = {}
    if var_names is None:
        var_names = {}

    if node.type in ("function", "signature"):
        func_name = node.child_by_field_name("name")
        if func_name and func_name.text:
            func_text = func_name.text.decode("utf-8")
            if func_text not in func_names:
                func_names[func_text] = func_name.start_byte

    elif node.type == "apply":
        func_name = node.children[0] if node.children else None
        if func_name and func_name.text:
            func_text = func_name.text.decode("utf-8")
            if func_text not in func_names:
                func_names[func_text] = func_name.start_byte
    elif node.type in ("operator", "variable"):
        if node.text:
            var_or_func_name = node.text.decode("utf-8")
            if node.type == "operator" and var_or_func_name not in func_names:
                func_names[var_or_func_name] = node.start_byte
            elif node.type == "variable" and var_or_func_name not in var_names:
                var_names[var_or_func_name] = node.start_byte

    for child in node.children:
        get_names(child, func_names, var_names)

    return func_names, var_names


def replace_names(
    node: tree_sitter.Node,
    type_map: dict[str, str],
    param_map: dict[str, str],
    func_map: dict[str, str],
    var_map: dict[str, str],
) -> list[tuple[int, int, str]]:
    """
    Recursively replace function and variable names in the syntax tree using provided mappings.

    Args:
        node (tree_sitter.Node): The current node in the syntax tree.
        func_map (dict): A dictionary mapping original function names to replacement names.
        var_map (dict): A dictionary mapping original variable names to replacement names.

    Returns:
        List[Tuple[int, int, str]]: A list of tuples containing the start byte,
                                    end byte, and replacement string.
    """
    replacements = []

    if node.type in ["variable", "constructor", "operator", "type", "name"]:
        if node.text is not None:
            name = node.text.decode("utf-8")
            if name in type_map:
                replacements.append((node.start_byte, node.end_byte, type_map[name]))
            elif name in param_map:
                replacements.append((node.start_byte, node.end_byte, param_map[name]))
            elif name in func_map:
                replacements.append((node.start_byte, node.end_byte, func_map[name]))
            elif name in var_map:
                replacements.append((node.start_byte, node.end_byte, var_map[name]))

    for child in node.children:
        replacements.extend(
            replace_names(child, type_map, param_map, func_map, var_map)
        )

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


def find_name_nodes(node):
    name_nodes = []

    # Check if this node is a name node
    if node.type == "name":
        name_nodes.append(node)

    # Recursively check child nodes
    for child in node.children:
        name_nodes.extend(find_name_nodes(child))

    return name_nodes


def collect_parametric_nodes(root: tree_sitter.Node) -> list[tree_sitter.Node]:
    result = []

    def collect_variables(node):
        if node.type == "variable":
            result.append(node)
        for child in node.children:
            collect_variables(child)

    def traverse(node):
        if node.type == "signature":
            collect_variables(node)
        else:
            for child in node.children:
                traverse(child)

    traverse(root)
    return result


def rewrite(code: str) -> str:
    lang = Language(tree_sitter_haskell.language())
    root_node = AST(code, lang).root

    ast = AST(code, lang)
    param_names = {
        node.text.decode("utf-8"): node.start_byte
        for node in collect_parametric_nodes(ast.tree.root_node)
    }
    type_names = {
        node.text.decode("utf-8"): node.start_byte
        for node in find_name_nodes(ast.tree.root_node)
    }

    func_names, var_names = get_names(root_node)
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
    param_names_list = [
        name for name, _ in sorted(param_names.items(), key=lambda x: x[1])
    ]
    func_names_list = [
        name for name, _ in sorted(func_names.items(), key=lambda x: x[1])
    ]
    var_names_list = [name for name, _ in sorted(var_names.items(), key=lambda x: x[1])]

    print("type names: ", type_names_list)
    print("param names: ", param_names_list)
    print("function names: ", func_names_list)
    print("variable names: ", var_names_list)
    print("\n" * 2)

    # Ensure indices for functions are assigned consecutively without skipping
    type_map = {typ: f"T{i + 1}" for i, typ in enumerate(type_names_list)}
    param_map = {param: f"t{i + 1}" for i, param in enumerate(param_names_list)}
    func_map = {func: f"f{i + 1}" for i, func in enumerate(func_names_list)}
    var_map = {var: f"v{i + 1}" for i, var in enumerate(var_names_list)}

    print("type_map: ", type_map)
    print("param_map: ", param_map)
    print("func_map: ", func_map)
    print("var_map: ", var_map)
    print("\n" * 2)

    # Get the replacements list from replace_names
    replacements = replace_names(root_node, type_map, param_map, func_map, var_map)
    modified_code = replace_in_code(code, replacements)

    return re.sub(r"\(([^)]+)\)\s*::", r"\1 ::", modified_code)


def main(
    dataset_path: str = "Benchmark-F.json",
    output_path: str = "Benchmark-F.removed.json",
) -> None:
    lang = Language(tree_sitter_haskell.language())

    with open(dataset_path, "r") as fp:
        tasks = [from_dict(data_class=BenchmarkTask, data=d) for d in json.load(fp)]

    wrong_item = []
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

        # process the raw code
        combined_code = extract_and_modify_operators(combined_code)

        combined_code = "\n".join(
            [
                postprocess(process(preprocess(line)))
                for line in combined_code.split("\n")
            ]
        )

        # print the processed code
        print("#" * 50)
        print("processed code:")
        print("#" * 50)
        print(combined_code)
        print("\n" * 2)

        ast = AST(combined_code, lang)
        # assert ast.is_valid_code(), f"Error in the Process for item {i}"
        assert ast.is_valid_code()

        if not ast.is_valid_code():
            wrong_item.append(i)

        # type_names = {node:node.start_byte for node in find_name_nodes(ast.root)}

        # print the rewritten code
        rewritten_code = rewrite(combined_code)
        print("#" * 50)
        print("rewritten code:")
        print("#" * 50)
        print(rewritten_code)
        print("\n" * 2)

        ast = AST(rewritten_code, lang)
        # assert ast.is_valid_code(), f"Error in the Rewrite for item {i}"
        if not ast.is_valid_code():
            wrong_item.append(i)

        rewritten_parts = rewritten_code.split("\n" + "-" * 20 + "\n")
        task.dependencies = rewritten_parts[0].split("\n")
        task.signature = rewritten_parts[1]
        task.code = rewritten_parts[2]

    print("ERROR while processing items:")
    print(set(wrong_item))

    # If you need to dump the objects as dictionaries into a JSON file, do this step right before saving to the JSON file
    task_dicts = [asdict(task) for task in tasks]

    with open(output_path, "w") as fp:
        json.dump(task_dicts, fp)


if __name__ == "__main__":
    fire.Fire(main)
