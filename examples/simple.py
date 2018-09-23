# -*- coding: utf-8 -*-

# this is the base test case of the DI prototype
import logging
import sys
from typing import Type

from diecast.component import Component
from diecast.inject import build_passthru_args, make_injector
from diecast.registry import get_registry, register_component
from diecast.types import Injector

# This builds a decorator - a Callable that returns a Callable
# when given a Callable. oof.
inject: Injector = make_injector(get_registry())


class TestComponent(Component):
    ''' This is a barebones Component which does not expect any DI on its
        initializer
    '''

    @classmethod
    def init(cls: Type[Component]) -> 'TestComponent':

        return TestComponent()


class EmbeddingComponent(Component):
    ''' This component embeds a TestComponent
    '''

    @classmethod
    def init(cls: Type[Component], tc: TestComponent) -> 'EmbeddingComponent':

        c = cls()
        c.test_component = tc
        return c


@inject
def example(thing: TestComponent, another_arg: str) -> str:

    print(f'example() got another_arg={another_arg}')
    return str(thing)


@inject
def embedding(thing: EmbeddingComponent) -> str:

    print(f'component is {thing}, embedded component is {thing.test_component}')
    return str(thing)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    register_component(
        TestComponent,
        init=TestComponent.init,  # be explicit just because
        persist=False,
    )

    register_component(
        EmbeddingComponent,
        init=EmbeddingComponent.init,
        persist=True,
    )

    # When dumping the passthru args for `example`, only `another_arg` should show up
    passthru = build_passthru_args(get_registry(), example)
    assert(len(passthru) == 1)
    assert('another_arg' in passthru)

    value = example(..., 'this is a part of the direct call')
    print('example (injected):', value)

    value = embedding(...)
    print('embedding (injected):', value)
