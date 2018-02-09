# -*- coding: utf-8 -*-

from typing import (
    Any,
    Dict,
    NewType,
    Type,
)

from diecast.component import Component

ComponentState = NewType('ComponentState', Dict[str, Any])
ComponentRegistry = NewType(
    'ComponentRegistry',
    Dict[Type[Component], ComponentState],
)

