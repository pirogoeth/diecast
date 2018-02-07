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

    global __components
    return __components


def register_component(cls: Type[Component],
                       init: Optional[Callable[..., Component]]=None,
                       persist: bool=True,
                       registry: ComponentRegistry=None):

    if not registry:
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

