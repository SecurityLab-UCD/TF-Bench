"""definition for general Synchronizer and LSPSynchronizer based on pylspclient"""
from code import compile_command
import pylspclient
import subprocess
import sys
import os
from pylspclient.lsp_structs import (
    Location,
    Position,
    Range,
    TextDocumentIdentifier,
)
from src.hs_parser import HASKELL_LANGUAGE
from src.lsp_sync.util import path2uri, replace_tabs, uri2path, ReadPipe
from src.lsp_sync.common import (
    CAPABILITIES,
    UNITSYNCER_HOME,
    RUST_CAPABILITIES,
    RUST_INIT_OPTIONS,
)
from typing import Optional, Union
from returns.maybe import Maybe, Nothing, Some
from returns.result import Result, Success, Failure
from returns.converters import maybe_to_result
import logging
from src.lsp_sync.util import silence
import json
from os.path import realpath
from src.hs_parser.ast_util import AST
from tree_sitter import Node

# Need to implement!
def haskell_get_def(node: Node, lineno: int):
    for child in node.children:
        if (
            child.type == "function"
            # AST is 1-indexed, LSP is 0-indexed
            and child.start_point[0] == lineno + 1
            # AST count from def, LSP count from function name
            # and child.col_offset == col_offset - 4
        ):
            return Some(child)
        result = haskell_get_def(child, lineno)
        if result != Nothing:
            return result

    return Nothing

def get_function_code(
    func_location: Location
) -> Maybe[tuple[str, str | None, str | None]]:
    """Extract the source code of a function from a Location LSP response

    Args:
        func_location (Location): location of function responded by LS
    Returns:
        Maybe[tuple[str, str | None, str | None]]: source code of function, its docstring, code_id
    """
    lineno = func_location.range.start.line
    col_offset = func_location.range.start.character  # pylint: disable=unused-variable

    def _get_function_code(file_path) -> Maybe[tuple[str, str | None, str | None]]:
        try:
            with open(file_path, "r", errors="replace") as file:
                code = file.read()
        except FileNotFoundError:
            return Nothing

        ast_util = AST(replace_tabs(code), HASKELL_LANGUAGE)
        tree = ast_util.tree
        return haskell_get_def(tree.root_node, lineno).map(
            lambda node: (
                ast_util.get_src_from_node(node),
                None,
                f"{file_path}::{ast_util.get_fn_name(node).unwrap()}",
            )
        )

    return uri2path(func_location.uri).bind(_get_function_code)

def get_lsp_cmd() -> Optional[list[str]]:
    return ["haskell-language-server-wrapper", "--lsp"]


class Synchronizer:
    """interface definition for all Synchronizer"""

    def __init__(self, workspace_dir: str, language: str) -> None:
        self.workspace_dir = os.path.abspath(workspace_dir)
        self.langID = language

    def initialize(self, timeout: int):
        raise NotImplementedError

    def get_source_of_call(
        self,
        focal_name: str,
        file_path: str,
        line: int,
        col: int,
        verbose: bool = False,
    ) -> Result[tuple[str, str | None, str | None], str]:
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError


class LSPSynchronizer(Synchronizer):
    """Synchronizer implementation based on pylspclient"""

    def __init__(self, workspace_dir: str, language: str) -> None:
        super().__init__(workspace_dir, language)

        self.root_uri = path2uri(self.workspace_dir)
        workspace_name = os.path.basename(self.workspace_dir)
        self.workspace_folders = [{"name": workspace_name, "uri": self.root_uri}]
        self.lsp_proc: subprocess.Popen
        self.lsp_client: pylspclient.LspClient

    @silence
    def start_lsp_server(self, timeout: int = 10):
        lsp_cmd = get_lsp_cmd()

        self.lsp_proc = subprocess.Popen(
            lsp_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        read_pipe = ReadPipe(self.lsp_proc.stderr)
        read_pipe.start()
        json_rpc_endpoint = pylspclient.JsonRpcEndpoint(
            self.lsp_proc.stdin, self.lsp_proc.stdout
        )
        lsp_endpoint = pylspclient.LspEndpoint(json_rpc_endpoint, timeout=timeout)
        self.lsp_client = pylspclient.LspClient(lsp_endpoint)

    @silence
    def initialize(self, timeout: int = 60):
        self.start_lsp_server(timeout)
        response = self.lsp_client.initialize(
            self.lsp_proc.pid,
            self.workspace_dir,
            self.root_uri,
            None,
            CAPABILITIES,
            "off",
            self.workspace_folders,
        )
        logging.debug(json.dumps(response))
        self.lsp_client.initialized()

    def open_file(self, file_path: str) -> str:
        """send a file to LSP server

        Args:
            file_path (str): absolute path to the file

        Returns:
            str: uri of the opened file
        """
        uri = path2uri(file_path)
        with open(file_path, "r", errors="replace") as f:
            text = replace_tabs(f.read())
        version = 1
        self.lsp_client.didOpen(
            pylspclient.lsp_structs.TextDocumentItem(uri, self.langID, version, text)
        )
        return uri

    def get_source_of_call(
        self,
        focal_name: str,
        file_path: str,
        line: int,
        col: int,
        verbose: bool = False,
    ) -> Result[tuple[str, str | None, str | None], str]:
        """get the source code of a function called at a specific location in a file

        Args:
            file_path (str): absolute path to file that contains the call
            line (int): line number of the call, 0-indexed
            col (int): column number of the call, 0-indexed

        Returns:
            Maybe[tuple[str, str | None]]: the source code and docstring of the called function
        """
        try:
            uri = self.open_file(file_path)
        except Exception as e:  # pylint: disable=broad-exception-caught
            return Failure(str(e))

        try:
            goto_def = self.lsp_client.definition
            if not verbose:
                goto_def = silence(goto_def)

            response = goto_def(
                TextDocumentIdentifier(uri),
                Position(line, col),
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            return Failure(str(e))

        def_location: Location
        match response:
            case None | []:
                return Failure(f"No definition found: {response}")
            case [loc, *_]:
                def_location = loc
            case loc:
                if isinstance(loc, Location):
                    def_location = loc
                else:
                    return Failure(f"Unexpected response from LSP server: {loc}")

        file_path = uri2path(def_location.uri).value_or(str(def_location.uri))
        logging.debug(file_path)

        # check if file path is relative to workspace root
        if not (
            file_path.startswith(self.workspace_dir)
            or file_path.startswith(realpath(self.workspace_dir))
        ):
            return Failure(f"Source code not in workspace: {file_path}")

        def not_found_error(_):
            lineno = def_location.range.start.line
            col_offset = def_location.range.start.character
            return f"Source code not found: {file_path}:{lineno}:{col_offset}"

        return (
            # Need to edit get_function_code here WORK_IN_PROGRESS
            maybe_to_result(get_function_code(def_location))
            .alt(not_found_error)
            .bind(lambda t: Failure("Empty Source Code") if t[0] == "" else Success(t))
        )

    def stop(self):
        self.lsp_client.shutdown()
        self.lsp_client.exit()
        self.lsp_proc.kill()


def main():
    workspace_dir = os.path.abspath("data/repos/haskell_example/")
    test_file = os.path.join(workspace_dir, "main.hs")
    func_loc = (6, 15)

    sync = LSPSynchronizer(workspace_dir, "hs")
    sync.initialize()

    print(sync.get_source_of_call("", test_file, *func_loc))

    sync.stop()


if __name__ == "__main__":
    main()