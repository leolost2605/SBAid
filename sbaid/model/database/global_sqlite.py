# mypy: disable-error-code="func-returns-value, arg-type, no-any-return"
"""This module contains the GLobalSQLite class."""
import aiosqlite

from gi.repository import GLib, Gio

from sbaid.common import make_directory_with_parents_async
from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay
from sbaid.common.simulator_type import SimulatorType
from sbaid.common.vehicle_type import VehicleType
from sbaid.model.database.global_database import GlobalDatabase


class GlobalSQLite(GlobalDatabase):
    """This class implements the GlobalDatabase interface which allows for the all results
    and project metadata to be stored."""
    _file: Gio.File
    _db_path: str
    _connection: aiosqlite.Connection

    def __init__(self, file: Gio.File) -> None:
        self._file = file
        self._db_path = str(file.get_path())

    async def __aenter__(self) -> GlobalDatabase:
        if not self._file.query_exists():
            await make_directory_with_parents_async(self._file.get_parent())
            self._file.create(Gio.FileCreateFlags.NONE)  # pylint: disable=no-member
        self._connection = await aiosqlite.connect(self._db_path)
        async with aiosqlite.connect(self._db_path) as db:
            await db.executescript("""PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS project;
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
    FOREIGN KEY (result_id) REFERENCES result (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tag (id) ON DELETE CASCADE
);
CREATE TABLE tag (
    id TEXT PRIMARY KEY,
    name TEXT
);
CREATE TABLE snapshot (
    id TEXT PRIMARY KEY,
    result_id TEXT,
    date TEXT,
    FOREIGN KEY (result_id) REFERENCES result (id) ON DELETE CASCADE
);
CREATE TABLE cross_section_snapshot (
    id TEXT PRIMARY KEY,
    snapshot_id TEXT,
    cross_section_name TEXT,
    b_display INT,
    FOREIGN KEY (snapshot_id) REFERENCES snapshot (id) ON DELETE CASCADE
);
CREATE TABLE lane_snapshot (
    id TEXT PRIMARY KEY,
    cross_section_snapshot_id TEXT,
    lane_number INT,
    average_speed REAL,
    traffic_volume INT,
    a_display INT,
    FOREIGN KEY (cross_section_snapshot_id) REFERENCES cross_section_snapshot (id) ON DELETE CASCADE
);
CREATE TABLE vehicle_snapshot (
    id TEXT PRIMARY KEY,
    lane_snapshot_id TEXT,
    vehicle_type INT,
    speed REAL,
    FOREIGN KEY (lane_snapshot_id) REFERENCES lane_snapshot (id) ON DELETE CASCADE
);""")
            await db.commit()
            return self

    async def __aexit__(self, exc_type: Exception, exc_val: Exception, exc_tb: Exception) -> None:
        await self._connection.close()

    async def add_project(self, project_id: str, simulator_type: SimulatorType,
                          simulator_file_path: str, project_file_path: str) -> None:
        """Add a project to the database."""
        await self._connection.execute("""
        INSERT INTO project (id, simulator_type_id, simulator_type_name,
        simulator_file_path, project_file_path)
        VALUES (?, ?, ?, ?, ?);
        """, (project_id, simulator_type.id, simulator_type.name,
              simulator_file_path, project_file_path))
        await self._connection.commit()

    async def get_all_projects(self) -> list[tuple[str, SimulatorType, str, str,]]:
        """Return meta-information about all projects in the database."""
        async with self._connection.execute("""SELECT * FROM project;""") as cursor:
            return list(map(lambda x: (x[0], SimulatorType(x[1], x[2]), x[3], x[4]),
                            list(await cursor.fetchall())))

    async def remove_project(self, project_id: str) -> None:
        """Remove a project from the database."""
        await self._connection.execute("""DELETE FROM project WHERE id = ?;""", [project_id])
        await self._connection.commit()

    async def get_all_results(self) -> list[tuple[str, GLib.DateTime]]:
        """Return all results in the database."""
        async with self._connection.execute("""SELECT id, date FROM result;""") as cursor:
            return list(map(lambda x: (x[0], GLib.DateTime  # pylint:disable=no-member
                                       .new_from_iso8601(x[1])  # pylint:disable=no-member
                                       ),
                            await cursor.fetchall()))

    async def add_result(self, result_id: str, result_name: str, project_name: str,
                         creation_date_time: GLib.DateTime) -> None:
        """Add a result to the database."""
        await self._connection.execute("""
        INSERT INTO result (id, name, project_name, date)
        VALUES (?, ?, ?, ?);
        """, (result_id, result_name, project_name, creation_date_time.format_iso8601()))
        await self._connection.commit()

    async def delete_result(self, result_id: str) -> None:
        """Remove a result and all sub-results from the database."""
        await self._connection.execute("""
        DELETE FROM result WHERE id = ?;
        """, [result_id])
        await self._connection.commit()

    async def get_result_name(self, result_id: str) -> str:
        """Return the name of the given result_id from the database."""
        async with self._connection.execute("""
        SELECT name FROM result WHERE id = ?;
        """, [result_id]) as cursor:
            return str(list(await cursor.fetchall())[0][0])

    async def add_tag(self, tag_id: str, tag_name: str) -> None:
        """Add a tag to the database."""
        await self._connection.execute("""
        INSERT INTO tag (id, name) VALUES (?, ?)""", (tag_id, tag_name))
        await self._connection.commit()

    async def remove_tag(self, tag_id: str) -> None:
        """Remove a tag from the database."""
        await self._connection.execute("""
        DELETE FROM tag WHERE id = ?;""", (tag_id,))
        await self._connection.commit()

    async def add_result_tag(self, result_tag_id: str, result_id: str, tag_id: str) -> None:
        """Add a tag to a result."""""
        async with self._connection.execute("""
        SELECT * FROM tag WHERE id = ?;""", (tag_id,)) as cursor:
            tags = list(await cursor.fetchall())

        if len(tags) == 0:
            raise KeyError("Tag id is invalid")

        async with self._connection.execute("""
        SELECT * FROM result WHERE id = ?;""", (result_id,)) as cursor:
            results = list(await cursor.fetchall())

        if len(results) == 0:
            raise KeyError("Result id is invalid")

        await self._connection.execute("""
        INSERT INTO result_tag (id, result_id, tag_id) VALUES (?, ?, ?);""",
                                       (result_tag_id, result_id, tag_id))
        await self._connection.commit()

    async def get_all_tags(self) -> list[tuple[str, str]]:
        """Return all tags in the database."""
        async with self._connection.execute("""SELECT * FROM tag';""") as cursor:
            return await cursor.fetchall()

    async def get_result_tags(self, result_id: str) -> list[str]:
        """Return all tags that belong to the given result."""
        async with self._connection.execute("""SELECT tag_id FROM result_tag WHERE result_id = ?;
        """, (result_id,)) as cursor:
            return await cursor.fetchall()

    async def get_all_snapshots(self, result_id: str) -> list[tuple[str, GLib.DateTime]]:
        """Return all snapshots from a given result."""
        async with self._connection.execute("""SELECT id, date FROM snapshot;""") as cursor:
            values = await cursor.fetchall()
            return list(
                map(lambda x: (x[0], GLib.DateTime  # pylint:disable=no-member
                               .new_from_iso8601(x[1])), values))  # pylint:disable=no-member

    async def add_snapshot(self, snapshot_id: str, result_id: str, time: GLib.DateTime) -> None:
        """Add a snapshot to a given result."""
        time_string = time.format_iso8601()
        await self._connection.execute("""
        INSERT INTO snapshot (id, result_id, date)
        VALUES (?, ?, ?);
        """, (snapshot_id, result_id, time_string))
        await self._connection.commit()

    async def get_all_cross_section_snapshots(self, snapshot_id: str) \
            -> list[tuple[str, str, BDisplay]]:
        """Return all cross section snapshots from a given snapshot."""
        async with self._connection.execute("""
        SELECT id, snapshot_id, b_display FROM cross_section_snapshot WHERE snapshot_id = ?;
        """, [snapshot_id]) as cursor:
            return await cursor.fetchall()

    async def add_cross_section_snapshot(self, cross_section_snapshot_id: str, snapshot_id: str,
                                         cross_section_name: str, b_display: BDisplay) -> None:
        """Add a cross section snapshot to a given snapshot."""
        await self._connection.execute("""
        INSERT INTO cross_section_snapshot (id, snapshot_id, cross_section_name, b_display)
        VALUES (?, ?, ?, ?);
        """, (cross_section_snapshot_id, snapshot_id, cross_section_name, b_display.value))
        await self._connection.commit()

    async def get_all_lane_snapshots(self, cross_section_snapshot_id: str) -> list[
                                     tuple[str, int, float, int, ADisplay]]:
        """Return all lane snapshots from a given cross section snapshot."""
        async with self._connection.execute("""
        SELECT id, lane_number, average_speed, traffic_volume, a_display
        FROM lane_snapshot WHERE cross_section_snapshot_id = ?;
        """, (cross_section_snapshot_id,)) as db_cursor:
            return await db_cursor.fetchall()

    async def add_lane_snapshot(self, lane_snapshot_id: str, cross_section_snapshot_id: str,
                                lane: int, average_speed: float, traffic_volume: int,
                                a_display: ADisplay) -> None:
        """Add a lane snapshot to a given cross section snapshot."""
        await self._connection.execute("""
        INSERT INTO lane_snapshot (id, cross_section_snapshot_id, lane_number,
        average_speed, traffic_volume, a_display) VALUES (?, ?, ?, ?, ?, ?);
        """, (lane_snapshot_id, cross_section_snapshot_id, lane, average_speed,
              traffic_volume, a_display.value))
        await self._connection.commit()

    async def get_all_vehicle_snapshots(self, lane_snapshot_id: str) \
            -> list[tuple[VehicleType, float]]:
        """Return all vehicle snapshots from a given lane snapshot."""
        async with self._connection.execute("""
        SELECT * FROM vehicle_snapshot WHERE lane_snapshot_id = ?;
        """, (lane_snapshot_id,)) as cursor:
            return await cursor.fetchall()

    async def add_vehicle_snapshot(self, lane_snapshot_id: str, vehicle_type:
                                   VehicleType, speed: float) -> None:
        """Add a venicle snapshot to a given lane snapshot."""
        await self._connection.execute("""
        INSERT INTO vehicle_snapshot (?, ?, ?, ?);
        """, (GLib.uuid_string_random(),  # pylint:disable=no-value-for-parameter
              lane_snapshot_id, vehicle_type.value, speed))
        await self._connection.commit()
