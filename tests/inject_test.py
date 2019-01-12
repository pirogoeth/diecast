# -*- coding: utf-8 -*-

import pytest

from diecast.inject import build_passthru_args, make_injector, map_passthru_args
from diecast.registry import ComponentRegistry, register_component

from tests.components import SimpleComponent


@pytest.fixture
def registry():
    r = ComponentRegistry()

    register_component(
        cls=SimpleComponent, init=SimpleComponent.init, persist=False, registry=r
    )

    return r


@pytest.fixture
def injector(registry):
    return make_injector(registry)


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


def test_map_passthru_kwargs(registry):
    def _test(alpha=None, beta=None):
        pass

    passthru = build_passthru_args(registry, _test)
    args = map_passthru_args(passthru, alpha="gamma", beta="omega")
    assert args == {"alpha": "gamma", "beta": "omega"}


def test_stacking_decorators(registry, injector):
    """ This test is targeting a single issue that appears when stacking
        multiple decorators on a function, followed by an @inject.

        The signature that this was produced with is:

            @github_client.command()
            @click.argument("repo")
            @click.argument("property")
            @app.inject
            def get_repo(gh: Github, repo: str, property: str):
                ...
    """

    def external_params(fn):
        def _inner(*args, **kw):
            # Click actually passes arguments to the callback as kwargs
            kw.update({"repo": "pirogoeth/diecast", "property": "id"})
            return fn(*args, **kw)

        return _inner

    @external_params
    @injector
    def _test(item: SimpleComponent, repo: str, property: str):
        assert isinstance(item, SimpleComponent)
        assert isinstance(repo, str)
        assert isinstance(property, str)

        assert repo == "pirogoeth/diecast"
        assert property == "id"

        return True

    assert _test(..., ..., ...) == True
