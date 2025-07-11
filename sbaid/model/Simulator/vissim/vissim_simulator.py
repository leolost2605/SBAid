"""This module contains the VissimCrossSection class."""
from abc import ABC
from ..simulator import Simulator


class VissimSimulator(Simulator, ABC):
    """This class represents the PTV Vissim simulator."""
    pass
