"""Parses Standard Pydantic Fields to Command-Line Arguments.

The `standard` module contains the `parse_field` function, which parses
standard `pydantic` model fields to `ArgumentParser` command-line arguments.

Unlike the other `parser` modules, the `standard` module does not contain a
`should_parse` function. This is because it is the fallback case, where fields
that do not match any other types and require no special handling are parsed.
"""

from argparse_dantic import utils
from argparse_dantic._argparse import actions

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from argparse_dantic import ArgumentParser, FieldInfo


def parse_field(
    parser: "ArgumentParser",
    field: "FieldInfo",
) -> Optional[utils.pydantic.PydanticValidator]:
    """Adds standard pydantic field to argument parser.

    Args:
        parser (actions.ArgumentParser): Argument parser to add to.
        field (FieldInfo): Field to be added to parser.

    Returns:
        Optional[utils.pydantic.PydanticValidator]: Possible validator method.
    """
    # Add Standard Field
    parser.add_argument(
        *utils.arguments.names(field),
        action=actions._StoreAction,
        help=field.help or utils.arguments.description(field),
        dest=field.alias,
        metavar=field.alias.upper(),
        required=bool(field.required),
        model=field
    )

    # Construct and Return Validator
    return utils.pydantic.as_validator(field, lambda v: v)
