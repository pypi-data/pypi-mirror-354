from functools import cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .fields import FieldInfo

@cache
def import_cached_field_info() -> type['FieldInfo']:
    from .fields import FieldInfo

    return FieldInfo