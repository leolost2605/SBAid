"""This module defines the QVGenerator class."""
from io import BytesIO
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
from pandas import DataFrame
from sbaid.common.diagram_type import DiagramType
from sbaid.common.image import Image
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.cross_section_diagram_generator import CrossSectionDiagramGenerator
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot
from sbaid.model.results.lane_snapshot import LaneSnapshot
from sbaid.model.results.result import Result
from sbaid.model.results.seaborn_image import SeabornImage
from sbaid.model.results.snapshot import Snapshot


class QVGenerator(CrossSectionDiagramGenerator):
    """Contains methods for generating the 'QV-Diagram'.
    QV-Diagrams map the average speed of cross_section to the
    density of traffic (how many cars passed through in the measured timeframe).
    The types of A-Displays that are being displayed at this time are assigned different colours."""

    def get_diagram_type(self) -> DiagramType:
        """Returns the type of the diagram."""
        return DiagramType("QV-Diagram", "QV-Diagram")

    def get_diagram(self, result: Result, cross_section_id: str,
                    export_format: ImageFormat) -> Image:
        """Returns a SeabornImage class containing the bytes that make up the desired image."""

        data = self.__extract_data(result, cross_section_id)
        fig = self.__generate_diagram(data)

        buffer = BytesIO()
        fig.savefig(buffer, format=export_format.value_name.lower(), bbox_inches='tight')
        plt.close(fig)

        return SeabornImage(buffer.getvalue(), export_format)

    def __extract_data(self, result: Result, cross_section_id: str) -> DataFrame:
        """Extracts the needed information from the Result class and puts
        together a DataFrame with appropriate headers. """

        average_speed = []
        traffic_volume = []
        a_displays = []

        cross_section_name: str | None = None

        for snapshot in result.snapshots:
            assert isinstance(snapshot, Snapshot)
            for cs_snapshot in snapshot.cross_section_snapshots:
                assert isinstance(cs_snapshot, CrossSectionSnapshot)
                if cs_snapshot.cross_section_id == cross_section_id:
                    if cross_section_name is None:
                        cross_section_name = cs_snapshot.cross_section_name
                    for lane_snapshot in cs_snapshot.lane_snapshots:
                        assert isinstance(lane_snapshot, LaneSnapshot)
                        average_speed.append(lane_snapshot.average_speed)
                        traffic_volume.append(lane_snapshot.traffic_volume)
                        a_displays.append(lane_snapshot.a_display)

        data = {
            "speed": average_speed,
            "volume": traffic_volume,
            "display": a_displays
        }

        return pd.DataFrame(data)

    def __generate_diagram(self, data: DataFrame) -> Figure:
        """Maps the desired diagram with Matplotlib and Seaborn."""

        colorscheme = LinearSegmentedColormap.from_list('rg',
                                                        ["#910000", "#c10000", "r",
                                                         "#ffa500", "y", "g"], N=256)

        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots()
        ax.set_xlabel("Q_pkv [Pkv/min]")
        ax.set_ylabel("V[km/h]")

        sns.scatterplot(data=data, x="volume", y="speed", hue="display",
                        palette=colorscheme, legend=False, ax=ax)

        return fig
