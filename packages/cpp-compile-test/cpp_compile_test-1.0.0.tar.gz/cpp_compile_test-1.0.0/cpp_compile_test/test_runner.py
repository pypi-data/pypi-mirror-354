import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
from cpp_compile_test.compiler_settings.compiler_settings import CompilerSettings
from cpp_compile_test.compile_test import CompileTest
from cpp_compile_test.compile_source import compile_source


class TestRunner:
    def __init__(self, settings: CompilerSettings, source_file: str = "main.cpp"):
        self.settings = settings
        self.source_file = source_file
        self.results: Dict[str, bool] = {}  # test ID → pass/fail

    def run_tests(self, tests: List[CompileTest], max_workers: int = os.cpu_count()) -> None:
        """
        Executes all provided tests in parallel using a thread pool.

        Args:
            tests: List of CompileTest objects to run.
            max_workers: Max number of threads (default: number of CPU cores).
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_test = {
                executor.submit(compile_source, test, self.source_file, self.settings): test
                for test in tests
            }

            for future in as_completed(future_to_test):
                test = future_to_test[future]
                try:
                    success = future.result()
                except Exception as e:
                    print(f"[ERROR] Exception while compiling test '{test.id}': {e}")
                    success = False
                self.results[test.id] = success

    def summary(self):
        """
        Prints a basic pass/fail summary after test execution.
        """
        total = len(self.results)
        passed = sum(1 for result in self.results.values() if result)
        failed = total - passed

        print("\n========== Test Summary ==========")
        print(f"Total: {total}  Passed: {passed}  Failed: {failed}")
        print("==================================\n")
