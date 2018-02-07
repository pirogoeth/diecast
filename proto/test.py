#!/usr/bin/env python

import di
import registry

def a(b, c, d: str, e: int = 10) -> str:
    pass

print(di.build_passthru_args(registry.get_registry(), a))
