# mypy: disable-error-code="union-attr"
# connections are checked for None in the db_action decorator
"""This module contains the ProjectSQLite class."""
import functools
from typing import cast, TypeVar, Callable, Any, Awaitable

import aiosqlite
import aiopathlib
from gi.repository import GLib, Gio

import sbaid.common
from sbaid.model.database.project_database import ProjectDatabase


class InvalidDatabaseError(Exception):
    """Exception raised when an invalid database is encountered."""


class NotOpenedException(Exception):
    """Exception raised when an action was attempted that requires an open database
    but the database was not opened."""


F = TypeVar('F', bound=Callable[..., Awaitable[Any]])


class ProjectSQLite(ProjectDatabase):
    """This class implements the ProjectDatabase interface which allows for the
    project specific data to be stored."""
    _file: Gio.File
    _creation_time: GLib.DateTime
    __connection: aiosqlite.Connection | None

    @staticmethod
    def db_action(func: F) -> F:
        """DB action decorator that checks for the connection to exist. """
        @functools.wraps(func)  # pylint: disable=no-self-argument
        async def wrapper(self: Any, *args: Any) -> Any:
            if self.__connection is None:
                raise NotOpenedException("The database is not open.")
            return await func(self, *args)

        return wrapper

    def __init__(self, file: Gio.File) -> None:
        self._file = file
        self._creation_time = cast(GLib.DateTime, GLib.DateTime.new_now_local())
        self.__connection = None

        app = Gio.Application.get_default()  # pylint: disable=no-value-for-parameter
        if app:
            app.connect("shutdown", self.__on_app_shutdown)

    def __on_app_shutdown(self, app: Gio.Application) -> None:
        if self.__connection is None:
            return
        sbaid.common.run_coro_in_background(self.__connection.close())

    async def open(self) -> None:
        """Loads the database's schema."""
        already_existed = self._file.query_exists()
        is_valid = True
        if self.__connection is None:
            self.__connection = await aiosqlite.connect(str(self._file.get_path()))
            async with self.__connection.execute("""PRAGMA integrity_check""") as cursor:
                res = await cursor.fetchone()
                assert res is not None
                is_valid = res[0] == 'ok'
        if not is_valid:
            raise InvalidDatabaseError("The given file is not a valid global sqlite database.")
        if not already_existed:
            async_path = aiopathlib.AsyncPath(self._file.get_parent().get_path())  # type: ignore
            if not await async_path.exists():
                await async_path.mkdir(parents=True)

        if not already_existed:
            await self.__connection.executescript("""
            PRAGMA foreign_keys = ON;
            CREATE TABLE meta_information(
                name TEXT,
                created_at TEXT,
                last_opened TEXT
            );
            CREATE TABLE algorithm_configuration (
                id TEXT PRIMARY KEY,
                name TEXT,
                evaluation_interval INTEGER,
                display_interval INTEGER,
                script_path TEXT,
                is_selected BOOLEAN
            );
            CREATE TABLE cross_section (
                id TEXT PRIMARY KEY,
                name TEXT,
                HARD_SHOULDER_ACTIVE BOOLEAN,
                B_DISPLAY_ACTIVE BOOLEAN
            );
            CREATE TABLE parameter (
                algorithm_configuration_id TEXT,
                name TEXT,
                cross_section_id TEXT,
                value TEXT,
                PRIMARY KEY (algorithm_configuration_id, name, cross_section_id),
                FOREIGN KEY (algorithm_configuration_id) REFERENCES algorithm_configuration(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (cross_section_id) REFERENCES cross_section(id) ON DELETE CASCADE
            );
            CREATE TABLE tag (
                id TEXT PRIMARY KEY,
                name TEXT
            );
            CREATE TABLE parameter_tag (
                id TEXT PRIMARY KEY,
                parameter_name TEXT,
                algorithm_configuration_id TEXT,
                cross_section_id TEXT,
                tag_id TEXT,
                FOREIGN KEY (algorithm_configuration_id, parameter_name, cross_section_id)
                    REFERENCES parameter(algorithm_configuration_id, name, cross_section_id)
                        ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE
            );""")
            await self.__connection.execute("""
            INSERT INTO meta_information (name, created_at, last_opened) VALUES
            (?, ?, ?)""", ("", GLib.DateTime.format_iso8601(self._creation_time),
                           GLib.DateTime.format_iso8601(  # pylint: disable=no-member
                               GLib.DateTime.new_now_local())))  # type: ignore
        await self.__connection.commit()

    @db_action
    async def get_created_at(self) -> GLib.DateTime | None:
        """Return the GLib.DateTime when the project was created."""
        async with (self.__connection.execute("""SELECT created_at FROM meta_information""")
                    as cursor):
            date = await cursor.fetchone()
            if date is None:
                return None
            return GLib.DateTime.new_from_iso8601(date[0])    # pylint: disable=no-member

    @db_action
    async def get_last_opened(self) -> GLib.DateTime | None:
        """Return the GLib.DateTime when the project was last modified."""
        async with (self.__connection.execute("""SELECT last_opened FROM meta_information""")
                    as cursor):
            date = await cursor.fetchone()
            if date is None:
                return None
            return GLib.DateTime.new_from_iso8601(date[0])  # pylint: disable=no-member

    @db_action
    async def set_last_opened(self, new_last_opened: GLib.DateTime) -> None:
        """Update the GLib.DateTime when the project was last opened."""
        await self.__connection.execute("""UPDATE meta_information SET last_opened = ?""",
                                        [new_last_opened.format_iso8601()])
        await self.__connection.commit()

    @db_action
    async def get_project_name(self) -> str | None:
        """Return the name of the project."""
        async with self.__connection.execute("""SELECT name FROM meta_information""") as cursor:
            result_list = await cursor.fetchone()
            if result_list is None:
                return None
            return str(result_list[0])

    @db_action
    async def set_project_name(self, name: str) -> None:
        """Update the name of the project."""
        await self.__connection.execute("""UPDATE meta_information SET name = ?""", [name])
        await self.__connection.commit()

    @db_action
    async def get_cross_section_name(self, cross_section_id: str) -> str | None:
        """Return the name of the cross_section with the given id."""
        async with self.__connection.execute("""SELECT name FROM cross_section WHERE id = ?""",
                                             [cross_section_id]) as cursor:
            result = await cursor.fetchone()
            if result is None:
                return None
            return str(list(result)[0])

    @db_action
    async def set_cross_section_name(self, cross_section_id: str, name: str) -> None:
        """Update the name of the cross_section with the given id."""
        await self.__connection.execute("""UPDATE cross_section SET name = ?
        WHERE id = ?""", (name, cross_section_id))
        await self.__connection.commit()

    @db_action
    async def get_cross_section_hard_shoulder_active(self, cross_section_id: str) -> bool | None:
        """Return whether the hard should is active for the given cross section."""
        async with self.__connection.execute(
                """SELECT hard_shoulder_active FROM cross_section WHERE id = ?""",
                [cross_section_id]) as cursor:
            result = await cursor.fetchone()
            if result is None:
                return None
            return bool(list(result)[0])

    @db_action
    async def set_cross_section_hard_shoulder_active(self, cross_section_id: str,
                                                     status: bool) -> None:
        """Update the hard_shoulder_active value of the cross_section with the given id."""
        await self.__connection.execute("""UPDATE cross_section SET hard_shoulder_active = ?
        WHERE id = ?""", (status, cross_section_id))
        await self.__connection.commit()

    @db_action
    async def get_cross_section_b_display_active(self, cross_section_id: str) -> bool | None:
        """Return whether the hard should is active for the given cross section."""
        async with self.__connection.execute(
                """SELECT b_display_active FROM cross_section WHERE id = ?""",
                [cross_section_id]) as cursor:
            result = await cursor.fetchone()
            if result is None:
                return None
            return bool(list(result)[0])

    @db_action
    async def set_cross_section_b_display_active(self, cross_section_id: str, value: bool) -> None:
        """Update the b_display_active value of the cross_section with the given id."""
        await self.__connection.execute("""UPDATE cross_section SET b_display_active = ?
        WHERE id = ?""", (value, cross_section_id))
        await self.__connection.commit()

    @db_action
    async def get_algorithm_configuration_name(self, algorithm_configuration_id: str) -> str | None:
        """Return the name of the algorithm_configuration with the given id."""
        async with self.__connection.execute("""SELECT name FROM algorithm_configuration
        WHERE id = ?""", [algorithm_configuration_id]) as cursor:
            result_list = await cursor.fetchone()
            if result_list is None:
                return None
            return str(result_list[0])

    @db_action
    async def set_algorithm_configuration_name(self, algorithm_configuration_id: str,
                                               name: str) -> None:
        """Update the name of the algorithm_configuration with the given id."""
        await self.__connection.execute("""UPDATE algorithm_configuration SET name = ?
        WHERE id = ?""", (name, algorithm_configuration_id))
        await self.__connection.commit()

    @db_action
    async def get_algorithm_configuration(self, algorithm_configuration_id: str)\
            -> tuple[str, str, int, int, str, bool]:
        """Return the algorithm_configuration with the given id."""
        async with self.__connection.execute("""SELECT * FROM algorithm_configuration
        WHERE id = ?""", [algorithm_configuration_id]) as cursor:
            result_list = await cursor.fetchone()
            if result_list is None:
                return "", "", 0, 0, "", False
            return result_list[0]  # type: ignore

    @db_action
    async def get_all_algorithm_configuration_ids(self) -> list[str]:
        """Return all algorithm_configuration ids."""
        async with (self.__connection.execute("""SELECT id FROM algorithm_configuration""")
                    as cursor):
            result_list = await cursor.fetchall()
            return list(map(lambda x: x[0], result_list))

    @db_action
    async def get_selected_algorithm_configuration_id(self) -> str | None:
        """Return the currently selected algorithm_configuration id."""
        async with self.__connection.execute("""SELECT id FROM algorithm_configuration
        WHERE is_selected = 1""") as cursor:
            result = await cursor.fetchone()
            if result is None:
                return None
            return str(list(result)[0])

    @db_action
    async def set_selected_algorithm_configuration_id(self, configuration_id: str) -> None:
        """Update the currently selected algorithm_configuration id."""
        await self.__connection.execute("""UPDATE algorithm_configuration SET is_selected = 0""")
        await self.__connection.execute("""UPDATE algorithm_configuration SET is_selected = 1
        WHERE id = ?""", [configuration_id])
        await self.__connection.commit()

    @db_action
    async def get_display_interval(self, algorithm_configuration_id: str) -> int | None:
        """Return the display interval of the given algorithm_configuration id."""
        async with self.__connection.execute("""SELECT display_interval FROM algorithm_configuration
        WHERE id = ?""", [algorithm_configuration_id]) as cursor:
            result_list = await cursor.fetchone()
            if result_list is None:
                return None
            return int(result_list[0])

    @db_action
    async def set_display_interval(self, algorithm_configuration_id: str, interval: int) -> None:
        """Update the display interval of the given algorithm_configuration id."""
        await self.__connection.execute("""UPDATE algorithm_configuration SET display_interval = ?
        WHERE id = ?""", (interval, algorithm_configuration_id))
        await self.__connection.commit()

    @db_action
    async def get_evaluation_interval(self, algorithm_configuration_id: str) -> int | None:
        """Return the evaluation interval of the given algorithm_configuration id."""
        async with self.__connection.execute("""SELECT evaluation_interval
        FROM algorithm_configuration WHERE id = ?""", [algorithm_configuration_id]) as cursor:
            result_list = await cursor.fetchone()
            if result_list is None:
                return None
            return int(result_list[0])

    @db_action
    async def set_evaluation_interval(self, algorithm_configuration_id: str,
                                      interval: int) -> None:
        """Update the evaluation interval of the given algorithm_configuration id."""
        await self.__connection.execute("""UPDATE algorithm_configuration
        SET evaluation_interval = ? WHERE id = ?""", (interval, algorithm_configuration_id))
        await self.__connection.commit()

    @db_action
    async def get_script_path(self, algorithm_configuration_id: str) -> str | None:
        """Return the scrip path of the given algorithm_configuration id."""
        async with self.__connection.execute("""SELECT script_path FROM algorithm_configuration
        WHERE id = ?""", [algorithm_configuration_id]) as cursor:
            result_list = await cursor.fetchone()
            if result_list is None:
                return None
            return str(result_list[0])

    @db_action
    async def set_script_path(self, algorithm_configuration_id: str, path: str) -> None:
        """Update the script path of the given algorithm_configuration id."""
        await self.__connection.execute("""UPDATE algorithm_configuration SET script_path = ?
        WHERE id = ?""", (path, algorithm_configuration_id))
        await self.__connection.commit()

    @db_action
    async def get_all_parameters(self, algorithm_configuration_id: str) -> list[tuple[str, str]]:
        """Return all parameters of the given algorithm_configuration id."""
        async with self.__connection.execute("""SELECT parameter_name,
        cross_section_id FROM parameter WHERE algorithm_configuration_id = ?""",
                                             [algorithm_configuration_id]) as cursor:
            result = await cursor.fetchall()
            if result is None:
                return []
            return list(result)  # type: ignore

    @db_action
    async def get_parameter_value(self, algorithm_configuration_id: str, parameter_name: str,
                                  cross_section_id: str | None) -> GLib.Variant | None:
        """Return the value of the parameter of the given algorithm configuration
        and parameter and possibly cross section."""
        if cross_section_id is None:
            async with self.__connection.execute("""SELECT value FROM parameter
            WHERE algorithm_configuration_id = ? AND name = ? AND cross_section_id IS Null""",
                                                 (algorithm_configuration_id, parameter_name)
                                                 ) as cursor:
                result = await cursor.fetchone()
                if result is None:
                    return None
                return GLib.Variant.parse(None, list(result)[0])
        else:
            async with self.__connection.execute("""SELECT value FROM parameter
            WHERE algorithm_configuration_id = ? AND name = ? AND cross_section_id = ?""",
                                                 (algorithm_configuration_id, parameter_name,
                                                  cross_section_id)) as cursor:
                result = await cursor.fetchone()
                if result is None:
                    return None
                return GLib.Variant.parse(None, list(result)[0])

    @db_action
    async def set_parameter_value(self, algorithm_configuration_id: str, parameter_name: str,
                                  cross_section_id: str | None,
                                  parameter_value: GLib.Variant) -> None:
        """Update the value of the parameter of the given algorithm configuration,
        parameter name and cross section."""
        if cross_section_id is None:
            await self.__connection.execute("""UPDATE parameter SET value = ?
            WHERE algorithm_configuration_id = ? AND name = ? AND cross_section_id IS NULL""",
                                            (parameter_value.print_(True),
                                             algorithm_configuration_id, parameter_name))
        else:
            await self.__connection.execute("""UPDATE parameter SET value = ?
                        WHERE algorithm_configuration_id = ? AND name = ?
                        AND cross_section_id = ?""", (parameter_value.print_(True),
                                                      algorithm_configuration_id,
                                                      parameter_name, cross_section_id))
        await self.__connection.commit()

    @db_action
    async def add_cross_section(self, cross_section_id: str, name: str,
                                hard_shoulder_active: bool, b_display_active: bool) -> None:
        """Add a new cross section with an id, a name and whether the hard shoulder
        or b display are active."""
        await self.__connection.execute("""
        INSERT INTO cross_section (id, name, hard_shoulder_active, b_display_active)
        VALUES (?, ?, ?, ?)""", (cross_section_id, name, hard_shoulder_active,
                                 b_display_active))
        await self.__connection.commit()

    @db_action
    async def remove_cross_section(self, cross_section_id: str) -> None:
        """Remove a cross section from the database."""
        await self.__connection.execute("""DELETE FROM cross_section WHERE id = ?""",
                                        [cross_section_id])
        await self.__connection.commit()

    @db_action
    async def add_algorithm_configuration(self, algorithm_configuration_id: str, name: str,
                                          evaluation_interval: int, display_interval: int,
                                          script_path: str, is_selected: bool = True) -> None:
        """Add a new algorithm configuration to the database."""
        await self.__connection.execute("""PRAGMA foreign_keys = ON""")
        if is_selected:
            await self.__connection.execute("""UPDATE algorithm_configuration
            SET is_selected = 0""")
            await self.__connection.commit()

        await self.__connection.execute("""
        INSERT INTO algorithm_configuration (id, name, evaluation_interval, display_interval,
        script_path, is_selected) VALUES (?, ?, ?, ?, ?, ?)""",
                                        (algorithm_configuration_id, name,
                                         evaluation_interval,
                                         display_interval,
                                         script_path, is_selected))
        await self.__connection.commit()

    @db_action
    async def remove_algorithm_configuration(self, algorithm_configuration_id: str) -> None:
        """Remove a algorithm configuration from the database."""
        await self.__connection.execute("""DELETE FROM algorithm_configuration WHERE id = ?""",
                                        [algorithm_configuration_id])
        await self.__connection.commit()

    @db_action
    async def add_parameter(self, algorithm_configuration_id: str, name: str,
                            cross_section_id: str | None, value: GLib.Variant) -> None:
        """Add a new parameter from the given algorithm configuration and parameter."""
        await self.__connection.execute("""PRAGMA foreign_keys = ON""")
        await self.__connection.execute("""INSERT INTO parameter (algorithm_configuration_id,
        name,  cross_section_id, value) VALUES (?, ?, NULL, ?)""",
                                        (algorithm_configuration_id, name, value.print_(True)))
        await self.__connection.commit()

    @db_action
    async def remove_parameter(self, algorithm_configuration_id: str, name: str,
                               cross_section_id: str | None) -> None:
        """Remove a parameter with the given algorithm configuration and parameter name
        and possibly cross section."""
        if cross_section_id is None:
            await self.__connection.execute("""DELETE FROM parameter
            WHERE algorithm_configuration_id = ? AND name = ? AND cross_section_id IS NULL""",
                                            (algorithm_configuration_id, name))
        else:
            await self.__connection.execute("""DELETE FROM parameter
                        WHERE algorithm_configuration_id = ? AND name = ?
                        AND cross_section_id = ?""", (algorithm_configuration_id,
                                                      name, cross_section_id))
        await self.__connection.commit()

    @db_action
    async def add_tag(self, tag_id: str, name: str) -> None:
        """Add a new tag to the database."""
        await self.__connection.execute("""INSERT INTO tag (id, name) VALUES (?, ?)""",
                                        (tag_id, name))
        await self.__connection.commit()

    @db_action
    async def remove_tag(self, tag_id: str) -> None:
        """Remove a tag from the database."""
        await self.__connection.execute("""DELETE FROM tag WHERE id = ?""", [tag_id])
        await self.__connection.commit()

    @db_action
    async def get_tag_name(self, tag_id: str) -> str | None:
        """Return the name of the given tag_id."""
        async with self.__connection.execute("""
        SELECT name FROM tag WHERE id = ?""", [tag_id]) as cursor:
            result = list(await cursor.fetchall())
            if result is None:
                return None
            return str(result[0][0])

    @db_action
    async def add_parameter_tag(self, parameter_tag_id: str, parameter_name: str,
                                algorithm_configuration_id: str,
                                cross_section_id: str | None, tag_id: str) -> None:
        """Add a new parameter tag entry which represents a tag
        belonging to the given parameter."""
        await self.__connection.execute("""PRAGMA foreign_keys = ON""")
        await self.__connection.execute("""INSERT INTO parameter_tag (id, parameter_name,
        algorithm_configuration_id, cross_section_id, tag_id)
        VALUES (?, ?, ?, ?, ?)""", (parameter_tag_id, parameter_name,
                                    algorithm_configuration_id, cross_section_id, tag_id))
        await self.__connection.commit()

    @db_action
    async def remove_parameter_tag(self, parameter_tag_id: str) -> None:
        """Remove a parameter tag entry."""
        await self.__connection.execute("""DELETE FROM parameter_tag WHERE id = ?""",
                                        [parameter_tag_id])
        await self.__connection.commit()

    @db_action
    async def get_all_tags(self) -> list[tuple[str, str]]:
        """Return the id and name for all tags in this project."""
        async with self.__connection.execute("""
        SELECT * FROM tag""") as cursor:
            res = await cursor.fetchall()
            if res is None:
                return []
            return res

    @db_action
    async def get_all_tag_ids_for_parameter(self, algorithm_configuration_id: str,
                                            parameter_name: str,
                                            cross_section_id: str | None) -> list[str]:
        """Return all tag ids belonging to the given parameter."""
        if cross_section_id is None:
            async with self.__connection.execute("""SELECT tag_id FROM parameter_tag
                WHERE parameter_name = ? AND algorithm_configuration_id = ?
                AND cross_section_id IS NULL""", (parameter_name,
                                                  algorithm_configuration_id)) as cursor:
                result_cursor = await cursor.fetchall()
                result = map(lambda x: x[0], result_cursor)
                if result is None:
                    return []
                return list(result)
        else:
            async with self.__connection.execute("""SELECT tag_id FROM parameter_tag
                WHERE algorithm_configuration_id = ? AND parameter_name = ?
                AND cross_section_id = ?""", (algorithm_configuration_id, parameter_name,
                                              cross_section_id)) as cursor:
                result_cursor = await cursor.fetchall()
                result = map(lambda x: x[0], result_cursor)
                if result is None:
                    return []
                return list(result)
