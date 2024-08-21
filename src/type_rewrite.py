import re
import fire
import tree_sitter
from tree_sitter import Language, Parser
import tree_sitter_haskell
import json
from typing import List, Tuple, Set, Optional


double_letters = [chr(i) * 2 for i in range(ord('a'), ord('z') + 1)]


def extract_and_modify_operators(input_string):
    # Step 1: Extract infix operators inside parentheses but before "::"
    operator_pattern = re.compile(r'\((.*?)\)\s*::')
    operators = operator_pattern.findall(input_string)
    
    # Step 2: Add spaces around the extracted operators everywhere else in the string
    for operator in operators:
        spaced_operator = f' {operator} '
        input_string = re.sub(rf'(?<!\()\b{re.escape(operator)}\b(?!\))', spaced_operator, input_string)
    
    return input_string

def move_line_up_after_arrow(text: str) -> str:
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
    line = re.sub(r"\(", r"( ", line)
    line = re.sub(r"\)", r" )", line)

    line = re.sub(r"\[", r"[ ", line)
    line = re.sub(r"\]", r" ]", line)

    line = re.sub(r"::", r" :: ", line)
    line = re.sub(r"\,", " , ", line)
    return line


def process(line: str) -> str:
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
            lst[i] = double_letters[ord(elem[1])%26]

    return leading_spaces + " ".join(lst)



def postprocess(line: str) -> str:
    line = re.sub(r"\( ", r"(", line)
    line = re.sub(r" \)", r")", line)

    line = re.sub(r"\[ ", r"[", line)
    line = re.sub(r" \]", r"]", line)

    line = re.sub(r'".*"', r'""', line)
    line = re.sub(r"\((\w)\1\)", r"\1\1", line)

    return line




def get_root(code: str) -> tree_sitter.Node:
    parser = Parser()
    parser.language = Language(tree_sitter_haskell.language())
    return parser.parse(code.encode("utf-8")).root_node


def get_byte_offset(code: str, line: int, column: int) -> int:
    lines = code.splitlines(keepends=True)
    return sum(len(lines[i]) for i in range(line)) + column


def replace_in_code(code: str, replacements: List[Tuple[int, int, str]]) -> str:
    code_bytes = code.encode("utf-8")
    for start, end, replacement in sorted(
        replacements, key=lambda x: x[0], reverse=True
    ):
        code_bytes = code_bytes[:start] + replacement.encode("utf-8") + code_bytes[end:]
    return code_bytes.decode("utf-8")


def get_names(
    node: tree_sitter.Node, func_names: Set[str] = set(), var_names: Set[str] = set()
) -> Tuple[Set[str], Set[str]]:
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
    if node.type in ["variable", "constructor", "operator"]:
        if node.text is not None:
            name = node.text.decode("utf-8")
            if name in func_map:
                replacements.append((node.start_byte, node.end_byte, func_map[name]))
            elif name in var_map:
                replacements.append((node.start_byte, node.end_byte, var_map[name]))

    for child in node.children:
        replace_names(child, replacements, func_map, var_map)


def print_code(item: dict) -> None:
    print("\n".join(item["dependencies"]))
    print("-" * 50)
    print(item["signature"])
    print("-" * 50)
    print(item["code"])
    print("\n" * 2)


def all_node_types(node: tree_sitter.Node, node_types: Set[str] = set()) -> Set[str]:
    node_types.add(node.type)

    for child in node.children:
        all_node_types(child, node_types)

    return node_types


def rewrite(code: str) -> str:
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
        #print the code
        print("#" * 50)
        print(f"Start rewriting item {i}:")
        print("\n" * 2)

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
        
        code = extract_and_modify_operators(code)
        code = move_line_up_after_arrow(code)
        parts = code.split("-" * 20)
        item["dependencies"] = parts[0].split('\n')
        item["signature"] = parts[1]
        item["code"] = parts[2]

        print_code(item)

        item["signature"] = postprocess(process(preprocess(item["signature"])))

        for j, dep in enumerate(item["dependencies"]):
            item["dependencies"][j] = postprocess(process(preprocess(dep)))

        code_lst = item["code"].split("\n")
        for k, line in enumerate(code_lst):
            code_lst[k] = postprocess(process(preprocess(line)))
        item["code"] = "\n".join(code_lst)

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
        
        print_code(item)
        

        root_node = get_root(code)
        assert "ERROR" not in all_node_types(
            root_node
        ), f"Error in the Process for item {i}"

        rewritten_code = rewrite(code)
        print(rewritten_code)

        root_node = get_root(rewritten_code)
        assert "ERROR" not in all_node_types(
            root_node
        ), f"Error in the Rewrite for item {i}"

        print("\n" * 2)

if __name__ == "__main__":
    fire.Fire(main)
