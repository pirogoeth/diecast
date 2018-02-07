# -*- coding: utf-8 -*-

# this is the base test case of the DI prototype
from typing import Callable, Type

from component import Component
from di import build_passthru_args, make_injector
from registry import get_registry, register_component

# This builds a decorator - a Callable that returns a Callable
# when given a Callable. oof.
inject: Callable[[Callable], Callable] = make_injector(get_registry())


class TestComponent(Component):
    ''' This is a barebones Component which does not expect any DI on its
        initializer
    '''

    @classmethod
    def init(cls: Type[Component]) -> 'TestComponent':

        return TestComponent()


@inject
def example(thing: TestComponent, another_arg: str) -> str:

    print(f'example() got another_arg={another_arg}')
    return str(thing)


if __name__ == '__main__':

    register_component(
        TestComponent,
        init=TestComponent.init,  # be explicit just because
        persist=False,
    )

    # When dumping the passthru args for `example`, only `another_arg` should show up
    passthru = build_passthru_args(get_registry(), example)
    print(passthru)
    assert(len(passthru) == 1)
    assert('another_arg' in passthru)

    value = example('this is a part of the direct call')
    print('example (injected):', value)
