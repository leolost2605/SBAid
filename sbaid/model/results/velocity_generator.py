"""This model defines the VelocityGenerator class"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from pandas import DataFrame
from matplotlib.figure import Figure
from gi.repository import GLib
from sbaid.common.diagram_type import DiagramType
from sbaid.common.image import Image
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.cross_section_diagram_generator import CrossSectionDiagramGenerator
from sbaid.model.results.result import Result
from sbaid.model.results.seaborn_image import SeabornImage


class VelocityGenerator(CrossSectionDiagramGenerator):
    """Contains methods for generating the 'Velocity Diagram'.
    Velocity Diagrams map the speed of different vehicles measured at a given timepoint as a scatter plot.
    Different types of vehicles are differentiated with orange (lorry) and blue (car).
    A line-plot of the mean of the measured speeds is mapped in a dark blue. """

    diagram_name = "Velocity-Diagram"
    diagram_id = GLib.uuid_string_random()


    def get_diagram_type(self) -> DiagramType:  # pylint:disable=useless-parent-delegation
        """Returns the type of diagram."""
        return super().get_diagram_type()

    def get_diagram(self, result: Result, cross_section_id: str,
                    export_format: ImageFormat) -> Image:
        """Returns a SeabornImage class containing the bytes that make up the desired image."""
        data, filename = self.__extract_data(result, cross_section_id)

        fig = self.__generate_diagram(data)
        buffer = BytesIO()

        fig.savefig(buffer, format=export_format.value_name.lower(), bbox_inches='tight')
        plt.close(fig)

        return SeabornImage(buffer.getvalue())

    def __extract_data(self, result: Result, cross_section_id: str) -> (DataFrame, str):
        """Extracts the needed information from the Result class and puts
        together a DataFrame with appropriate headers. """

        vehicle_speeds = []
        capture_timestamps = []
        vehicle_type = []
        cross_section_name: str | None = None

        for snapshot in result.snapshots:
            for cs_snapshot in snapshot.cross_section_snapshots:
                if cs_snapshot.cross_section_snapshot_id == cross_section_id:
                    if cross_section_name is None:
                        cross_section_name = cs_snapshot.cross_section_name
                    for lane_snapshot in cs_snapshot.lane_snapshots:
                        for vehicle_snapshot in lane_snapshot.vehicle_snapshots:
                            vehicle_speeds.append(vehicle_snapshot.speed)
                            vehicle_type.append(vehicle_snapshot.vehicle_type)
                            formatted_time = snapshot.capture_timestamp.format("%H:%M:%S")
                            capture_timestamps.append(formatted_time)

        data = {
            "vehicle speeds": vehicle_speeds,
            "types": vehicle_type,
            "timestamps": capture_timestamps,
        }

        return pd.DataFrame(data), cross_section_name

    def __generate_diagram(self, data: DataFrame) -> Figure:
        """Maps the desired diagram with Matplotlib and Seaborn."""

        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots()

        ax.set_xlabel("Zeit")
        ax.set_ylabel("V[km/h]")
        avg_data = data.groupby("timestamps", as_index=False)["vehicle speeds"].mean()

        sns.scatterplot(data=data, x="timestamps", y="vehicle speeds", hue="types", legend=False, ax=ax)
        sns.lineplot(data=avg_data, x="timestamps", y="vehicle speeds", legend=False, errorbar=None, linewidth=1.5,
                     color="#00008B", ax=ax)

        timestamps = data["timestamps"]

        labels = [t if t.endswith(":00:00") else "" for t in timestamps]
        positions = [t if (t.endswith(":00:00") or t.endswith(":30:00")) else "" for t in timestamps]

        ax.set_xticks(positions, labels=labels)
        fig.tight_layout()

        return fig