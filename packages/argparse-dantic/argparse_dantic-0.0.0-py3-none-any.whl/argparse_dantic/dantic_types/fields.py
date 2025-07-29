import sys
import typing
import annotated_types
import dataclasses

from warnings import warn
from typing import Any, Callable, Literal
from typing_extensions import TypeAlias, Unpack, deprecated
from typing_inspection import typing_objects
from pydantic_core import PydanticUndefined
from pydantic.fields import FieldInfo as PydanticFieldInfo, _EmptyKwargs, _FIELD_ARG_NAMES, _Unset
from typing_inspection.introspection import UNKNOWN, AnnotationSource, ForbiddenQualifier, inspect_annotation

from pydantic import types
from pydantic.aliases import AliasChoices, AliasPath
from pydantic.config import JsonDict
from pydantic.errors import PydanticForbiddenQualifier, PydanticUserError
from pydantic.json_schema import PydanticJsonSchemaWarning


if sys.version_info >= (3, 13):
    import warnings

    Deprecated: TypeAlias = warnings.deprecated | deprecated
else:
    Deprecated: TypeAlias = deprecated


class FieldInfo(PydanticFieldInfo):
    def __init__(self, default: typing.Any = _Unset, **kwargs):
        help =          kwargs.pop('help', None)
        required =      kwargs.pop('required', False)
        allow_none =    kwargs.pop('allow_none', False)
        aliases =       kwargs.pop('aliases', [])
        prog =          kwargs.pop('prog', None)
        usage =         kwargs.pop('usage', None)
        description =   kwargs.pop('description', None)
        epilog =        kwargs.pop('epilog', None)
        prefix_chars =  kwargs.pop('prefix_chars', "-")
        add_help =      kwargs.pop('add_help', True)
        exit_on_error = kwargs.pop('exit_on_error', False)
        version =       kwargs.pop('version', None)

        global_ =       kwargs.pop('global_', False)

        required = required if required is not _Unset else False
        if not required and default is _Unset:
            # If the required is False, we want to set default to None, not _Unset.
            # That new pydantic will not raise missing value error.
            default = None
        
        super().__init__(default=default, **kwargs)
        self.global_:                     bool = global_
        self.help:        typing.Optional[str] = help if help is not _Unset else None
        self.required:                    bool = required
        self.allow_none:                  bool = allow_none if allow_none is not _Unset else (default is None or default is _Unset)
        self.aliases:                list[str] = aliases
        self.prog:        typing.Optional[str] = prog if prog is not _Unset else None
        self.usage:       typing.Optional[str] = usage if usage is not _Unset else None
        self.description: typing.Optional[str] = description if description is not _Unset else None
        self.epilog:      typing.Optional[str] = epilog if epilog is not _Unset else None
        self.prefix_chars:                str  = prefix_chars
        self.add_help:                    bool = add_help if add_help is not _Unset else None
        self.exit_on_error:               bool = exit_on_error if exit_on_error is not _Unset else None
        self.version:     typing.Optional[str] = version if version is not _Unset else None
    
    @classmethod
    def from_field(cls, default: typing.Any = _Unset, **kwargs) -> "FieldInfo":
        if 'annotation' in kwargs:
            raise TypeError('"annotation" is not permitted as a Field keyword argument')
        return cls(default=default, **kwargs)

    @classmethod
    def from_annotation(
        cls, 
        annotation: typing.Any, 
        *, _source: AnnotationSource = AnnotationSource.ANY,
        **kwargs,
    ) -> "FieldInfo":
        try:
            inspected_ann = inspect_annotation(
                annotation,
                annotation_source=_source,
                unpack_type_aliases='skip',
            )
        except ForbiddenQualifier as e:
            raise PydanticForbiddenQualifier(e.qualifier, annotation)

        # TODO check for classvar and error?

        # No assigned value, this happens when using a bare `Final` qualifier (also for other
        # qualifiers, but they shouldn't appear here). In this case we infer the type as `Any`
        # because we don't have any assigned value.
        type_expr: Any = Any if inspected_ann.type is UNKNOWN else inspected_ann.type
        final = 'final' in inspected_ann.qualifiers
        metadata = inspected_ann.metadata

        if not metadata:
            # No metadata, e.g. `field: int`, or `field: Final[str]`:
            field_info = cls(annotation=type_expr, frozen=final or None, **kwargs)
            field_info._qualifiers = inspected_ann.qualifiers
            return field_info

        # With metadata, e.g. `field: Annotated[int, Field(...), Gt(1)]`:
        field_info_annotations = [a for a in metadata if isinstance(a, FieldInfo)]
        field_info = cls.merge_field_infos(*field_info_annotations, annotation=type_expr, **kwargs)

        new_field_info = field_info._copy()
        new_field_info.annotation = type_expr
        new_field_info.frozen = final or field_info.frozen
        field_metadata: list[Any] = []
        for a in metadata:
            if typing_objects.is_deprecated(a):
                new_field_info.deprecated = a.message
            elif not isinstance(a, FieldInfo):
                field_metadata.append(a)
            else:
                field_metadata.extend(a.metadata)
            new_field_info.metadata = field_metadata
        new_field_info._qualifiers = inspected_ann.qualifiers
        return new_field_info
    
    @classmethod
    def from_annotated_attribute(
        cls, 
        annotation: type[typing.Any], 
        default: typing.Any, *, 
        _source: AnnotationSource = AnnotationSource.ANY,
        **kwargs,
    ) -> "FieldInfo":
        if annotation is default:
            raise PydanticUserError(
                'Error when building FieldInfo from annotated attribute. '
                "Make sure you don't have any field name clashing with a type annotation.",
                code='unevaluable-type-annotation',
            )

        try:
            inspected_ann = inspect_annotation(
                annotation,
                annotation_source=_source,
                unpack_type_aliases='skip',
            )
        except ForbiddenQualifier as e:
            raise PydanticForbiddenQualifier(e.qualifier, annotation)

        # TODO check for classvar and error?

        # TODO infer from the default, this can be done in v3 once we treat final fields with
        # a default as proper fields and not class variables:
        type_expr: Any = Any if inspected_ann.type is UNKNOWN else inspected_ann.type
        final = 'final' in inspected_ann.qualifiers
        metadata = inspected_ann.metadata

        if isinstance(default, cls):
            # e.g. `field: int = Field(...)`
            default.annotation = type_expr
            default.metadata += metadata
            merged_default = cls.merge_field_infos(
                *[x for x in metadata if isinstance(x, cls)],
                default,
                annotation=default.annotation,
                **kwargs
            )
            merged_default.frozen = final or merged_default.frozen
            merged_default._qualifiers = inspected_ann.qualifiers
            return merged_default

        if isinstance(default, dataclasses.Field):
            # `collect_dataclass_fields()` passes the dataclass Field as a default.
            pydantic_field = cls._from_dataclass_field(default, **kwargs)
            pydantic_field.annotation = type_expr
            pydantic_field.metadata += metadata
            pydantic_field = cls.merge_field_infos(
                *[x for x in metadata if isinstance(x, cls)],
                pydantic_field,
                annotation=pydantic_field.annotation,
                **kwargs
            )
            pydantic_field.frozen = final or pydantic_field.frozen
            pydantic_field.init_var = 'init_var' in inspected_ann.qualifiers
            pydantic_field.init = getattr(default, 'init', None)
            pydantic_field.kw_only = getattr(default, 'kw_only', None)
            pydantic_field._qualifiers = inspected_ann.qualifiers
            return pydantic_field

        if not metadata:
            # No metadata, e.g. `field: int = ...`, or `field: Final[str] = ...`:
            field_info = cls(annotation=type_expr, default=default, frozen=final or None, **kwargs)
            field_info._qualifiers = inspected_ann.qualifiers
            return field_info

        # With metadata, e.g. `field: Annotated[int, Field(...), Gt(1)] = ...`:
        field_infos = [a for a in metadata if isinstance(a, cls)]
        field_info = cls.merge_field_infos(*field_infos, annotation=type_expr, default=default, **kwargs)
        field_metadata: list[Any] = []
        for a in metadata:
            if typing_objects.is_deprecated(a):
                field_info.deprecated = a.message
            elif not isinstance(a, cls):
                field_metadata.append(a)
            else:
                field_metadata.extend(a.metadata)
        field_info.metadata = field_metadata
        field_info._qualifiers = inspected_ann.qualifiers
        return field_info
    
    @classmethod
    def merge_field_infos(cls, *field_infos: "FieldInfo", **overrides: typing.Any) -> "FieldInfo":
        if len(field_infos) == 1:
            # No merging necessary, but we still need to make a copy and apply the overrides
            field_info = field_infos[0]._copy()
            field_info._attributes_set.update(overrides)

            default_override = overrides.pop('default', PydanticUndefined)
            if default_override is Ellipsis:
                default_override = PydanticUndefined
            if default_override is not PydanticUndefined:
                field_info.default = default_override

            for k, v in overrides.items():
                setattr(field_info, k, v)
            return field_info  # type: ignore

        merged_field_info_kwargs: dict[str, Any] = {}
        metadata = {}
        for field_info in field_infos:
            attributes_set = field_info._attributes_set.copy()

            try:
                json_schema_extra = attributes_set.pop('json_schema_extra')
                existing_json_schema_extra = merged_field_info_kwargs.get('json_schema_extra')

                if existing_json_schema_extra is None:
                    merged_field_info_kwargs['json_schema_extra'] = json_schema_extra
                if isinstance(existing_json_schema_extra, dict):
                    if isinstance(json_schema_extra, dict):
                        merged_field_info_kwargs['json_schema_extra'] = {
                            **existing_json_schema_extra,
                            **json_schema_extra,
                        }
                    if callable(json_schema_extra):
                        warn(
                            'Composing `dict` and `callable` type `json_schema_extra` is not supported.'
                            'The `callable` type is being ignored.'
                            "If you'd like support for this behavior, please open an issue on pydantic.",
                            PydanticJsonSchemaWarning,
                        )
                elif callable(json_schema_extra):
                    # if ever there's a case of a callable, we'll just keep the last json schema extra spec
                    merged_field_info_kwargs['json_schema_extra'] = json_schema_extra
            except KeyError:
                pass

            # later FieldInfo instances override everything except json_schema_extra from earlier FieldInfo instances
            merged_field_info_kwargs.update(attributes_set)

            for x in field_info.metadata:
                if not isinstance(x, cls):
                    metadata[type(x)] = x

        merged_field_info_kwargs.update(overrides)
        field_info = cls(**merged_field_info_kwargs)
        field_info.metadata = list(metadata.values())
        return field_info
    
    @classmethod
    def _from_dataclass_field(cls, dc_field: dataclasses.Field[typing.Any], **kwargs) -> "FieldInfo":
        default = dc_field.default
        if default is dataclasses.MISSING:
            default = _Unset

        if dc_field.default_factory is dataclasses.MISSING:
            default_factory = _Unset
        else:
            default_factory = dc_field.default_factory

        # use the `Field` function so in correct kwargs raise the correct `TypeError`
        dc_field_metadata = {k: v for k, v in dc_field.metadata.items() if k in _FIELD_ARG_NAMES}
        return Field(default=default, default_factory=default_factory, repr=dc_field.repr, **dc_field_metadata, **kwargs)  # pyright: ignore[reportCallIssue]


