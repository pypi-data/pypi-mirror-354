from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
from tree_sitter import Node


@dataclass(slots=True)
class CompileTest:
    """
    Represents a single compile-time test case with associated metadata.
    Each test corresponds to a C++ struct definition containing specific static fields.
    """
    id: str
    expect_compile: bool
    description: str
    struct_name: str

    @classmethod
    def from_node(cls, node: Node) -> CompileTest:
        """
        Constructs a CompileTest instance from a Tree-sitter AST node.

        Args:
            node: A Tree-sitter node representing a C++ struct.

        Returns:
            A CompileTest instance populated from metadata fields.
        """
        metadata = cls._extract_metadata(node)
        cls._validate_metadata(metadata)
        struct_name = node.child_by_field_name("name").text.decode()
        return cls(
            id=metadata["id"],
            expect_compile=metadata["expect_error"].lower() != "true",
            description=metadata["description"],
            struct_name=struct_name,
        )

    @staticmethod
    def _extract_metadata(node: Node) -> Dict[str, str]:
        """
        Extracts metadata fields from the body of a struct.

        Args:
            node: A Tree-sitter node representing the struct.

        Returns:
            A dictionary containing key-value pairs for metadata fields.
        """
        metadata = {}
        body = node.child_by_field_name("body")
        if body is None:
            return metadata

        for field in body.named_children:
            if field.type != "field_declaration":
                continue

            declarator = field.child_by_field_name("declarator")
            value_node = field.child_by_field_name("default_value")
            if not declarator or not value_node:
                continue

            key = CompileTest._parse_metadata_field(declarator.text.decode())
            value = value_node.text.decode().strip('"')
            metadata[key] = value
        return metadata

    @staticmethod
    def _parse_metadata_field(field_name: str) -> str:
        """
        Normalizes field names by removing pointer indicators or spacing.

        Args:
            field_name: The raw field name string from the AST.

        Returns:
            A cleaned metadata key.
        """
        return field_name.lstrip("* ")

    @staticmethod
    def _validate_metadata(metadata: Dict[str, str]) -> None:
        """
        Validates that all required metadata fields are present.

        Args:
            metadata: Dictionary of extracted metadata.

        Raises:
            ValueError: If any required field is missing.
        """
        required_keys = ["id", "expect_error", "description"]
        missing = [key for key in required_keys if key not in metadata]
        if missing:
            raise ValueError(f"Missing required metadata: {missing}")
