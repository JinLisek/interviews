from __future__ import annotations

from abc import ABCMeta
from typing import Dict


class AbstractSingletonMeta(ABCMeta):
    _instances: Dict[type, AbstractSingletonMeta] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(AbstractSingletonMeta, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]
