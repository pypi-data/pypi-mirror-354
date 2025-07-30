#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

def main():
    schema_path = Path("compiler_settings_schema.json")
    output_path = Path("compiler_settings.py")

    if not schema_path.exists():
        print(f"[ERROR] Schema file not found: {schema_path}")
        sys.exit(1)

    cmd = [
        "datamodel-codegen",
        "--input", str(schema_path),
        "--input-file-type", "jsonschema",
        "--output", str(output_path),
        "--output-model-type", "pydantic_v2.BaseModel"
    ]

    print(f"[INFO] Generating model from schema...")
    try:
        subprocess.run(cmd, check=True)
        print(f"[SUCCESS] Model written to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] datamodel-codegen failed with exit code {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
