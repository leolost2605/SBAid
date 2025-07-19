"""TODO"""
import sqlite3

from gi.repository import GLib, Gio

from sbaid.model.database.project_database import ProjectDatabase


class ProjectSQLite(ProjectDatabase):
    """TODO"""
    _connection: sqlite3.Connection

    async def open(self, file: Gio.File) -> None:
        """TODO"""
        if not file.query_exists():
            file.create_async(Gio.FileCreateFlags.NONE, 0)  # pylint: disable=no-member
        else:
            raise FileExistsError("File already exists")
        path = file.get_path()
        if path is None:
            raise FileNotFoundError("Path is invalid")
        self._connection = sqlite3.connect(path)
        self._connection.executescript("""PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS meta_information
DROP TABLE IF EXISTS algorithm_configuration
DROP TABLE IF EXISTS cross_section
DROP TABLE IF EXISTS parameter
DROP TABLE IF EXISTS tag
DROP TABLE IF EXISTS parameter_tag

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
    is_selected BOOLEAN,
    ON DELETE CASCADE
);
CREATE TABLE cross_section (
    id TEXT PRIMARY KEY,
    name TEXT,
    ON DELETE CASCADE
);
CREATE TABLE parameter (
    parameter_id TEXT PRIMARY KEY,
    name TEXT,
    algorithm_configuration_id TEXT,
    cross_section_id TEXT,
    value BLOB,
    FOREIGN KEY (algorithm_configuration_id) REFERENCES algorithm_configuration(id)
    FOREIGN KEY (cross_section_id) REFERENCES cross_section(id),
    ON DELETE CASCADE
);
CREATE TABLE tag (
    id TEXT PRIMARY KEY,
    name TEXT,
    ON DELETE CASCADE
);
CREATE TABLE parameter_tag (
    parameter_id TEXT,
    tag_id TEXT
    PRIMARY KEY (parameter_id, tag_id)
    FOREIGN KEY (parameter_id) REFERENCES parameter(id)
    FOREIGN KEY (tag_id) REFERENCES tag(id)
);""")
        self._connection.execute("""
        INSERT INTO meta_information (name, created_at, last_modified) VALUES
        (?, ?, ?)""", ("", "0000-01-01T00:00:00", "0000-01-01T00:00:00"))

    async def get_created_at(self) -> GLib.DateTime:
        """TODO"""
        return GLib.DateTime.new_from_iso8601(self._connection.execute("""
        SELECT created_at FROM meta_information""").fetchone())

    async def get_last_modified(self) -> GLib.DateTime:
        """TODO"""
        return GLib.DateTime.new_from_iso8601(self._connection.execute("""
        SELECT last_modified FROM meta_information""").fetchone())

    async def set_last_modified(self, new_last_modified: GLib.DateTime) -> None:
        """TODO"""
        self._connection.execute("""
        UPDATE meta_information SET last_modified = ?""", [new_last_modified.format_iso8601()])

    async def get_project_name(self) -> str:
        """TODO"""
        return self._connection.execute("""
        SELECT name FROM meta_information""").fetchone()

    async def set_project_name(self, name: str) -> None:
        """TODO"""
        self._connection.execute("""
        UPDATE meta_information SET name = ?""", [name])

    async def get_cross_section_name(self, cross_section_id: str) -> str:
        """TODO"""
        return self._connection.execute("""
        SELECT name FROM cross_section WHERE id = ?""",
                                        [cross_section_id]).fetchone()

    async def set_cross_section_name(self, cross_section_id: str, name: str) -> None:
        """TODO"""
        self._connection.execute("""
        UPDATE cross_section SET cross_section_name= ?, WHERE id = ?""",
                                 (name, cross_section_id))

    async def get_algorithm_configuration_name(self, algorithm_configuration_id: str) -> str:
        """TODO"""
        return self._connection.execute("""
        SELECT name FROM algorithm_configuration WHERE id = ?""",
                                        [algorithm_configuration_id]).fetchone()

    async def set_algorithm_configuration_name(self, algorithm_configuration_id: str,
                                               name: str) -> None:
        """TODO"""
        self._connection.execute("""
        UPDATE algorithm_configuration SET name = ? WHERE id = ?""",
                                 (name, algorithm_configuration_id))

    async def get_algorithm_configuration(self, algorithm_configuration_id: str)\
            -> tuple[str, str, int, int, str, bool]:
        """TODO"""
        return self._connection.execute("""
        SELECT * FROM algorithm_configuration WHERE id = ?""",
                                        [algorithm_configuration_id]).fetchone()

    async def get_all_algorithm_configuration_ids(self) -> list[str]:
        """TODO"""
        return self._connection.execute("""
        SELECT id FROM algorithm_configuration""").fetchall()

    async def get_selected_algorithm_configuration_id(self) -> str:
        """TODO"""
        return self._connection.execute("""
        SELECT id FROM algorithm_configurationWHERE is_selected = 1""").fetchone()

    async def set_selected_algorithm_configuration_id(self, configuration_id: str) -> None:
        """TODO"""
        self._connection.execute("""
        UPDATE algorithm_configuration SET is_selected = 0""")

        self._connection.execute("""
        UPDATE algorithm_configuration SET is_selected = 1 WHERE id = ?""",
                                 [configuration_id])

    async def get_display_interval(self, algorithm_configuration_id: str) -> int:
        """TODO"""
        return self._connection.execute("""
        SELECT display_interval FROM algorithm_configuration
        WHERE id = ?""").fetchone()

    async def set_display_interval(self, algorithm_configuration_id: str, interval: int) -> None:
        """TODO"""
        self._connection.execute("""
        UPDATE algorithm_configuration SET display_interval = ?
        WHERE id = ?""", (interval, algorithm_configuration_id))

    async def get_evaluation_interval(self, algorithm_configuration_id: str) -> int:
        """TODO"""
        return self._connection.execute("""
        SELECT evaluation_interval FROM algorithm_configuration
        WHERE id = ?""", [algorithm_configuration_id]).fetchone()

    async def set_evaluation_interval(self, algorithm_configuration_id: str, interval: int) -> None:
        """TODO"""
        self._connection.execute("""
        UPDATE algorithm_configuration SET evaluation_interval = ?
        WHERE id = ?""", (interval, algorithm_configuration_id))

    async def get_script_path(self, algorithm_configuration_id: str) -> str:
        """TODO"""
        return self._connection.execute("""
        SELECT script_path FROM algorithm_configuration
        WHERE id = ?""", [algorithm_configuration_id]).fetchone()

    async def set_script_path(self, algorithm_configuration_id: str, path: str) -> None:
        """TODO"""
        self._connection.execute("""
        UPDATE algorithm_configuration SET script_path = ?
        WHERE id = ?""", [path, algorithm_configuration_id])

    async def get_parameter_value(self, algorithm_configuration_id: str, parameter_name: str,
                                  cross_section_id: str | None) -> str:
        """TODO"""
        # null is dealt with automatically
        return self._connection.execute("""
        SELECT value FROM parameter
        WHERE id = ? AND cross_section_id = ?""", (cross_section_id, cross_section_id)).fetchone()

    async def set_parameter_value(self, parameter_id: str, parameter_value: GLib.Variant) -> None:
        """TODO"""
        self._connection.execute("""
        UPDATE parameter SET value = ? WHERE algorihtm_configuration_id = ?
        AND parameter_name = ?""", (parameter_value, parameter_id))

    async def add_cross_section(self, cross_section_id: str, name: str) -> None:
        """TODO"""
        self._connection.execute("""
        INSERT INTO cross_section (cross_section_id, name) VALUES (?, ?)""",
                                 (cross_section_id, name))

    async def remove_cross_section(self, cross_section_id: str) -> None:
        """TODO"""
        self._connection.execute("""
        DELETE FROM cross_section WHERE cross_section_id = ?""", [cross_section_id])

    async def add_algorithm_configuration(self, algorithm_configuration_id: str, name: str,
                                          evaluation_interval: int, display_interval: int,
                                          script_path: str, is_selected: bool) -> None:
        """TODO"""
        self._connection.execute("""
        INSERT INTO algorithm_configuration (id, name, evaluation_interval, display_interval,
        script_path, is_selected) VALUES (?, ?, ?, ?, ?, ?)""", (algorithm_configuration_id, name,
                                                                 evaluation_interval, display_interval,
                                                                 script_path, is_selected))

    async def remove_algorithm_configuration(self, algorithm_configuration_id: str) -> None:
        """TODO"""
        self._connection.execute("""
        DELETE FROM algorithm_configuration WHERE id = ?""", [algorithm_configuration_id])

    async def add_parameter(self, parameter_id: str, name: str, algorithm_configuration_id: str,
                            cross_section_id: str, value: GLib.Variant) -> None:
        """TODO"""
        self._connection.execute("""
        INSERT INTO parameter (id, name, algorithm_configuration_id, cross_section_id, value)
        VALUES (?, ?, ?, ?, ?)""", (parameter_id, name, algorithm_configuration_id,
                                    cross_section_id, value))

    async def remove_parameter(self, parameter_id: str) -> None:
        """TODO"""
        self._connection.execute("""
        DELETE FROM parameter WHERE id = ?""", [parameter_id])

    async def add_tag(self, tag_id: str, name: str):
        """TODO"""
        self._connection.execute("""
        INSERT INTO tag (id, name) VALUES (?, ?)""", (tag_id, name))

    async def remove_tag(self, tag_id: str) -> None:
        """TODO"""
        self._connection.execute("""
        DELETE FROM tag WHERE id = ?""", [tag_id])

    async def add_parameter_tag(self, parameter_tag_id: str, parameter_id: str, tag_id: str):
        """TODO"""
        self._connection.execute("""
        INSERT INTO parameter_tag (id, parameter_id, tag_id)
        VALUES (?, ?, ?)""", (parameter_tag_id, parameter_id, tag_id))

    async def remove_parameter_tag(self, parameter_tag_id: str) -> None:
        """TODO"""
        self._connection.execute("""
        DELETE FROM parameter WHERE id = ?""", [parameter_tag_id])

