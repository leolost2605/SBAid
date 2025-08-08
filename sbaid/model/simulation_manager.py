"""This module defines the SimulationManager class"""
import asyncio

from gi.repository import GObject, GLib

from sbaid.model.simulation.display import Display
from sbaid.model.simulation.input import Input
from sbaid.model.simulation.parameter_state import ParameterState
from sbaid import common
from sbaid.model.results.result_builder import ResultBuilder
from sbaid.model.simulation.cross_section_state import CrossSectionState
from sbaid.model.simulation.network_state import NetworkState
from sbaid.model.simulation.parameter_configuration_state import ParameterConfigurationState
from sbaid.model.simulation_observer import SimulationObserver
from sbaid.model.network.network import Network
from sbaid.model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.results.result_manager import ResultManager


class SimulationManager(GObject.GObject):
    """
    This class defines the SimulationManager class, that manages a running simulation.
    """

    __result_builder: ResultBuilder

    __project_name: str
    __algorithm_configuration: AlgorithmConfiguration
    __network: Network
    __simulator: Simulator
    __observer: SimulationObserver

    __simulation_task: asyncio.Task[None]

    def __init__(self, project_name: str, algorithm_configuration: AlgorithmConfiguration,
                 network: Network, simulator: Simulator, result_manager: ResultManager,
                 observer: SimulationObserver) -> None:
        super().__init__()
        self.__result_builder = ResultBuilder(result_manager)
        self.__project_name = project_name
        self.__algorithm_configuration = algorithm_configuration
        self.__network = network
        self.__simulator = simulator
        self.__observer = observer

    async def cancel(self) -> None:
        """Cancel the running simulation"""
        self.__simulation_task.cancel()
        await self.__simulator.stop_simulation()

    def start(self) -> None:
        """Start the simulation"""

        self.__simulation_task = asyncio.create_task(self.__try_run_simulation())

    async def __try_run_simulation(self) -> None:
        try:
            await self.__run_simulation()
        except Exception as e:  # pylint: disable=broad-exception-caught
            print("Failed to simulate: ", e)
            self.__observer.failed(GLib.Error("Failed to simulate: " + str(e)))

    async def __run_simulation(self) -> None:
        simulation_start_time, simulation_duration = await self.__simulator.init_simulation()

        algorithm = self.__algorithm_configuration.algorithm
        eval_interval = self.__algorithm_configuration.evaluation_interval
        display_interval = self.__algorithm_configuration.display_interval

        param_config_state = self.__build_parameter_configuration_state()
        network_state = self.__build_network_state()
        algorithm.init(param_config_state, network_state)

        self.__result_builder.begin_result(self.__project_name)

        elapsed_time = 0
        while elapsed_time < simulation_duration:
            await self.__simulator.continue_simulation(eval_interval)

            measurement = await self.__simulator.measure()

            display = None

            if elapsed_time % display_interval == 0:
                display = algorithm.calculate_display(measurement)
                await self.__simulator.set_display(display)

            self.__add_to_results(measurement, display, network_state,
                                  simulation_start_time, elapsed_time)

            self.__observer.update_progress(elapsed_time / simulation_duration)

            elapsed_time += eval_interval

        await self.__simulator.stop_simulation()

        result = await self.__result_builder.end_result()

        self.__observer.finished(result.id)

    def __build_parameter_configuration_state(self) -> ParameterConfigurationState:
        config = self.__algorithm_configuration.parameter_configuration

        parameter_states = []
        for parameter in common.list_model_iterator(config.parameters):
            parameter_states.append(ParameterState(parameter.name, parameter.value,
                                                   parameter.cross_section))

        return ParameterConfigurationState(parameter_states)

    def __build_network_state(self) -> NetworkState:
        locations = list(common.list_model_iterator(self.__network.route.points))
        cs_states = []
        for cs in common.list_model_iterator(self.__network.cross_sections):
            cs_states.append(CrossSectionState(cs.id, cs.type, cs.lanes,
                                               cs.b_display_active, cs.hard_shoulder_active))
        return NetworkState(locations, cs_states)

    def __add_to_results(self, measurement: Input,
                         display: Display | None, network_state: NetworkState,
                         start_time: GLib.DateTime, elapsed_time: int) -> None:
        new_time = start_time.add_seconds(elapsed_time)
        assert new_time

        self.__result_builder.begin_snapshot(new_time)

        for cs_state in network_state.cross_section_states:
            cs_name = "Unknown cross section"

            for cs in common.list_model_iterator(self.__network.cross_sections):
                if cs.id == cs_state.id:
                    cs_name = cs.name
                    break

            self.__result_builder.begin_cross_section(cs_state.id, cs_name)

            if display:
                self.__result_builder.add_b_display(display.get_b_display(cs_state.id))

            for lane in range(cs_state.lanes):
                self.__result_builder.begin_lane(lane)

                avg_speed = measurement.get_average_speed(cs_state.id, lane)
                if avg_speed:
                    self.__result_builder.add_average_speed(avg_speed)

                volume = measurement.get_traffic_volume(cs_state.id, lane)
                if volume:
                    self.__result_builder.add_traffic_volume(volume)

                if display:
                    self.__result_builder.add_a_display(display.get_a_display(cs_state.id, lane))

                for vehicle_info in measurement.get_all_vehicle_infos(cs_state.id, lane):
                    self.__result_builder.begin_vehicle()
                    self.__result_builder.add_vehicle_type(vehicle_info.vehicle_type)
                    self.__result_builder.add_vehicle_speed(vehicle_info.speed)
                    self.__result_builder.end_vehicle()

                self.__result_builder.end_lane()

            self.__result_builder.end_cross_section()

        self.__result_builder.end_snapshot()
