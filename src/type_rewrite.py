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
        #a special case when the infix operator is .
        if operator == ".":
            pattern = r"(?<=\s|\()(\.)(?=\s|\))"
            input_string = re.sub(pattern, double_letters[ord('.') % 26], input_string)
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

    lst = line.split()
    for i, elem in enumerate(lst):
        #the first letter of a function cannot be capitalized
        if elem[0].isupper() and '"' not in elem:
            lst[i] = elem.lower() + "#"
        #the first letter of a function cannot be ":"
        elif elem[0] == ":" and len(elem) > 1 and elem[1] != ":":
            lst[i] = double_letters[(ord(elem[0]) + ord(elem[1])) % 26]
        
        #for items such as List.foldl
        pattern = r'\b\w+\.\w+\b'
        lst[i] = re.sub(pattern, double_letters[sum([ord(l) for l in lst[i]]) % 26], lst[i])

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
    #remove ()
    line = re.sub(r"\((\w)\1\)", r"\1\1", line)

    return line


def get_names(
    node: tree_sitter.Node, func_names: set[str] = set(), var_names: set[str] = set()
) -> tuple[set[str], set[str]]:
    """
    Recursively traverse the syntax tree to collect function and variable names using pattern matching.
    """
    match node.type:
        case "function" | "signature":
            if func_name := node.child_by_field_name("name"):
                func_names.add(func_name.text.decode("utf-8"))
        case "apply":
            if func_name := (node.children[0] if node.children else None):
                func_names.add(func_name.text.decode("utf-8"))
        case "operator" | "variable":
            var_or_func_name = node.text.decode("utf-8")
            if node.type == "operator":
                func_names.add(var_or_func_name)
            elif node.type == "variable":
                var_names.add(var_or_func_name)

    for child in node.children:
        get_names(child, func_names, var_names)

    return func_names, var_names


def replace_names(
    node: tree_sitter.Node,
    func_map: dict,
    var_map: dict,
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

    if node.type in ["variable", "constructor", "operator"]:
        if node.text is not None:
            name = node.text.decode("utf-8")
            if name in func_map:
                replacements.append((node.start_byte, node.end_byte, func_map[name]))
            elif name in var_map:
                replacements.append((node.start_byte, node.end_byte, var_map[name]))

    for child in node.children:
        replacements.extend(replace_names(child, func_map, var_map))

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
    """
    Rewrite the Haskell code by replacing function and variable names with standardized names.

    Args:
        code (str): The original Haskell code as a string.

    Returns:
        str: The rewritten Haskell code with standardized names.
    """
    lang = Language(tree_sitter_haskell.language())
    root_node = AST(code, lang).root

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

    # Directly get the replacements list from replace_names
    replacements = replace_names(root_node, func_map, var_map)
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
        if not ast.is_valid_code():
            wrong_item.append(i)

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

    print("ERROR while processing items:")
    print(set(wrong_item))

if __name__ == "__main__":
    fire.Fire(main)
