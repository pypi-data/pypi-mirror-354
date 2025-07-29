"""Parses Mapping Pydantic Fields to Command-Line Arguments.

The `mapping` module contains the `should_parse` function, which checks whether
this module should be used to parse the field, as well as the `parse_field`
function, which parses mapping `pydantic` model fields to `ArgumentParser`
command-line arguments.
"""

import ast
import collections.abc

from argparse_dantic import utils
from argparse_dantic._argparse import actions

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from argparse_dantic import ArgumentParser, FieldInfo


def should_parse(field: "FieldInfo") -> bool:
    """Checks whether the field should be parsed as a `mapping`.

    Args:
        field (FieldInfo): Field to check.

    Returns:
        bool: Whether the field should be parsed as a `mapping`.
    """
    # Check and Return
    return utils.types.is_field_a(field, collections.abc.Mapping)


def parse_field(
    parser: "ArgumentParser",
    field: "FieldInfo",
) -> Optional[utils.pydantic.PydanticValidator]:
    """Adds mapping pydantic field to argument parser.

    Args:
        parser (actions.ArgumentParser): Argument parser to add to.
        field (FieldInfo): Field to be added to parser.

    Returns:
        Optional[utils.pydantic.PydanticValidator]: Possible validator method.
    """
    # Add Mapping Field
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
    return utils.pydantic.as_validator(field, ast.literal_eval)
