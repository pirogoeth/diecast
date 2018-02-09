# -*- coding: utf-8 -*-

from typing import (
    Callable,
    Optional,
    Type,
)

from diecast.component import Component
from diecast.inject import _call_with_bound_params, _do_inject
from diecast.types import ComponentRegistry

__components: ComponentRegistry = {}


def get_registry() -> ComponentRegistry:
    ''' Returns the default global registry.
    '''

    global __components
    return __components


def register_component(cls: Type[Component],
                       init: Optional[Callable[..., Component]]=None,
                       persist: bool=True,
                       registry: ComponentRegistry=None):
    ''' Register a component with the dependency injection system.

        `cls` is the class that will be registered in the registry.

        `init` is the Callable that will provide an instance of `cls` for injection.
            Before `init` is called, dependency injection is performed on the function.

        `persist` specifies that the created instance should be stored in the registry.

        `registry` is the `ComponentRegistry` instance that the component will be registered with.
            If `None`, will use the default global registry.
    '''

    if registry is None:
        global __components
        registry = __components

    assert cls not in registry

    if not init:
        init = cls.init

    instance = None

    if persist:
        # This should perform DI on the `init` callable to
        # instantiate the Component
        sig_params = _do_inject(registry, init)
        instance = _call_with_bound_params(init, sig_params)

    registry.update({
        cls: {
            'init': init,
            'persist': persist,
            'instance': instance,
        },
    })

