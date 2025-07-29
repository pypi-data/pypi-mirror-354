"""Parses Container Pydantic Fields to Command-Line Arguments.

The `container` module contains the `should_parse` function, which checks
whether this module should be used to parse the field, as well as the
`parse_field` function, which parses container `pydantic` model fields to
`ArgumentParser` command-line arguments.
"""


import enum
import argparse
import collections.abc
from typing import Optional, TYPE_CHECKING

from argparse_dantic import utils
from argparse_dantic._argparse import actions


if TYPE_CHECKING:
    from argparse_dantic import ArgumentParser, FieldInfo


def should_parse(field: "FieldInfo") -> bool:
    """Checks whether the field should be parsed as a `container`.

    Args:
        field (FieldInfo): Field to check.

    Returns:
        bool: Whether the field should be parsed as a `container`.
    """
    # Check and Return
    return utils.types.is_field_a(field, collections.abc.Container) and not utils.types.is_field_a(
        field, (collections.abc.Mapping, enum.Enum, str, bytes)
    )


def parse_field(
    parser: "ArgumentParser",
    field: "FieldInfo",
) -> Optional[utils.pydantic.PydanticValidator]:
    """Adds container pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (FieldInfo): Field to be added to parser.

    Returns:
        Optional[utils.pydantic.PydanticValidator]: Possible validator method.
    """
    # Add Container Field
    parser.add_argument(
        *utils.arguments.names(field),
        action=actions._StoreAction,
        nargs=argparse.ONE_OR_MORE,
        help=field.help or utils.arguments.description(field),
        dest=field.alias,
        metavar=field.alias.upper(),
        required=bool(field.required),
        model=field
    )

    # Construct and Return Validator
    return utils.pydantic.as_validator(field, lambda v: v)
