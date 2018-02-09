# -*- coding: utf-8 -*-

from typing import Any, Type

from diecast.component import Component


class SimpleComponent(Component):
    ''' Defines a simple component which accepts no special arguments
        via initializer.
    '''

    @classmethod
    def init(cls: Type[Component]) -> 'SimpleComponent':

        return SimpleComponent()

    def some_action(self, val: Any) -> Any:

        return val


class ComplexComponent(Component):
    ''' Defines a component which expects a SimpleComponent to be injected
        via the initializer.
    '''

    @classmethod
    def init(cls: Type[Component], simple: SimpleComponent) -> 'ComplexComponent':

        return ComplexComponent(simple)

    def __init__(self, simple_component):

        self.simple_component = simple_component

    @property
    def simple(self):

        return self.simple_component
