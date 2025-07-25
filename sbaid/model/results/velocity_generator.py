"""This model defines the VelocityGenerator class"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
from sbaid.common.diagram_type import DiagramType
from sbaid.common.image import Image
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.cross_section_diagram_generator import CrossSectionDiagramGenerator
from sbaid.model.results.result import Result
from sbaid.model.results.seaborn_image import SeabornImage


class VelocityGenerator(CrossSectionDiagramGenerator):
    """todo"""

    diagram_name = "Velocity-Diagram"

    def get_diagram_type(self) -> DiagramType:  # pylint:disable=useless-parent-delegation
        """todo"""
        return super().get_diagram_type()

    def get_diagram(self, result: Result, cross_section_id: str,
                    export_format: ImageFormat) -> Image:

        self.__generate_diagram(self.__extract_data(result, cross_section_id))
        plt.savefig("out.png")
        image = SeabornImage()


    def __extract_data(self, result: Result, cross_section_id: str) -> DataFrame:
        """todo"""
        vehicle_speeds = []
        capture_timestamps = []
        vehicle_type = []

        for snapshot in result.snapshots:
            for cs_snapshot in snapshot.cross_section_snapshots:
                if cs_snapshot.cross_section_snapshot_id == cross_section_id:
                    for lane_snapshot in cs_snapshot.lane_snapshots:
                        for vehicle_snapshot in lane_snapshot.vehicle_snapshots:
                            vehicle_speeds.append(vehicle_snapshot.speed)
                            vehicle_type.append(vehicle_snapshot.vehicle_type)
                            capture_timestamps.append(snapshot.get_formated_timestamp())

        data = {
            "vehicle speeds": vehicle_speeds,
            "types": vehicle_type,
            "timestamps": capture_timestamps,
        }

        return pd.DataFrame(data)

    def __generate_diagram(self, data: DataFrame):
        """todo"""
        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots()

        ax.set_xlabel("Zeit")
        ax.set_ylabel("V[km/h]")
        ax.tick_params(axis='x', rotation=90)

        avg_data = data.groupby("timestamps", as_index=False)["vehicle speeds"].mean()

        sns.scatterplot(data=data, x="timestamps", y="vehicle speeds", hue="types", legend=False, ax=ax)
        sns.lineplot(data=avg_data, x="timestamps", y="vehicle speeds", legend=False, errorbar=None, linewidth=1.5,
                     color="#00008B", ax=ax)

        plt.show()