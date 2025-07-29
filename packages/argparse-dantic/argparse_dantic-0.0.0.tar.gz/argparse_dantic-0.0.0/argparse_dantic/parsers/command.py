"""Parses Nested Pydantic Model Fields to Sub-Commands.

The `command` module contains the `should_parse` function, which checks whether
this module should be used to parse the field, as well as the `parse_field`
function, which parses nested `pydantic` model fields to `ArgumentParser`
sub-commands.
"""

import pydantic
from typing import Optional, TYPE_CHECKING

from argparse_dantic import utils
from argparse_dantic._argparse import actions

if TYPE_CHECKING:
    from argparse_dantic import FieldInfo
    from rich.console import Console


def should_parse(field: "FieldInfo") -> bool:
    """Checks whether the field should be parsed as a `command`.

    Args:
        field (FieldInfo): Field to check.

    Returns:
        bool: Whether the field should be parsed as a `command`.
    """
    # Check and Return
    return utils.types.is_field_a(field, pydantic.BaseModel)


def parse_field(
    subparser: actions._SubParsersAction,
    field: "FieldInfo",
    console: "Console"
) -> Optional[utils.pydantic.PydanticValidator]:
    """Adds command pydantic field to argument parser.

    Args:
        subparser (actions._SubParsersAction): Sub-parser to add to.
        field (FieldInfo): Field to be added to parser.

    Returns:
        Optional[utils.pydantic.PydanticValidator]: Possible validator method.
    """
    # Add Command
    subparser.add_parser(
        field.alias,
        dest=field.alias,
        aliases=field.aliases,
        prog=field.prog,
        usage=field.usage,
        epilog=field.epilog,
        help=field.help,
        description=field.description,
        model_class=utils.types.get_field_type(field),
        prefix_chars=field.prefix_chars,
        exit_on_error=False,  # Allow top level parser to handle exiting 
        console=console,
    )
