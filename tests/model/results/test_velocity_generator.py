import unittest
import random
from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay
from sbaid.common.image_format import ImageFormat
from sbaid.common.vehicle_type import VehicleType
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot
from sbaid.model.results.lane_snapshot import LaneSnapshot
from sbaid.model.results.result import Result
from sbaid.model.results.snapshot import Snapshot
from sbaid.model.results.vehicle_snapshot import VehicleSnapshot
from sbaid.model.results.velocity_generator import VelocityGenerator
from gi.repository import GLib

class VelocityGeneratorTest(unittest.TestCase):
    generator = VelocityGenerator()
    cs_id = "test_id"

    def test_generate_diagram(self):
        result = self.generate_random_result()

        png_image = self.generator.get_diagram(result, "test_id", ImageFormat.PNG)
        png_image.save_to_file(r"C:\Users\PC\Projects\SBAid\tests\model\results\generator_outputs\diagram.png")

        svg_image = self.generator.get_diagram(result, "test_id", ImageFormat.SVG)
        svg_image.save_to_file(r"C:\Users\PC\Projects\SBAid\tests\model\results\generator_outputs\diagram.svg")

    def generate_random_result(self) -> Result:
        now = GLib.DateTime.new_now_local()
        test_id = GLib.uuid_string_random()
        test_name = "my_project"
        result = Result(test_id, test_name, now)

        for i in range(20):
            minute = (30 + i) % 60
            hour = 15 + ((30 + i) // 60)
            time = GLib.DateTime.new(tz=GLib.TimeZone.new_local(), year=2025, month=7, day=24, hour=hour, minute = minute, seconds=0)
            snapshot = Snapshot(GLib.uuid_string_random(), time)
            for m in range(10):
                if m == 4:
                    crosssectionid = self.cs_id
                else:
                    crosssectionid = GLib.uuid_string_random()

                cross_section_snapshot = CrossSectionSnapshot(GLib.uuid_string_random(),
                                                              crosssectionid,
                                                              "Julia",
                                                      random.choice(list(BDisplay)))
                for p in range(6):
                    lane_snapshot = lane_snapshot = LaneSnapshot(GLib.uuid_string_random(),
                                     GLib.uuid_string_random(), p,
                                       70.6 + (i / 4), random.randint(1, 9), random.choice(list(ADisplay)))

                    for q in range(random.randint(1, 9)):
                        vehicle_snapshot_1 = VehicleSnapshot(GLib.uuid_string_random(), random.choice(list(VehicleType)), random.uniform(60, 140))
                        lane_snapshot.add_vehicle_snapshot(vehicle_snapshot_1)

                    cross_section_snapshot.add_lane_snapshot(lane_snapshot)
                snapshot.add_cross_section_snapshot(cross_section_snapshot)
            result.add_snapshot(snapshot)

        return result