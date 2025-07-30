# cpp-compile-test

A fast, scriptable tool for **compile-time testing of C++ code**.  
Designed to parse C++ header files for test case definitions, and validate that each one **does or does not compile**, based on expected behavior.

This tool is particularly useful for:
- Libraries with SFINAE/constraint-based logic
- Metaprogramming-heavy APIs
- Validating invalid/ill-formed usage
- Compile-time regression testing

---

## Features

- Parses test structs using Tree-sitter C++ grammar
- Extracts test metadata via static constexpr fields
- Supports expected **compile** or **failure** behaviors
- Runs tests **in parallel** for fast execution
- Customizable compiler settings via JSON or CLI
- Supports `cl`, `gcc`, `clang`, or any custom compiler
- First-class support for **MSVC**, including pre-launch PowerShell script

---

## Installation

From PyPI:

```bash
pip install cpp-compile-test
```

---

## Usage

### Basic CLI Example

```bash
cpp-compile-test --config msvc_settings.json --header my_tests.hpp --source main.cpp
```

- `--config`: Path to a JSON file with compiler settings
- `--header`: Header file containing test case structs
- `--source`: Source file used for actual test compilation (should reference the test struct)

### Example Test Struct (in C++)

```cpp
struct simple_cast_test {
   static constexpr const char* id = "simple_cast";
   static constexpr bool expect_error = false;
   static constexpr const char* description = "Cast a length to a base_dimension length";

   template<typename = void>
   static void run() {
      Length<Meters> myLength{10.0};
      BaseDimension<UnitExponent<Meters>> other = myLength;
   }
};
```

### Example `msvc_settings.json`

```json
{
  "compiler": "cl",
  "compiler_type": "cl",
  "flags": [
    "/std:c++20",
    "/nologo",
    "/c",
    "/EHsc",
    "/Ipath\to\headers"
  ]
}
```

---

## Testing

To run unit tests:

```bash
pytest
```

---

## Development

### Regenerate model from JSON schema

```bash
python scripts/generate_schema_models.py
```

Make sure to install:

```bash
pip install datamodel-code-generator
```

### Setting up MSVC environment (PowerShell)

```powershell
.\scripts\setup_msvc_env.ps1
```

---

## Roadmap

- [ ] GitLab CI pipeline (build, lint, test)
- [ ] Pylint / Ruff integration
- [ ] Automated schema-to-model regeneration
- [ ] PyPI publishing from GitLab pipeline

---

## Contributing

Contributions welcome! Submit issues, PRs, or feature requests.

---

## License

[Apache 2.0 License](./LICENSE)
