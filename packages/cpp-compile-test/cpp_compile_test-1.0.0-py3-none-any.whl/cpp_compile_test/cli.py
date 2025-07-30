# cpp_compile_test/cli.py

import argparse
import json
from cpp_compile_test.compiler_settings.compiler_settings import CompilerSettings
from cpp_compile_test.test_discovery import discover_tests
from cpp_compile_test.test_runner import TestRunner

import os
def parse_args():
    parser = argparse.ArgumentParser(description="Run compile-time tests on C++ headers")
    parser.add_argument("--config", type=str, help="Path to JSON config file with compiler settings")
    parser.add_argument("--compiler", type=str, help="Override: path to compiler executable")
    parser.add_argument("--compiler-type", type=str, choices=["cl", "gcc", "clang", "other"], help="Override: compiler type")
    parser.add_argument("--flag", action="append", help="Override: additional compiler flag (repeatable)")

    parser.add_argument("--header", required=True, help="C++ header to parse for compile tests")
    parser.add_argument("--source", default="main.cpp", help="C++ source file that includes the test struct")
    parser.add_argument("--max-workers", type=int, default=None, help="Max parallel compiler invocations (defaults to CPU count)")

    return parser.parse_args()


def main():
    args = parse_args()

    
    print(f"[DEBUG] INCLUDE: {os.environ.get('INCLUDE')}")

    # Load config from JSON if provided
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config_dict = json.load(f)
        settings = CompilerSettings.model_validate(config_dict)
    else:
        settings = CompilerSettings.model_construct(compiler="g++", compiler_type="gcc", flags=[])

    # Apply CLI overrides
    if args.compiler:
        settings.compiler = args.compiler
    if args.compiler_type:
        settings.compiler_type = args.compiler_type
    if args.flag:
        settings.flags.extend(args.flag)

    # === Discover Tests ===
    print(f"Discovering tests from header: {args.header}")
    tests = discover_tests(args.header)
    print(f"Discovered {len(tests)} tests.\n")

    # === Run Tests ===
    runner = TestRunner(settings, source_file=args.source)
    runner.run_tests(tests, max_workers=args.max_workers)
    runner.summary()


if __name__ == "__main__":
    main()
