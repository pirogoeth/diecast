# -*- coding: utf-8 -*-

import inspect
import logging
from functools import wraps
from inspect import Parameter
from typing import (
    Any,
    Callable,
    List,
    Mapping,
    Type,
    get_type_hints,
)

from diecast.types import Injector

_log = logging.getLogger(__name__)


def _not_injectable(registry: 'ComponentRegistry', hint: Type) -> bool:

    return hint == Any or hint not in registry or hint is Parameter.empty


def build_arg_mapping(fn: Callable) -> Mapping[str, Any]:

    hints = get_type_hints(fn)
    if 'return' in hints:
        hints.pop('return')

    arg_names = fn.__code__.co_varnames[:fn.__code__.co_argcount]
    for arg in arg_names:
        if arg not in hints:
            hints.update({arg: Any})

    return hints


def build_passthru_args(registry: 'ComponentRegistry', fn: Callable) -> List[str]:

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


def make_injector(registry: 'ComponentRegistry') -> Injector:

    def _injector(fn: Callable):

        @wraps(fn)
        def _arg_injector(*args, **kw):

            sig_params = _do_inject(registry, fn, *args, **kw)
            return _call_with_bound_params(fn, sig_params)

        return _arg_injector

    return _injector


def _do_inject(_registry: 'ComponentRegistry', _fn: Callable, *args, **kw) -> inspect.BoundArguments:

    _log.debug(f'Performing injection for {_fn} with {_registry}')

    sig = inspect.signature(_fn)

    arg_map = build_arg_mapping(_fn)
    injected_params = {}

    for arg, hint in arg_map.items():
        if _not_injectable(_registry, hint):
            continue

        dep = _registry.get(hint)

        if dep['instance'] is None:
            # Initialize dependency - should also perform DI on this!
            _log.debug(f'Initialize dependency for injection {dep}')

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

    passthru_args = build_passthru_args(_registry, _fn)
    passthru_params = map_passthru_args(passthru_args, *args, **kw)

    params = dict(injected_params)
    params.update(passthru_params)

    return sig.bind_partial(**params)


def _call_with_bound_params(fn: Callable, sig_params: inspect.BoundArguments) -> Any:

    return fn(*sig_params.args, **sig_params.kwargs)
