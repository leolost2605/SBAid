"""This module defines the QVGenerator class."""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from pandas import DataFrame
from sbaid.common.diagram_type import DiagramType
# from sbaid.common.image import Image
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.cross_section_diagram_generator import CrossSectionDiagramGenerator
from sbaid.model.results.result import Result


class QVGenerator(CrossSectionDiagramGenerator):
    """todo"""

    diagram_name = "QV-Diagram"

    def get_diagram_type(self) -> DiagramType:  # pylint:disable=useless-parent-delegation
        """todo"""
        return super().get_diagram_type()

    def get_diagram(self, result: Result, cross_section_id: str,
                    export_format: ImageFormat) -> None:
        # cross_section_snapshot = GlobalDatabase.get_cross_section_snapshot(cross_section_id)
        self.__generate_diagram(self.__extract_data(result, cross_section_id))

    def __extract_data(self, result: Result, cross_section_id: str) -> DataFrame:
        """todo """
        average_speed = []
        traffic_volume = []
        a_displays = []

        for snapshot in result.snapshots:
            for cs_snapshot in snapshot.cross_section_snapshots:
                if cs_snapshot.cross_section_snapshot_id == cross_section_id:
                    for lane_snapshot in cs_snapshot.lane_snapshots:
                        average_speed.append(lane_snapshot.average_speed)
                        traffic_volume.append(lane_snapshot.traffic_volume)
                        a_displays.append(lane_snapshot.a_display)

        data = {
            "speed": average_speed,
            "volume": traffic_volume,
            "display": a_displays
        }

        return pd.DataFrame(data)

    def __generate_diagram(self, data: DataFrame) -> None:
        """todo help m"""

        colorscheme = LinearSegmentedColormap.from_list('rg',
                                                        ["#910000", "#c10000", "r",
                                                         "#ffa500", "y", "g"], N=256)

        sns.set_theme(style="whitegrid")
        ax = plt.subplot()
        ax.set_xlabel("Q_pkv [Pkv/min]")
        ax.set_ylabel("V[km/h]")

        sns.scatterplot(data=data, x="volume", y="speed", hue="display",
                        palette=colorscheme, ax=ax)

        plt.show()

    def generate_diagram(self, average_speed: list[float], traffic_volume: list[int],
                         a_displays: list[int]) -> None:
        """TODO DELETE ONLY FOR TESTUNG"""

        data = {
            "speed": average_speed,
            "volume": traffic_volume,
            "display": a_displays
        }

        new_data = pd.DataFrame(data)

        colorscheme = LinearSegmentedColormap.from_list('rg',
                                                        ["#910000", "#c10000", "r",
                                                         "#ffa500", "y", "g"], N=256)

        sns.set_theme(style="whitegrid")
        ax = plt.subplot()
        ax.set_xlabel("Q_pkv [Pkv/min]")
        ax.set_ylabel("V[km/h]")

        graph = sns.scatterplot(data=new_data, x="volume", y="speed",
                                hue="display", palette=colorscheme, ax=ax)
        plt.show()

        graph.set_title("we be testin")
