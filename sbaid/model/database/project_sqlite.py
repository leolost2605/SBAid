"""This module contains the ProjectSQLite class."""
import sqlite3

import aiosqlite
from gi.repository import GLib, Gio

from sbaid.model.database.foreign_key_error import ForeignKeyError
from sbaid.common import make_directory_with_parents_async
from sbaid.model.database.project_database import ProjectDatabase


class ProjectSQLite(ProjectDatabase):
    """This class implements the ProjectDatabase interface which allows for the
    project specific data to be stored."""
    _file: Gio.File
    _connection: aiosqlite.Connection
    _creation_time: GLib.DateTime

    def __init__(self, file: Gio.File) -> None:
        self._file = file
        self._creation_time = GLib.DateTime.new_now_local()  # type: ignore

    async def __aenter__(self) -> ProjectDatabase:
        if not self._file.query_exists():
            await make_directory_with_parents_async(self._file.get_parent())
            self._file.create_async(Gio.FileCreateFlags.NONE,  # pylint: disable=no-member
                                    GLib.PRIORITY_DEFAULT)
        self._connection = await aiosqlite.connect(str(self._file.get_path()))
        await self._connection.executescript("""PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS meta_information;
DROP TABLE IF EXISTS algorithm_configuration;
DROP TABLE IF EXISTS cross_section;
DROP TABLE IF EXISTS parameter;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS parameter_tag;

CREATE TABLE meta_information(
    name TEXT,
    created_at TEXT,
    last_modified TEXT
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
    name TEXT
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
        REFERENCES parameter(algorithm_configuration_id, name, cross_section_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE
);""")
        await self._connection.execute("""
        INSERT INTO meta_information (name, created_at, last_modified) VALUES
        (?, ?, ?)""", ("", GLib.DateTime.format_iso8601(self._creation_time),
                       GLib.DateTime.format_iso8601(  # pylint: disable=no-member
                           GLib.DateTime.new_now_local())))  # type: ignore
        await self._connection.commit()
        return self

    async def __aexit__(self, exc_type: Exception, exc_val: Exception, exc_tb: Exception) -> None:
        await self._connection.close()

    async def get_created_at(self) -> GLib.DateTime:
        """Return the GLib.DateTime when the project was created."""

        async with (self._connection.execute("""SELECT created_at FROM meta_information""")
                    as cursor):
            date = await cursor.fetchone()
            if date is None:
                raise KeyError("The project was not created properly.")
            return GLib.DateTime.new_from_iso8601(date[0])    # pylint: disable=no-member

    async def get_last_modified(self) -> GLib.DateTime:
        """Return the GLib.DateTime when the project was last modified."""
        async with (self._connection.execute("""SELECT last_modified FROM meta_information""")
                    as cursor):
            date = await cursor.fetchone()
            if date is None:
                raise KeyError("The project was not modified properly.")
            return GLib.DateTime.new_from_iso8601(date[0])  # pylint: disable=no-member

    async def set_last_modified(self, new_last_modified: GLib.DateTime) -> None:
        """Update the GLib.DateTime when the project was last modified."""
        await self._connection.execute("""UPDATE meta_information SET last_modified = ?""",
                                       [new_last_modified.format_iso8601()])
        await self._connection.commit()

    async def get_project_name(self) -> str:
        """Return the name of the project."""
        async with self._connection.execute("""SELECT name FROM meta_information""") as cursor:
            result_list = await cursor.fetchone()
            return str(result_list[0])  # type: ignore

    async def set_project_name(self, name: str) -> None:
        """Update the name of the project."""
        await self._connection.execute("""UPDATE meta_information SET name = ?""", [name])
        await self._connection.commit()

    async def get_cross_section_name(self, cross_section_id: str) -> str:
        """Return the name of the cross_section with the given id."""
        async with self._connection.execute("""SELECT name FROM cross_section WHERE id = ?""",
                                            [cross_section_id]) as cursor:
            result = await cursor.fetchone()
            if result is None:
                return ""
            return str(list(result)[0])

    async def set_cross_section_name(self, cross_section_id: str, name: str) -> None:
        """Update the name of the cross_section with the given id."""
        await self._connection.execute("""UPDATE cross_section SET cross_section_name= ?,
        WHERE id = ?""", (name, cross_section_id))
        await self._connection.commit()

    async def get_algorithm_configuration_name(self, algorithm_configuration_id: str) -> str:
        """Return the name of the algorithm_configuration with the given id."""
        async with self._connection.execute("""SELECT name FROM algorithm_configuration
        WHERE id = ?""", [algorithm_configuration_id]) as cursor:
            result_list = await cursor.fetchone()
            return str(result_list[0])  # type: ignore

    async def set_algorithm_configuration_name(self, algorithm_configuration_id: str,
                                               name: str) -> None:
        """Update the name of the algorithm_configuration with the given id."""
        await self._connection.execute("""UPDATE algorithm_configuration SET name = ?
        WHERE id = ?""", (name, algorithm_configuration_id))
        await self._connection.commit()

    async def get_algorithm_configuration(self, algorithm_configuration_id: str)\
            -> tuple[str, str, int, int, str, bool]:
        """Return the algorithm_configuration with the given id."""
        async with self._connection.execute("""SELECT * FROM algorithm_configuration
        WHERE id = ?""", [algorithm_configuration_id]) as cursor:
            result_list = await cursor.fetchone()
            return str(result_list[0])  # type: ignore

    async def get_all_algorithm_configuration_ids(self) -> list[str]:
        """Return all algorithm_configuration ids."""
        async with (self._connection.execute("""SELECT id FROM algorithm_configuration""")
                    as cursor):
            return await cursor.fetchall()

    async def get_selected_algorithm_configuration_id(self) -> str:
        """Return the currently selected algorithm_configuration id."""
        async with self._connection.execute("""SELECT id FROM algorithm_configuration
        WHERE is_selected = 1""") as cursor:
            result = await cursor.fetchone()
            if result is None:
                return ""
            return str(list(result)[0])

    async def set_selected_algorithm_configuration_id(self, configuration_id: str) -> None:
        """Update the currently selected algorithm_configuration id."""
        await self._connection.execute("""UPDATE algorithm_configuration SET is_selected = 0""")
        await self._connection.execute("""UPDATE algorithm_configuration SET is_selected = 1
        WHERE id = ?""", [configuration_id])
        await self._connection.commit()

    async def get_display_interval(self, algorithm_configuration_id: str) -> int:
        """Return the display interval of the given algorithm_configuration id."""
        async with self._connection.execute("""SELECT display_interval FROM algorithm_configuration
        WHERE id = ?""", [algorithm_configuration_id]) as cursor:
            result_list = await cursor.fetchone()
            return int(result_list[0])  # type: ignore

    async def set_display_interval(self, algorithm_configuration_id: str, interval: int) -> None:
        """Update the display interval of the given algorithm_configuration id."""
        await self._connection.execute("""UPDATE algorithm_configuration SET display_interval = ?
        WHERE id = ?""", (interval, algorithm_configuration_id))
        await self._connection.commit()

    async def get_evaluation_interval(self, algorithm_configuration_id: str) -> int:
        """Return the evaluation interval of the given algorithm_configuration id."""
        async with self._connection.execute("""SELECT evaluation_interval
        FROM algorithm_configuration WHERE id = ?""", [algorithm_configuration_id]) as cursor:
            result_list = await cursor.fetchone()
            return int(result_list[0])  # type: ignore

    async def set_evaluation_interval(self, algorithm_configuration_id: str,
                                      interval: int) -> None:
        """Update the evaluation interval of the given algorithm_configuration id."""
        await self._connection.execute("""UPDATE algorithm_configuration
        SET evaluation_interval = ? WHERE id = ?""", (interval, algorithm_configuration_id))
        await self._connection.commit()

    async def get_script_path(self, algorithm_configuration_id: str) -> str:
        """Return the scrip path of the given algorithm_configuration id."""
        async with self._connection.execute("""SELECT script FROM algorithm_configuration
        WHERE id = ?""", [algorithm_configuration_id]) as cursor:
            result_list = await cursor.fetchone()
            return str(result_list[0])  # type: ignore

    async def set_script_path(self, algorithm_configuration_id: str, path: str) -> None:
        """Update the script path of the given algorithm_configuration id."""
        await self._connection.execute("""UPDATE algorithm_configuration SET script_path = ?
        WHERE id = ?""", (path, algorithm_configuration_id))
        await self._connection.commit()

    async def get_all_parameters(self, algorithm_configuration_id: str) -> list[tuple[str, str]]:
        """Return all parameters of the given algorithm_configuration id."""
        async with self._connection.execute("""SELECT parameter_name,
        cross_section_id FROM parameter WHERE algorithm_configuration_id = ?""",
                                            [algorithm_configuration_id]) as cursor:
            result = await cursor.fetchall()
            if result is None:
                return []
            return list(result)  # type: ignore

    async def get_parameter_value(self, algorithm_configuration_id: str, parameter_name: str,
                                  cross_section_id: str | None) -> GLib.Variant | None:
        """Return the value of the parameter of the given algorithm configuration
        and parameter and possibly cross section."""
        if cross_section_id is None:
            async with self._connection.execute("""SELECT value FROM parameter
            WHERE algorithm_configuration_id = ? AND name = ? AND cross_section_id IS Null""",
                                                (algorithm_configuration_id,
                                                 parameter_name)) as cursor:
                result = await cursor.fetchone()
                if result is None:
                    return None
                return GLib.Variant.parse(None, list(result)[0])
        else:
            async with self._connection.execute("""SELECT value FROM parameter
            WHERE algorithm_configuration_id = ? AND name = ? AND cross_section_id = ?""",
                                                (algorithm_configuration_id, parameter_name,
                                                 cross_section_id)) as cursor:
                result = await cursor.fetchone()
                if result is None:
                    return None
                return GLib.Variant.parse(None, list(result)[0])

    async def set_parameter_value(self, algorithm_configuration_id: str, parameter_name: str,
                                  cross_section_id: str | None,
                                  parameter_value: GLib.Variant) -> None:
        """Update the value of the parameter of the given algorithm configuration,
        parameter name and cross section."""
        if cross_section_id is None:
            await self._connection.execute("""UPDATE parameter SET value = ?
            WHERE algorithm_configuration_id = ? AND name = ? AND cross_section_id IS NULL""",
                                           (parameter_value.print_(True),
                                            algorithm_configuration_id, parameter_name))
        else:
            await self._connection.execute("""UPDATE parameter SET value = ?
                        WHERE algorithm_configuration_id = ? AND name = ?
                        AND cross_section_id = ?""", (parameter_value.print_(True),
                                                      algorithm_configuration_id,
                                                      parameter_name, cross_section_id))
        await self._connection.commit()

    async def add_cross_section(self, cross_section_id: str, name: str) -> None:
        """Add a new cross section with an id and a name."""
        await self._connection.execute("""INSERT INTO cross_section (id, name)
        VALUES (?, ?)""", (cross_section_id, name))
        await self._connection.commit()

    async def remove_cross_section(self, cross_section_id: str) -> None:
        """Remove a cross section from the database."""
        await self._connection.execute("""DELETE FROM cross_section WHERE id = ?""",
                                       [cross_section_id])
        await self._connection.commit()

    async def add_algorithm_configuration(self, algorithm_configuration_id: str, name: str,
                                          evaluation_interval: int, display_interval: int,
                                          script_path: str, is_selected: bool = True) -> None:
        """Add a new algorithm configuration to the database."""
        if is_selected:
            await self._connection.execute("""UPDATE algorithm_configuration
            SET is_selected = 0""")
            await self._connection.commit()

        await self._connection.execute("""
        INSERT INTO algorithm_configuration (id, name, evaluation_interval, display_interval,
        script_path, is_selected) VALUES (?, ?, ?, ?, ?, ?)""", (algorithm_configuration_id, name,
                                                                 evaluation_interval,
                                                                 display_interval,
                                                                 script_path, is_selected))
        await self._connection.commit()

    async def remove_algorithm_configuration(self, algorithm_configuration_id: str) -> None:
        """Remove a algorithm configuration from the database."""
        await self._connection.execute("""DELETE FROM algorithm_configuration WHERE id = ?""",
                                       [algorithm_configuration_id])
        await self._connection.commit()

    async def add_parameter(self, algorithm_configuration_id: str, name: str,
                            cross_section_id: str | None, value: GLib.Variant) -> None:
        """Add a new parameter from the given algorithm configuration and parameter."""
        try:
            await self._connection.execute("""INSERT INTO parameter (algorithm_configuration_id,
            name,  cross_section_id, value) VALUES (?, ?, NULL, ?)""",
                                           (algorithm_configuration_id, name, value.print_(True)))
            await self._connection.commit()
        except sqlite3.IntegrityError as e:
            raise ForeignKeyError("Foreign key does not exist!") from e

    async def remove_parameter(self, algorithm_configuration_id: str, name: str,
                               cross_section_id: str | None) -> None:
        """Remove a parameter with the given algorithm configuration and parameter name
        and possibly cross section."""
        if cross_section_id is None:
            await self._connection.execute("""DELETE FROM parameter
            WHERE algorithm_configuration_id = ? AND name = ? AND cross_section_id IS NULL""",
                                           (algorithm_configuration_id, name))
        else:
            await self._connection.execute("""DELETE FROM parameter
                        WHERE algorithm_configuration_id = ? AND name = ?
                        AND cross_section_id = ?""", (algorithm_configuration_id,
                                                      name, cross_section_id))
            await self._connection.commit()

    async def add_tag(self, tag_id: str, name: str) -> None:
        """Add a new tag to the database."""
        await self._connection.execute("""INSERT INTO tag (id, name) VALUES (?, ?)""",
                                       (tag_id, name))
        await self._connection.commit()

    async def remove_tag(self, tag_id: str) -> None:
        """Remove a tag from the database."""
        await self._connection.execute("""DELETE FROM tag WHERE id = ?""", [tag_id])
        await self._connection.commit()

    async def add_parameter_tag(self, parameter_tag_id: str, parameter_name: str,
                                algorithm_configuration_id: str,
                                cross_section_id: str | None, tag_id: str) -> None:
        """Add a new parameter tag entry which represents a tag
        belonging to the given parameter."""
        try:
            await self._connection.execute("""INSERT INTO parameter_tag (id, parameter_name,
            algorithm_configuration_id, cross_section_id, tag_id)
            VALUES (?, ?, ?, ?, ?)""", (parameter_tag_id, parameter_name,
                                        algorithm_configuration_id, cross_section_id, tag_id))
            await self._connection.commit()
        except sqlite3.IntegrityError as e:
            raise ForeignKeyError("Foreign key does not exist!") from e

    async def remove_parameter_tag(self, parameter_tag_id: str) -> None:
        """Remove a parameter tag entry."""
        await self._connection.execute("""DELETE FROM parameter_tag WHERE id = ?""",
                                       [parameter_tag_id])
        await self._connection.commit()

    async def get_all_tag_ids_for_parameter(self, algorithm_configuration_id: str,
                                            parameter_name: str,
                                            cross_section_id: str | None) -> list[str]:
        """Return all tag ids belonging to the given parameter."""
        try:
            if cross_section_id is None:
                async with self._connection.execute("""SELECT tag_id FROM parameter_tag
                    WHERE parameter_name = ? AND algorithm_configuration_id = ?
                    AND cross_section_id IS NULL""", (parameter_name,
                                                      algorithm_configuration_id)) as cursor:
                    result_cursor = await cursor.fetchall()
                    result = map(lambda x: x[0], result_cursor)
                    if result is None:
                        return []
                    return list(result)
            else:
                async with self._connection.execute("""SELECT tag_id FROM parameter_tag
                    WHERE algorithm_configuration_id = ? AND parameter_name = ?
                    AND cross_section_id = ?""", (algorithm_configuration_id, parameter_name,
                                                  cross_section_id)) as cursor:
                    result_cursor = await cursor.fetchall()
                    result = map(lambda x: x[0], result_cursor)
                    if result is None:
                        return []
                    return list(result)
        except sqlite3.IntegrityError as e:
            raise ForeignKeyError("Foreign key does not exist!") from e
