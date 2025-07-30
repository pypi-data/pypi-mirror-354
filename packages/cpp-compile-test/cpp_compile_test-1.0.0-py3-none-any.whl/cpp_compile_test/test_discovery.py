from tree_sitter import Tree
from cpp_compile_test.compiler_settings.compiler_settings import CompilerSettings
from cpp_compile_test.compile_test import CompileTest
from typing import List
from tree_sitter import Language, Parser
import tree_sitter_cpp as tscpp


def parse_header(filename: str) -> Tree:
    CPP_LANGUAGE = Language(tscpp.language())
    parser = Parser(CPP_LANGUAGE)
    with open(filename, 'rb') as f:
        code = f.read()
    return parser.parse(code)


def discover_tests(header_path: str) -> List[CompileTest]:
    """
    Parses a C++ header and returns all discovered CompileTest structs.
    """
    tree = parse_header(header_path)
    return find_tests(tree)


def find_tests(tree: Tree) -> List[CompileTest]:
    """
    Recursively walks the AST looking for test structs.
    """
    def walk(node):
        found = []
        if node.type == "struct_specifier":
            try:
                found.append(CompileTest.from_node(node))
            except Exception as e:
                print(f"Warning: {e}")
        for child in node.children:
            found.extend(walk(child))
        return found

    return walk(tree.root_node)
