# -*- coding: utf-8 -*-

import pytest

from diecast.inject import build_passthru_args, map_passthru_args
from diecast.registry import ComponentRegistry, register_component

from tests.components import SimpleComponent


@pytest.fixture
def registry():

    r = ComponentRegistry()

    register_component(
        cls=SimpleComponent, init=SimpleComponent.init, persist=False, registry=r
    )

    return r


def test_build_passthru_args(registry):
    def _test(a: int, b: str, c: SimpleComponent, d: float):
        pass

    passthru = build_passthru_args(registry, _test)
    assert passthru == ["a", "b", "d"]


def test_map_passthru_args(registry):
    def _test(a: int, b: str, d: float):
        pass

    passthru = build_passthru_args(registry, _test)
    args = map_passthru_args(passthru, 42, "hello", 10.2)
    assert args == {"a": 42, "b": "hello", "d": 10.2}


def test_map_passthru_ellipses(registry):
    def _test(a: int, b: str, c: SimpleComponent, d: float):
        pass

    passthru = build_passthru_args(registry, _test)
    args = map_passthru_args(passthru, 42, "hello", ..., 10.2)
    assert args == {"a": 42, "b": "hello", "d": 10.2}
