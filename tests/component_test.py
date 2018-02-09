# -*- coding: utf-8 -*-

import unittest
from nose.tools import *

from diecast.inject import make_injector
from diecast.registry import register_component
from diecast.types import ComponentRegistry
from tests.components import (
    SimpleComponent,
    ComplexComponent,
)


class ComponentTestCase(unittest.TestCase):

    def setUp(self):

        self.registry = ComponentRegistry({})

    def register_simple_component(self, persist=False):

        register_component(
            cls=SimpleComponent,
            init=SimpleComponent.init,
            persist=persist,
            registry=self.registry,
        )

    def register_complex_component(self, persist=False):

        # Since this is not persisting, it does not initialize immediately and
        # does not require SimpleComponent to be registered
        register_component(
            cls=ComplexComponent,
            init=ComplexComponent.init,
            persist=persist,
            registry=self.registry,
        )

    def register_simple_component_test(self):

        self.register_simple_component(persist=False)

        self.assertIn(SimpleComponent, self.registry)
        self.assertEqual(self.registry[SimpleComponent]['instance'], None)

    def register_complex_component_test(self):

        self.register_complex_component(persist=False)

        self.assertIn(ComplexComponent, self.registry)
        self.assertEqual(self.registry[ComplexComponent]['instance'], None)

    def persist_simple_component_test(self):

        self.register_simple_component(persist=True)

        self.assertIn(SimpleComponent, self.registry)
        self.assertNotEqual(self.registry[SimpleComponent]['instance'], None)

    def persist_complex_component_test(self):

        self.register_simple_component(persist=True)
        self.register_complex_component(persist=True)

        self.assertIn(ComplexComponent, self.registry)
        self.assertNotEqual(self.registry[ComplexComponent]['instance'], None)

        complex_comp = self.registry[ComplexComponent]['instance']
        simple_comp = complex_comp.simple
        self.assertEqual(self.registry[SimpleComponent]['instance'], simple_comp)

    def inject_complex_component_test(self):

        self.persist_complex_component_test()

        inject = make_injector(self.registry)

        @inject
        def _test_func(complex_comp: ComplexComponent):

            self.assertIsInstance(complex_comp, ComplexComponent)
            return complex_comp.simple.some_action('success')

        self.assertEqual(_test_func(), 'success')
