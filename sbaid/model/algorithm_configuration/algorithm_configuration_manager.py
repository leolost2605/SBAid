"""This module represents the class AlgorithmConfigurationManager"""
import asyncio
from uuid import uuid4

from gi.repository import GObject, Gio

from sbaid import common
from sbaid.common.tag import Tag
from sbaid.model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.model.algorithm_configuration.parameter import TagNotFoundException
from sbaid.model.database.project_database import ProjectDatabase
from sbaid.model.network.network import Network


class AlgorithmConfigurationNotFoundException(Exception):
    """Raised when an algorithm configuration cannot be found"""


class AlgorithmConfigurationManager(GObject.GObject):
    """
    Manages and holds the algorithm configurations of a project. Furthermore it manages
    the tags that can be given to parameters across the algorithm configurations.
    """

    __background_tasks: set[asyncio.Task[None]]

    __db: ProjectDatabase
    __network: Network

    __selected_algo_config: str | None
    __available_tags: Gio.ListStore
    __algorithm_configurations: Gio.ListStore

    selected_algorithm_configuration_id: str | None = GObject.Property(  # type: ignore
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE)

    @selected_algorithm_configuration_id.getter  # type: ignore
    def selected_algorithm_configuration_id(self) -> str | None:
        """Returns the id of the selected algorithm configuration"""
        return self.__selected_algo_config

    @selected_algorithm_configuration_id.setter  # type: ignore
    def selected_algorithm_configuration_id(self, new_id: str) -> None:
        """Sets the id of the selected algorithm configuration"""
        self.__selected_algo_config = new_id

        task = asyncio.create_task(self.__db.set_selected_algorithm_configuration_id(new_id))
        self.__background_tasks.add(task)
        task.add_done_callback(self.__background_tasks.discard)

    available_tags: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore

    @available_tags.getter  # type: ignore
    def available_tags(self) -> Gio.ListModel:
        """Returns the list of available tags"""
        return self.__available_tags

    algorithm_configurations: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore

    @algorithm_configurations.getter  # type: ignore
    def algorithm_configurations(self) -> Gio.ListModel:
        """Returns the list of algorithm configurations"""
        return self.__algorithm_configurations

    def __init__(self, network: Network, db: ProjectDatabase) -> None:
        super().__init__()

        self.__db = db
        self.__network = network
        self.__available_tags = Gio.ListStore.new(Tag)
        self.__algorithm_configurations = Gio.ListStore.new(AlgorithmConfiguration)

    async def load(self) -> None:
        """Loads the algorithm configurations from the database."""

        algo_config_ids = await self.__db.get_all_algorithm_configuration_ids()

        for algo_config_id in algo_config_ids:
            algo_config = AlgorithmConfiguration(algo_config_id, self.__network, self.__db)
            self.__algorithm_configurations.append(algo_config)
            await algo_config.load_from_db()

        self.__selected_algo_config = await self.__db.get_selected_algorithm_configuration_id()

    async def create_algorithm_configuration(self) -> int:
        """
        Creates a new algorithm configuration.
        :return: the position of the new algo config in the list of algo configs
        """
        algo_config = AlgorithmConfiguration(str(uuid4()), self.__network, self.__db)

        await self.__db.add_algorithm_configuration(
            algo_config.id, algo_config.name, algo_config.evaluation_interval,
            algo_config.display_interval, algo_config.script_path, True)

        self.__selected_algo_config = algo_config.id
        self.__algorithm_configurations.append(algo_config)

        return self.__algorithm_configurations.get_n_items() - 1

    def delete_algorithm_configuration(self, algo_config_id: str) -> None:
        """
        Deletes the algorithm configuration with the given id.
        """

        for pos, config in enumerate(common.list_model_iterator(self.__algorithm_configurations)):
            if config.id == algo_config_id:
                self.__algorithm_configurations.remove(pos)

                task = asyncio.create_task(self.__db.remove_algorithm_configuration(algo_config_id))
                self.__background_tasks.add(task)
                task.add_done_callback(self.__background_tasks.discard)

                return

        raise AlgorithmConfigurationNotFoundException("The algorithm configuration "
                                                      f"with id {algo_config_id} was not found")

    async def create_tag(self, name: str) -> int:
        """
        Creates a new tag with the given name.
        :param name: the name of the new tag
        :return: the position in the available tags list of the new tag
        """

        tag = Tag(str(uuid4()), name)

        await self.__db.add_tag(tag.tag_id, tag.name)

        self.__available_tags.append(tag)

        return self.__available_tags.get_n_items() - 1

    def delete_tag(self, tag_id: str) -> None:
        """
        Deletes the tag with the given id.
        :param tag_id: the id of the tag to delete
        """

        for pos, tag in enumerate(common.list_model_iterator(self.__available_tags)):
            if tag.tag_id == tag_id:
                self.__available_tags.remove(pos)

                task = asyncio.create_task(self.__db.remove_tag(tag_id))
                self.__background_tasks.add(task)
                task.add_done_callback(self.__background_tasks.discard)

                return

        raise TagNotFoundException("The algorithm configuration "
                                   f"with id {tag_id} was not found")
