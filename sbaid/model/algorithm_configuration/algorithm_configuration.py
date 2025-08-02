"""This module defines the AlgorithmConfiguration class"""
import asyncio
import importlib.util
import sys
import os

from gi.repository import GObject

from sbaid.model.database.project_database import ProjectDatabase
from sbaid.model.network.network import Network
from sbaid.model.algorithm.algorithm import Algorithm
from sbaid.model.algorithm_configuration.parameter_configuration import (
    ParameterConfiguration)


class AlgorithmNotFoundException(Exception):
    """Raised when loading an algorithm from a script path failed."""


class AlgorithmConfiguration(GObject.GObject):
    """
    Represents an algorithm configuration consisting of an algorithm given via its script path,
    evaluation and display interval, a name, and the parameter configuration for the
    algorithm.
    """

    __background_tasks: set[asyncio.Task[None]]
    __db: ProjectDatabase

    __name: str = "New Algorithm Configuration"
    __script_path: str | None = None
    __evaluation_interval: int = 60
    __display_interval: int = 60

    id: str = GObject.Property(  # type: ignore
        type=str,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    name: str = GObject.Property(type=str)  # type: ignore

    @name.getter  # type: ignore
    def name(self) -> str:
        """Returns the name of the algo config"""
        return self.__name

    @name.setter  # type: ignore
    def name(self, new_name: str) -> None:
        """Sets the name of the algo config"""
        self.__name = new_name

        task = asyncio.create_task(self.__db.set_algorithm_configuration_name(self.id, new_name))
        self.__background_tasks.add(task)
        task.add_done_callback(self.__background_tasks.discard)

    script_path: str = GObject.Property(type=str)  # type: ignore

    @script_path.getter  # type: ignore
    def script_path(self) -> str | None:
        """Returns the current script path of the algo config"""
        return self.__script_path

    @script_path.setter  # type: ignore
    def script_path(self, new_script_path: str) -> None:
        """Sets the current script path of the algo config"""
        self.__script_path = new_script_path

        task = asyncio.create_task(self.__db.set_script_path(self.id, new_script_path))
        self.__background_tasks.add(task)
        task.add_done_callback(self.__background_tasks.discard)

        load_task = asyncio.create_task(self.__load_algorithm())
        self.__background_tasks.add(load_task)
        task.add_done_callback(self.__background_tasks.discard)

    evaluation_interval: int = GObject.Property(type=int)  # type: ignore

    @evaluation_interval.getter  # type: ignore
    def evaluation_interval(self) -> int:
        """Returns the current evaluation interval"""
        return self.__evaluation_interval

    @evaluation_interval.setter  # type: ignore
    def evaluation_interval(self, new_evaluation_interval: int) -> None:
        """Sets the evaluation interval"""
        self.__evaluation_interval = new_evaluation_interval

        task = asyncio.create_task(self.__db.set_evaluation_interval(self.id,
                                                                     new_evaluation_interval))
        self.__background_tasks.add(task)
        task.add_done_callback(self.__background_tasks.discard)

    display_interval: int = GObject.Property(type=int)  # type: ignore

    @display_interval.getter  # type: ignore
    def display_interval(self) -> int:
        """Returns the display interval"""
        return self.__display_interval

    @display_interval.setter  # type: ignore
    def display_interval(self, new_display_interval: int) -> None:
        """Sets the display interval"""
        self.__display_interval = new_display_interval

        task = asyncio.create_task(self.__db.set_evaluation_interval(self.id,
                                                                     new_display_interval))
        self.__background_tasks.add(task)
        task.add_done_callback(self.__background_tasks.discard)

    algorithm: Algorithm = GObject.Property(  # type: ignore
        type=Algorithm,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    parameter_configuration: ParameterConfiguration = GObject.Property(  # type: ignore
        type=ParameterConfiguration,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, configuration_id: str, network: Network, db: ProjectDatabase) -> None:
        super().__init__(id=configuration_id, parameter_configuration=ParameterConfiguration(
                         network, db, configuration_id))
        self.__db = db

    async def load_from_db(self) -> None:
        """
        Loads the meta data about this algorithm configuration like name, etc. from the database.
        """
        self.__name = await self.__db.get_algorithm_configuration_name(self.id)
        self.__script_path = await self.__db.get_script_path(self.id)
        await self.__load_algorithm()
        self.__evaluation_interval = await self.__db.get_evaluation_interval(self.id)
        self.__display_interval = await self.__db.get_evaluation_interval(self.id)

    async def __load_algorithm(self) -> None:
        if self.__script_path is None:
            return

        base_name = os.path.basename(self.__script_path)
        module_name = base_name.removesuffix(".py")

        spec = importlib.util.spec_from_file_location(module_name, self.__script_path)

        if spec is None:
            raise AlgorithmNotFoundException("Failed to get spec from path and module name")

        module = importlib.util.module_from_spec(spec)

        if module is None:
            raise AlgorithmNotFoundException("Failed to get module from spec")

        sys.modules[module_name] = module

        if spec.loader is None:
            raise AlgorithmNotFoundException("Spec has no loader")

        spec.loader.exec_module(module)

        self.algorithm = module.Algorithm()
        self.parameter_configuration.set_algorithm(self.algorithm)