@typing.overload
def Field(
    default: Any = PydanticUndefined,
    *,
    default_factory: Callable[[], Any] | Callable[[dict[str, Any]], Any] | None = _Unset,
    alias: str | None = _Unset,
    alias_priority: int | None = _Unset,
    validation_alias: str | AliasPath | AliasChoices | None = _Unset,
    serialization_alias: str | None = _Unset,
    title: str | None = _Unset,
    field_title_generator: Callable[[str, FieldInfo], str] | None = _Unset,
    description: str | None = _Unset,
    examples: list[Any] | None = _Unset,
    exclude: bool | None = _Unset,
    discriminator: str | types.Discriminator | None = _Unset,
    deprecated: Deprecated | str | bool | None = _Unset,
    json_schema_extra: JsonDict | Callable[[JsonDict], None] | None = _Unset,
    frozen: bool | None = _Unset,
    validate_default: bool | None = _Unset,
    repr: bool = _Unset,
    init: bool | None = _Unset,
    init_var: bool | None = _Unset,
    kw_only: bool | None = _Unset,
    pattern: str | typing.Pattern[str] | None = _Unset,
    strict: bool | None = _Unset,
    coerce_numbers_to_str: bool | None = _Unset,
    gt: annotated_types.SupportsGt | None = _Unset,
    ge: annotated_types.SupportsGe | None = _Unset,
    lt: annotated_types.SupportsLt | None = _Unset,
    le: annotated_types.SupportsLe | None = _Unset,
    multiple_of: float | None = _Unset,
    allow_inf_nan: bool | None = _Unset,
    max_digits: int | None = _Unset,
    decimal_places: int | None = _Unset,
    min_length: int | None = _Unset,
    max_length: int | None = _Unset,
    union_mode: Literal['smart', 'left_to_right'] = _Unset,
    fail_fast: bool | None = _Unset,

    global_: bool | None = _Unset,
    
    required: bool = _Unset,
    help: typing.Optional[str] = None,
    aliases: typing.Optional[list] = None,
    version: typing.Optional[str] = None,
) -> typing.Any:
    ...

