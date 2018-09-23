# -*- coding: utf-8 -*-

import unittest

from diecast.inject import make_injector
from diecast.registry import ComponentRegistry, register_component
from tests.components import SimpleComponent, ComplexComponent


class ComponentTestCase(unittest.TestCase):
    def setUp(self):

        self.registry = ComponentRegistry()

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

    def test_register_simple_component(self):

        self.register_simple_component(persist=False)

        self.assertIn(SimpleComponent, self.registry)
        self.assertEqual(self.registry.get(SimpleComponent)["instance"], None)

    def test_register_complex_component(self):

        self.register_simple_component(persist=False)
        self.register_complex_component(persist=False)

        self.assertIn(ComplexComponent, self.registry)
        self.assertEqual(self.registry.get(ComplexComponent)["instance"], None)

    def test_persist_simple_component(self):

        self.register_simple_component(persist=True)

        self.assertIn(SimpleComponent, self.registry)
        self.assertNotEqual(self.registry[SimpleComponent], None)

    def test_persist_complex_component(self):

        self.register_simple_component(persist=True)
        self.register_complex_component(persist=True)

        self.assertIn(ComplexComponent, self.registry)
        self.assertNotEqual(self.registry[ComplexComponent], None)

        complex_comp = self.registry[ComplexComponent]
        simple_comp = complex_comp.simple
        self.assertEqual(self.registry[SimpleComponent], simple_comp)

    def test_inject_complex_component(self):

        self.test_persist_complex_component()

        inject = make_injector(self.registry)

        @inject
        def _test_func(complex_comp: ComplexComponent):

            self.assertIsInstance(complex_comp, ComplexComponent)
            return complex_comp.simple.some_action("success")

        self.assertEqual(_test_func(), "success")

    def test_inject_complex_ellipses_placeholder(self):

        self.test_persist_complex_component()

        inject = make_injector(self.registry)

        @inject
        def _test_func(complex_comp: ComplexComponent):

            self.assertIsInstance(complex_comp, ComplexComponent)
            return complex_comp.simple.some_action("success")

        self.assertEqual(_test_func(...), "success")

    def test_inject_complex_ellipses_ordering(self):

        self.test_persist_complex_component()

        inject = make_injector(self.registry)

        @inject
        def _test_func(a: int, b: str, complex_comp: ComplexComponent, d: float):

            self.assertEqual(a, 42)
            self.assertEqual(b, "testing")
            self.assertIsInstance(complex_comp, ComplexComponent)
            self.assertEqual(d, 10.2)
            return complex_comp.simple.some_action("success")

        self.assertEqual(_test_func(42, "testing", ..., 10.2), "success")
