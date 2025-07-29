import typing
from pydantic import BaseModel as PydanticBaseModel

from ._construct import BaseModelMetaRewrite
from .fields import Field, FieldInfo


_T = typing.TypeVar('_T')

def __dataclass_transform__(
    *,
    eq_default: bool = True,       
    order_default: bool = False,   
    kw_only_default: bool = False, 
    field_descriptors: tuple[typing.Union[type, typing.Callable[..., typing.Any]], ...] = (()), # pylint: disable=unused-argument
) -> typing.Callable[[_T], _T]:
    return lambda a: a

class GlobalData(dict):
    pass

default_global_data = GlobalData()

class ActionNameBind:
    """
    Action name bind. This is a marker class for action bind types.
    
    Example:
    
    ```python
    from argparse_dantic import ArgumentParser, BaseModel, Field, ActionNameBind
    
    class MyBaseModel(BaseModel):
        action_name: ActionNameBind
    
    class OptionModels(MyBaseModel):
        option_a: bool = Field(default=False, aliases=['--a'])
        option_b: bool = Field(default=False, aliases=['--b'])
    
    class ActionModel(OptionModels):
        action_a: ActionA = Field(...)
        action_b: ActionB = Field(...)
    
    if __name__ == '__main__':
        args = ['action_a', '--a']
        parser = ArgumentParser(
            model=ActionModel,
        )
        arguments = parser.parse_typed_args(args)
        print(arguments)
    
    ```
    >>> ActionModel(action_name='action_a', option_a=True, option_b=True)
    """

@__dataclass_transform__(kw_only_default=True, field_descriptors=(Field, FieldInfo))
class BaseModelMeta(BaseModelMetaRewrite):
    @classmethod
    def __set__action_name_binds_names__(mcs, bases: tuple[type], namespace: dict[str, typing.Any], annotations: dict[str, typing.Any]) -> None:
        action_name_binds_names = set()
        if bases:
            for base in bases:
                if hasattr(base, '__action_name_binds_names__'):
                    action_name_binds_names.update(getattr(base, '__action_name_binds_names__'))
        for k, v in annotations.items():
            typ = typing.get_origin(v) or v
            try:
                if issubclass(typ, ActionNameBind):
                    action_name_binds_names.add(k)
            except TypeError:
                # ignore non-classes
                pass
        if '__action_name_binds_names__' in namespace:
            action_name_binds_names.update(namespace['__action_name_binds_names__'])
        
        for action_name in action_name_binds_names:
            # 仅保留 __action_name_binds_names__
            if action_name in namespace:
                del namespace[action_name]
            if action_name in annotations:
                del annotations[action_name]
        
        namespace['__action_name_binds_names__'] = action_name_binds_names

class BaseModel(PydanticBaseModel, metaclass=BaseModelMeta, global_data=default_global_data):
    # 用于标记Fields中CommandAction的绑定名称列表
    global_data: typing.ClassVar[GlobalData]
    __action_name_binds_names__: typing.ClassVar[set[str]]
    
    if typing.TYPE_CHECKING:
        model_fields: typing.ClassVar[dict[str, FieldInfo]]