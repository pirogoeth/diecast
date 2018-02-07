# -*- coding: utf-8 -*-

from typing import (
    Any,
    Callable,
    Mapping,
    NewType,
    Optional,
    Type,
)

from component import Component

ComponentState = NewType('ComponentState', Mapping[str, Any])
ComponentRegistry = NewType(
    'ComponentRegistry',
    Mapping[Type[Component], ComponentState],
)

__components: ComponentRegistry = {}


def get_registry() -> ComponentRegistry:

    global __components
    return __components


def register_component(cls: Type[Component],
                       init: Optional[Callable[..., Component]]=None,
                       persist: bool=True):

    global __components

    assert cls not in __components

    if not init:
        init = cls.init

    if persist:
        # This should perform DI on the `init` callable to
        # instantiate the Component
        pass
    else:
        print(f'Putting component {cls}')
        __components.update({
            cls: {
                'init': init,
                'persist': persist,
                'instance': None,
            },
        })

