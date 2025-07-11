"""This module contains the DummySimulator class."""
from abc import ABC
from ..simulator import Simulator


class DummySimulator(Simulator, ABC):
    """This class represents the dummy simulator."""
    pass
