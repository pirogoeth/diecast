# -*- coding: utf-8 -*-

import logging
import os
from typing import Type

from diecast.component import Component
from diecast.inject import make_injector
from diecast.registry import ComponentRegistry
from diecast.types import Injector

registry = ComponentRegistry()


class Settings(Component):
    ''' A component that is used to store application
        settings.
    '''

    DEBUG: bool = False
    LOG_LEVEL: int = logging.INFO

    @classmethod
    def init(cls: Type[Component]) -> 'Settings':

        this = Settings()

        this.DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
        this.LOG_LEVEL = logging._nameToLevel.get(
            os.getenv('LOG_LEVEL', 'INFO').upper(),
            logging.INFO,
        )

        return this

    @property
    def environment(self):
        ''' Assume the environment based on the DEBUG flag.
        '''

        if self.DEBUG:
            return 'develop'
        else:
            return 'production'


# I'll be using explicit argument forms here.
registry.add(
    cls=Settings,
    init=Settings.init,
    persist=True,
)

# Create an injector to use the Settings component
inject: Injector = make_injector(registry)


# Make a function to use the Settings component
@inject
def is_debugging(settings: Settings) -> bool:

    return settings.DEBUG


if __name__ == '__main__':

    print('settings.DEBUG:', is_debugging())
    print('environment:', registry[Settings].environment)