def Field(  # noqa: C901
    default: Any = PydanticUndefined,
    *,
    default_factory: Callable[[], Any] | Callable[[dict[str, Any]], Any] | None = _Unset,
    alias: str | None = _Unset,
    alias_priority: int | None = _Unset,
    validation_alias: str | AliasPath | AliasChoices | None = _Unset,
    serialization_alias: str | None = _Unset,
    title: str | None = _Unset,
    field_title_generator: Callable[[str, FieldInfo], str] | None = _Unset,
    description: str | None = _Unset,
    examples: list[Any] | None = _Unset,
    exclude: bool | None = _Unset,
    discriminator: str | types.Discriminator | None = _Unset,
    deprecated: Deprecated | str | bool | None = _Unset,
    json_schema_extra: JsonDict | Callable[[JsonDict], None] | None = _Unset,
    frozen: bool | None = _Unset,
    validate_default: bool | None = _Unset,
    repr: bool = _Unset,
    init: bool | None = _Unset,
    init_var: bool | None = _Unset,
    kw_only: bool | None = _Unset,
    pattern: str | typing.Pattern[str] | None = _Unset,
    strict: bool | None = _Unset,
    coerce_numbers_to_str: bool | None = _Unset,
    gt: annotated_types.SupportsGt | None = _Unset,
    ge: annotated_types.SupportsGe | None = _Unset,
    lt: annotated_types.SupportsLt | None = _Unset,
    le: annotated_types.SupportsLe | None = _Unset,
    multiple_of: float | None = _Unset,
    allow_inf_nan: bool | None = _Unset,
    max_digits: int | None = _Unset,
    decimal_places: int | None = _Unset,
    min_length: int | None = _Unset,
    max_length: int | None = _Unset,
    union_mode: Literal['smart', 'left_to_right'] = _Unset,
    fail_fast: bool | None = _Unset,

    global_: bool = False,
    
    help: typing.Optional[str] = None,
    required: bool = _Unset,
    allow_none: bool = _Unset,
    aliases: typing.Optional[list] = None,
    prog: typing.Optional[str] = None,
    usage: typing.Optional[str] = None,
    epilog: typing.Optional[str] = None,
    prefix_chars: typing.Optional[str] = "-",
    add_help: bool = True,
    exit_on_error: bool = False,
    version: typing.Optional[str] = None,
    
    **extra: Unpack[_EmptyKwargs],
) -> FieldInfo:
    if aliases is None:
        aliases = []
    field = FieldInfo.from_field(
        default,
        default_factory=default_factory,
        alias=alias,
        alias_priority=alias_priority,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        title=title,
        field_title_generator=field_title_generator,
        description=description,
        examples=examples,
        exclude=exclude,
        discriminator=discriminator,
        deprecated=deprecated,
        json_schema_extra=json_schema_extra,
        frozen=frozen,
        validate_default=validate_default,
        repr=repr,
        init=init,
        init_var=init_var,
        kw_only=kw_only,
        pattern=pattern,
        strict=strict,
        coerce_numbers_to_str=coerce_numbers_to_str,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        min_length=min_length,
        max_length=max_length,
        union_mode=union_mode,
        fail_fast=fail_fast,
        global_ = global_,
        help=help,
        required=required,
        allow_none=allow_none,
        aliases=aliases,
        prog=prog,
        usage=usage,
        epilog=epilog,
        prefix_chars=prefix_chars,
        add_help=add_help,
        exit_on_error=exit_on_error,
        version=version,
        **extra
    )
    return field
