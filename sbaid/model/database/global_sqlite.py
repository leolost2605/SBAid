"""TODO"""
import sqlite3

from gi.repository import GLib, Gio

from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay
from sbaid.common.simulator_type import SimulatorType
from sbaid.common.vehicle_type import VehicleType
from sbaid.model.database.global_database import GlobalDatabase


class GlobalSQLite(GlobalDatabase):
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
        self._connection = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES |
                                           sqlite3.PARSE_COLNAMES)
        self._connection.cursor().executescript("""DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS result;
DROP TABLE IF EXISTS result_tag;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS snapshot;
DROP TABLE IF EXISTS cross_section_snapshot;
DROP TABLE IF EXISTS lane_snapshot;
DROP TABLE IF EXISTS vehicle_snapshot;

CREATE TABLE project (
    id TEXT PRIMARY KEY,
    simulator_type_id TEXT,
    simulator_type_name TEXT,
    simulator_file_path TEXT,
    project_file_path TEXT
);
CREATE TABLE result (
    id TEXT PRIMARY KEY,
    name TEXT,
    project_name TEXT,
    date TEXT
);
CREATE TABLE result_tag (
    id TEXT PRIMARY KEY,
    tag_id TEXT,
    result_id TEXT,
    FOREIGN KEY (result_id) REFERENCES result (id),
    FOREIGN KEY (tag_id) REFERENCES tag (id)
);
CREATE TABLE tag (
    id TEXT PRIMARY KEY,
    name TEXT
);
CREATE TABLE snapshot (
    id TEXT PRIMARY KEY,
    result_id TEXT,
    date TEXT,
    FOREIGN KEY (result_id) REFERENCES result (id)
);
CREATE TABLE cross_section_snapshot (
    id TEXT PRIMARY KEY,
    snapshot_id TEXT,
    cross_section_name TEXT,
    b_display INT,
    FOREIGN KEY (snapshot_id) REFERENCES snapshot (id)
);
CREATE TABLE lane_snapshot (
    id TEXT PRIMARY KEY,
    cross_section_snapshot_id TEXT,
    lane_number INT,
    average_speed REAL,
    traffic_volume INT,
    a_display INT,
    FOREIGN KEY (cross_section_snapshot_id) REFERENCES cross_section_snapshot (id)
);
CREATE TABLE vehicle_snapshot (
    id TEXT PRIMARY KEY,
    lane_snapshot_id TEXT,
    vehicle_type INT,
    speed REAL,
    FOREIGN KEY (lane_snapshot_id) REFERENCES lane_snapshot (id)
);""")

    async def add_project(self, project_id: str, simulator_type: SimulatorType,
                          simulator_file_path: str, project_file_path: str) -> None:
        self._connection.cursor().execute("""
        INSERT INTO project (id, simulator_type_id, simulator_type_name,
        simulator_file_path, project_file_path)
        VALUES (?, ?, ?, ?, ?);
        """, (project_id, simulator_type.id, simulator_type.name,
              simulator_file_path, project_file_path))

    async def get_all_projects(self) -> list[tuple[str, SimulatorType, str, str,]]:
        """TODO"""
        def func(db_input: tuple[str, str, str, str, str]) -> tuple[str, SimulatorType, str, str,]:
            return db_input[0], SimulatorType(db_input[1], db_input[2]), db_input[3], db_input[4]
        return list(map(func, self._connection.cursor().execute("""
        SELECT * FROM project;
        """).fetchall()))

    async def remove_project(self, project_id: str) -> None:
        """TODO"""
        self._connection.cursor().execute("DELETE FROM project WHERE id = ?;", (project_id,))

    async def get_all_results(self) -> list[tuple[str, GLib.DateTime]]:
        """TODO"""
        def func(values: tuple[str, str, str, str]) -> tuple[str, GLib.DateTime]:
            return values[0], GLib.DateTime.new_from_iso8601(values[3])  # pylint:disable=no-member

        result = list(map(func, self._connection.cursor().execute("""
                SELECT * FROM result;""").fetchall()))
        return result

    async def add_result(self, result_id: str, result_name: str, project_name: str,
                         creation_date_time: GLib.DateTime) -> None:
        """TODO"""
        self._connection.cursor().execute("""
        INSERT INTO result (id, name, project_name, date)
        VALUES (?, ?, ?, ?);
        """, (result_id, result_name, project_name, creation_date_time.format_iso8601()))

    async def delete_result(self, result_id: str) -> None:
        """TODO"""
        self._connection.cursor().execute("""
        DELETE FROM result WHERE id = ?;
        """, (result_id,)).close()

    async def get_result_name(self, result_id: str) -> str:
        """TODO"""
        result: str = self._connection.cursor().execute("""
        SELECT name FROM result WHERE id = ?;
        """, (result_id,)).fetchone()
        return result[0]

    async def add_result_tag(self, result_tag_id: str, result_id: str,
                             tag_id: str, tag_name: str) -> None:
        """TODO"""
        self._connection.cursor().execute("""
        INSERT INTO tag (id, name) VALUES (?, ?);""", (tag_id, tag_name))
        new_result_tag_id = GLib.uuid_string_random()  # pylint: disable=no-value-for-parameter
        self._connection.cursor().execute("""
        INSERT INTO result_tag (id, result_id, tag_id) VALUES (?, ?, ?);""",
                                          (new_result_tag_id, result_id, tag_id))

    async def get_all_tags(self) -> list[tuple[str, str]]:
        """TODO"""
        return self._connection.cursor().execute("""
        SELECT * FROM tag';
        """).fetchall()

    async def get_result_tags(self, result_id: str) -> list[str]:
        """TODO"""
        return self._connection.cursor().execute("""
        SELECT tag_id FROM result_tag WHERE result_id = ?;
        """, (result_id,)).fetchall()

    async def get_all_snapshots(self, result_id: str) -> list[tuple[str, GLib.DateTime]]:
        """TODO"""
        def func(values: tuple[str, str, str]) -> tuple[str, GLib.DateTime]:
            return values[0], GLib.DateTime.new_from_iso8601(values[2])  # pylint:disable=no-member

        return list(map(func, self._connection.cursor().execute("""
        SELECT * FROM snapshot;""").fetchall()))

    async def add_snapshot(self, snapshot_id: str, result_id: str, time: GLib.DateTime) -> None:
        """TODO"""
        time_string = time.format_iso8601()
        self._connection.cursor().execute("""
        INSERT INTO snapshot (id, result_id, date)
        VALUES (?, ?, ?);
        """, (snapshot_id, result_id, time_string))

    async def get_all_cross_section_snapshots(self, snapshot_id: str)\
            -> list[tuple[str, str, BDisplay]]:
        """TODO"""
        def func(values: tuple[str, str, str, BDisplay]) -> tuple[str, str, BDisplay]:
            return values[0], values[1], values[3]
        return list(map(func, (self._connection.cursor().execute("""
        SELECT * FROM cross_section_snapshot WHERE snapshot_id = ?;
        """, (snapshot_id,)).fetchall())))  # TODO double check

    async def add_cross_section_snapshot(self, cross_section_snapshot_id: str, snapshot_id: str,
                                         cross_section_name: str, b_display: BDisplay) -> None:
        """TODO"""
        self._connection.cursor().execute("""
        INSERT INTO cross_section_snapshot (id, snapshot_id, cross_section_name, b_display)
        VALUES (?, ?, ?, ?);
        """, (cross_section_snapshot_id, snapshot_id, cross_section_name, b_display.value))

    async def get_all_lane_snapshots(self, cross_section_snapshot_id: str) -> list[
                                     tuple[str, int, float, int, ADisplay]]:
        """TODO"""
        def func(values: tuple[str, str, int, float, int, ADisplay])\
                -> tuple[str, int, float, int, ADisplay]:
            return values[0], values[2], values[3], values[4], values[5]
        return list(map(func, self._connection.cursor().execute("""
        SELECT * FROM lane_snapshot WHERE cross_section_snapshot_id = ?;
        """, (cross_section_snapshot_id,)).fetchall()))

    async def add_lane_snapshot(self, lane_snapshot_id: str, cross_section_snapshot_id: str,
                                lane: int, average_speed: float, traffic_volume: int,
                                a_display: ADisplay) -> None:
        """TODO"""
        self._connection.cursor().execute("""
        INSERT INTO lane_snapshot (id, cross_section_snapshot_id, lane_number,
        average_speed, traffic_volume, a_display) VALUES (?, ?, ?, ?, ?, ?);
        """, (lane_snapshot_id, cross_section_snapshot_id, lane, average_speed,
              traffic_volume, a_display.value))

    async def get_all_vehicle_snapshots(self, lane_snapshot_id: str)\
            -> list[tuple[VehicleType, float]]:
        """TODO"""
        return self._connection.cursor().execute("""
        SELECT * FROM vehicle_snapshot WHERE lane_snapshot_id = ?;
        """, (lane_snapshot_id,)).fetchall()

    async def add_vehicle_snapshot(self, lane_snapshot_id: str, vehicle_type:
                                   VehicleType, speed: float) -> None:
        """TODO"""
        self._connection.cursor().execute("""
        INSERT INTO vehicle_snapshot (?, ?, ?, ?);
        """, (GLib.uuid_string_random(),  # pylint:disable=no-value-for-parameter
              lane_snapshot_id, vehicle_type.value, speed))
