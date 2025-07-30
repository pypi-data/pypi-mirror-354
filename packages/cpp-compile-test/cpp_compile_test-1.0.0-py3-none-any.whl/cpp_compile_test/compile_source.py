from __future__ import annotations

import subprocess
from cpp_compile_test.compiler_settings.compiler_settings import CompilerSettings
from cpp_compile_test.compile_test import CompileTest


def compile_source(test: CompileTest, source: str, settings: CompilerSettings) -> bool:
    """
    Compiles a single test struct using the configured compiler.

    Args:
        test: The CompileTest instance representing the test case.
        source: Path to the source file (e.g., main.cpp).
        settings: CompilerSettings object with compiler and flags.

    Returns:
        True if the compiler behavior matched the expected result; False otherwise.
    """
    struct_name = test.struct_name
    result = subprocess.run(
        [
            settings.compiler,
            str(source),
            "/D", f"TEST_STRUCT_NAME={struct_name}",
            *settings.flags
        ],
        capture_output=True,
        env=None  # Use external environment only
    )

    success = result.returncode == 0
    expected = test.expect_compile

    if success == expected:
        print(f"[PASS] {test.id}: {test.description}")
    else:
        print(f"[FAIL] {test.id}: {test.description} (expected {'compile' if expected else 'failure'})")
        if success:
            print("  [Unexpected Compile]")
        else:
            print("  [Unexpected Error Output]")
            print("  --- Compiler STDOUT ---")
            print(result.stdout.decode(errors="replace"))
            print("  --- Compiler STDERR ---")
            print(result.stderr.decode(errors="replace"))
            print("  ------------------------")

    return success == expected
