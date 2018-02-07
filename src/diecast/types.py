# -*- coding: utf-8 -*-

from typing import (
    Any,
    Mapping,
    NewType,
    Type,
)

from diecast.component import Component

ComponentState = NewType('ComponentState', Mapping[str, Any])
ComponentRegistry = NewType(
    'ComponentRegistry',
    Mapping[Type[Component], ComponentState],
)

