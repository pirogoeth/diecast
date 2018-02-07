# -*- coding: utf-8 -*-

import inspect
from functools import wraps
from inspect import Parameter
from typing import (
    Any,
    Callable,
    List,
    Mapping,
    get_type_hints,
)

from component import Component
from registry import ComponentRegistry

_not_injectable = lambda reg, h: h == Any or h not in reg or h is Parameter.empty


def build_arg_mapping(fn: Callable) -> Mapping[str, Any]:

    hints = get_type_hints(fn)
    hints.pop('return')

    arg_names = fn.__code__.co_varnames[:fn.__code__.co_argcount]
    for arg in arg_names:
        if arg not in hints:
            hints.update({arg: Any})

    return hints


def build_passthru_args(registry: ComponentRegistry, fn: Callable) -> List[str]:

    args = []

    sig = inspect.signature(fn)
    fn_params = {parm.name: parm.annotation for name, parm in sig.parameters.items()}

    for arg, hint in fn_params.items():
        if _not_injectable(registry, hint):
            # This is not an injectable argument
            args.append(arg)

    return args


def map_passthru_args(passthru_args: List[str], *args, **kw) -> Mapping[str, Any]:

    arg_map = {}

    # Apply *args in order
    for name, val in zip(passthru_args, args):
        arg_map.update({name: val})

    for name, val in kw.items():
        if name in passthru_args:
            if name in arg_map:
                raise ValueError(f'Passthru arg {name} mapped through *args and **kw')

            arg_map.update({name: val})

    return arg_map


def make_injector(registry: ComponentRegistry) -> Callable[[Callable], Callable]:

    def _injector(fn: Callable):

        # Build a signature and the injected fntion
        sig = inspect.signature(fn)

        @wraps(fn)
        def _arg_injector(*args, **kw):

            print(f'Performing injection for {fn} with {registry}')

            arg_map = build_arg_mapping(fn)
            injected_params = {}

            for arg, hint in arg_map.items():
                if _not_injectable(registry, hint):
                    continue

                dep = registry.get(hint)

                if dep['instance'] is None:
                    # Initialize dependency - should also perform DI on this!
                    print(f'Initialize dependency for injection {dep}')
                    instance = dep.get('init')()
                    if dep.get('persist'):
                        dep.update({'instance': instance})

                    injected_params.update({
                        arg: instance,
                    })
                else:
                    injected_params.update({
                        arg: dep.get('instance'),
                    })

            passthru_args = build_passthru_args(registry, fn)
            passthru_params = map_passthru_args(passthru_args, *args, **kw)

            params = dict(injected_params)
            params.update(passthru_params)

            sig_params = sig.bind_partial(**params)
            return fn(*sig_params.args, **sig_params.kwargs)

        return _arg_injector

    return _injector
