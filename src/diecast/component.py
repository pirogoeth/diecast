# -*- coding: utf-8 -*-

import abc
from typing import Type


class Component(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def init(cls: Type['Component'], *args, **kw) -> 'Component':
        ''' Component initializer -- should be implemented by Component
            inheritors
        '''

        pass
