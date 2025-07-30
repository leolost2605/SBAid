"""This module contains unit tests for the result diagrams."""
import unittest
from sbaid.model.results.result import Result
from sbaid.model.results.heatmap_generator import HeatmapGenerator
from sbaid.model.results.snapshot import Snapshot
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot
from sbaid.model.results.lane_snapshot import LaneSnapshot
from sbaid.model.results.vehicle_snapshot import VehicleSnapshot
from sbaid.common.image_format import ImageFormat
from sbaid.common.b_display import BDisplay
from sbaid.common.a_display import ADisplay
from sbaid.common.vehicle_type import VehicleType
import random
from gi.repository import GLib


class DiagramTest(unittest.TestCase):
    """This class tests the generating of result diagrams."""
    def test_random_data_heatmap(self):
        generator = HeatmapGenerator()
        diagram_data = []
        for i in range(200):
            row = []
            for j in range(20):
                a = random.uniform(0, 140)
                row.append(a)
            diagram_data.append(row)
        cross_sections = []
        for i in range(20):
            cross_sections.append("MQ%d"%i)
        timestamps = []
        for i in range(200):
            if i%50 == 0:
                timestamps.append("time: %d" % i)
            else:
                timestamps.append("")

        date = GLib.DateTime.new_utc(2025, 7, 22, 13, 16, 45)
        print(self.generate_random_result()[0].snapshots)
        print(self.generate_random_result()[1])
        generator.get_diagram(self.generate_random_result()[0], self.generate_random_result()[1], ImageFormat.PNG)

    def generate_random_result(self) -> tuple[Result, list]:
        now = GLib.DateTime.new_now_local()
        test_id = GLib.uuid_string_random()
        test_name = "my_project"
        result = Result(test_id, test_name, now)
        cross_section_ids: list[str] = []

        for i in range(50):
            minute = (30 + i) % 60
            hour = 15 + ((30 + i) // 60)
            time = GLib.DateTime.new(tz=GLib.TimeZone.new_local(), year=2025, month=7, day=24, hour=hour, minute=minute,
                                     seconds=0)
            snapshot = Snapshot(GLib.uuid_string_random(), time)
            for m in range(10):
                if m == 4:
                    cross_section_id = "test_id"
                    cross_section_ids.append(cross_section_id)
                else:
                    cross_section_id = GLib.uuid_string_random()
                    cross_section_ids.append(cross_section_id)

                cross_section_snapshot = CrossSectionSnapshot(GLib.uuid_string_random(),
                                                              cross_section_id,
                                                              "Julia",
                                                              cross_section_id,
                                                              random.choice(list(BDisplay)))
                for p in range(6):
                    lane_snapshot = LaneSnapshot(GLib.uuid_string_random(),
                                                                 GLib.uuid_string_random(), p,
                                                                 random.uniform(60, 140),
                                                                 random.randint(5, 30),
                                                                 random.choice(list(ADisplay)))

                    for q in range(random.randint(1, 9)):
                        vehicle_snapshot_1 = VehicleSnapshot(GLib.uuid_string_random(),
                                                             random.choice(list(VehicleType)), random.uniform(60, 140))
                        lane_snapshot.add_vehicle_snapshot(vehicle_snapshot_1)

                    cross_section_snapshot.add_lane_snapshot(lane_snapshot)
                snapshot.add_cross_section_snapshot(cross_section_snapshot)
            result.add_snapshot(snapshot)

        return result, cross_section_ids