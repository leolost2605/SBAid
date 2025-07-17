"""TODO"""
import sqlite3

from gi.repository import GObject, GLib, Gio

from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay
from sbaid.common.simulator_type import SimulatorType
from sbaid.common.vehicle_type import VehicleType
from sbaid.model.database.global_database import GlobalDatabase


class GlobalSQLite(GObject.GObject):
    """TODO"""
    _connection: sqlite3.Connection

    def __init__(self):
        super().__init__()
        self.init_contents = ""


    async def open(self, file: Gio.File) -> None:
        path = file.get_path()
        if path is None:
            file.create(Gio.FileCreateFlags.NONE, None)
        path = file.get_path()

        self._connection = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

        sql_file = Gio.File.new_for_path(
            "/Users/fuchs/PycharmProjects/SBAid/sbaid/model/database/init_global_sqlite.txt")

        def _load_contents_callback(giofile, async_result: Gio.AsyncResult) -> None:
            print("Path: ", giofile.get_path())
            # try:
            success, content, etag = giofile.load_contents_finish(async_result)
            self.init_contents = content
            print(success)
            print(content)
            # except GLib.GError as error:
            #     print("Error: ", error)
            #     return

        sql_file.load_contents_async(None, _load_contents_callback, file)

        print("RESULT: ", self.init_contents)

    async def add_project(self, project_id: str, simulator_type: SimulatorType,
                    simulator_file_path: str, project_file_path: str) -> None:
        self._connection.cursor().execute("""
        INSERT INTO projects (project_id, simulator_type, simulator_file_path, project_file_path)
        """)

    async def get_all_projects(self) -> list[tuple[str, SimulatorType, str, str,]]:
        """TODO"""
        def func(db_input: tuple[str, str, str, str, str]) -> tuple[str, SimulatorType, str, str,]:
            return db_input[0], SimulatorType(db_input[1], db_input[2]), db_input[3], db_input[4]
        return list(map(func, self._connection.cursor().execute("""
        SELECT (project_id, simulator_type_id, simulator_type_name, simulator_file_path, project_file_path)
        FROM project
        """).fetchall()))

    async def remove_project(self, project_id: str) -> None:
        """TODO"""
        self._connection.cursor().execute("""
        DELETE FROM projects (project_id, simulator_type, simulator_file_path, project_file_path)
        """)

    async def get_all_results(self) -> list[tuple[str, GLib.DateTime]]:
        """TODO"""
        return self._connection.cursor().execute("""
        SELECT (project_id, simulator_type_id, simulator_type_name, simulator_file_path, project_file_path)
        FROM result
        """).fetchall()

    async def save_result(self, result_id: str, project_name: str,
                          creation_date_time: GLib.DateTime) -> None:
        """TODO"""


    async def delete_result(self, result_id: str) -> None:
        """TODO"""

    async def get_result_name(self, result_id: str) -> str:
        """TODO"""
        return ""

    async def get_all_tags(self) -> list[str]:
        """TODO"""
        return []

    async def get_result_tags(self, result_id: str) -> list[str]:
        """TODO"""
        return []

    async def get_all_snapshots(self, result_id: str) -> list[tuple[str, GLib.DateTime]]:
        """TODO"""
        return []

    async def save_snapshot(self, result_id: str, snapshot_id: str, time: GLib.DateTime) -> None:
        """TODO"""

    async def get_all_cross_section_snapshots(self, snapshot_id: str) -> list[tuple[str, str, BDisplay]]:
        """TODO"""
        return []

    async def save_cross_section_snapshot(self, snapshot_id: str, cross_section_snapshot_ic: str,
                                    time: GLib.DateTime) -> None:
        """TODO"""

    async def get_all_lane_snapshots(self, cross_section_snapshot_id: str)\
            -> list[tuple[str, int, float, int, ADisplay]]:
        """TODO"""
        return []

    async def save_lane_snapshot(self, cross_section_snapshot_id: str, lane_snapshot_id: str,
                           lane: int, average_speed: float, traffic_volume: int,
                           a_display: ADisplay) -> None:
        """TODO"""

    async def get_all_vehicle_snapshots(self, lane_snapshot_id: str) -> list[tuple[VehicleType, float]]:
        """TODO"""
        return []

    async def save_vehicle_snapshot(self, lane_snapshot_id: str,
                              vehicle_type: VehicleType, speed: float) -> None:
        """TODO"""
