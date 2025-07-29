"""Arguments Utility Functions for Declarative Typed Argument Parsing.

The `arguments` module contains utility functions used for formatting argument
names and formatting argument descriptions.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from argparse_dantic import FieldInfo


def names(field: "FieldInfo", invert: bool = False) -> list[str]:
    """Standardises the argument name and any custom aliases.

    Args:
        field (FieldInfo): Field to construct name for.
        invert (bool): Whether to invert the name by prepending `--no-`.

    Returns:
        list[str]: Standardised names for the argument.
    """
    # Add any custom aliases first
    # We trust that the user has provided these correctly
    flags: list[str] = []
    flags.extend(field.aliases)

    # Construct prefix, prepend it, replace '_' with '-'
    prefix = "--no-" if invert else "--"
    flags.append(f"{prefix}{field.alias.replace('_', '-')}")

    # Return the standardised name and aliases
    return flags

def names_command(field: "FieldInfo") -> list[str]:
    """Standardises the command name and any custom aliases.

    Args:
        field (FieldInfo): Field to construct name for.

    Returns:
        list[str]: Standardised names for the command.
    """
    # Add any custom aliases first
    # We trust that the user has provided these correctly
    flags: list[str] = []
    flags.extend(field.aliases)

    flags.append(field.alias)
    return flags

def description(field: "FieldInfo") -> str:
    """Standardises argument description.

    Args:
        field (FieldInfo): Field to construct description for.

    Returns:
        str: Standardised description of the argument.
    """
    # Construct Default String
    default = f"(default: {field.get_default()})" if not field.required else None

    # Return Standardised Description String
    return " ".join(filter(None, [field.description, default]))
