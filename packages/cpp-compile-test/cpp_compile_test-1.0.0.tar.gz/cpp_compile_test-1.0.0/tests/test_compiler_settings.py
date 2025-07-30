import pytest
from cpp_compile_test.compiler_settings.compiler_settings import CompilerSettings, CompilerType

def test_compiler_settings_parse():
    data = {
        "compiler": "cl",
        "compiler_type": "cl",
        "flags": ["/std:c++20", "/nologo", "/c"]
    }

    settings = CompilerSettings.model_validate(data)

    assert settings.compiler == "cl"
    assert settings.compiler_type == CompilerType.cl
    assert settings.flags == ["/std:c++20", "/nologo", "/c"]
