"""This module defines the SimulationManager class"""
from typing import cast

from gi.repository import GObject, GLib

from sbaid.model.simulation import cross_section_state
from sbaid.model.simulation.display import Display
from sbaid.model.simulation.input import Input
from sbaid.model.simulation.parameter_state import ParameterState
from sbaid import common
from sbaid.model.algorithm_configuration.parameter_configuration import ParameterConfiguration
from sbaid.model.results.result import Result
from sbaid.common.location import Location
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
    """This class defines the SimulationManager class, that manages a running simulation."""

    def __init__(self, project_name: str, algorithm_configuration: AlgorithmConfiguration,
                 network: Network, simulator: Simulator, result_manager: ResultManager,
                 observer: SimulationObserver) -> None:
        """Initialize the SimulationManager class.  This is valid at the exact moment of
        its construction and should be used immediately, i.e. started."""
        super().__init__(project_name=project_name, algorithm_configuration=algorithm_configuration,
                         network=network, simulator=simulator, result_manager=result_manager,
                         observer=observer)
        self.observer = observer
        self.network = network
        self.algorithm_configuration = algorithm_configuration
        self.project_name = project_name
        self.simulator = simulator
        self.result_manager = result_manager

    def cancel(self) -> None:
        """Cancel the running simulation"""

    async def start(self) -> None:
        """Start the simulation"""
        result_builder = ResultBuilder(self.result_manager)
        result_builder.begin_result(self.project_name)
        param_config_state = self.__build_parameter_configuration_state(
            self.algorithm_configuration.parameter_configuration)
        network_state = self.__build_network_state(self.network)

        simulation_start_time, simulation_duration = self.simulator.init_simulation()

        self.algorithm_configuration.algorithm.init(param_config_state, network_state)

        elapsed_time = 0
        while elapsed_time < simulation_duration:
            await self.simulator.continue_simulation(self.algorithm_configuration
                                                     .evaluation_interval)
            measurement = await self.simulator.measure()
            display_interval = self.algorithm_configuration.display_interval
            display = self.algorithm_configuration.algorithm.calculate_display(measurement)

            if elapsed_time % display_interval == 0:
                await self.simulator.set_display(display)

            self.__add_to_results(result_builder, measurement, display, network_state,
                                  simulation_start_time, elapsed_time)

            self.observer.update_progress(elapsed_time / simulation_duration)

            elapsed_time += self.algorithm_configuration.evaluation_interval

        await self.simulator.stop_simulation()
        result = result_builder.end_result()
        self.observer.finished(result.id)

    def __build_parameter_configuration_state(self,
            _parameter_configuration: ParameterConfiguration)\
        -> ParameterConfigurationState:
        parameter_states = []
        for parameter in common.list_model_iterator(_parameter_configuration.parameters):
            parameter_states.append(ParameterState(parameter.name, parameter.value,
                                                   parameter.cross_section))

        return ParameterConfigurationState(parameter_states)

    def __build_network_state(self, network: Network) -> NetworkState:
        locations = cast(list[Location], common.list_model_iterator(network.route.points))
        cs_states = []
        for cs in common.list_model_iterator(network.cross_sections):
            cs_states.append(CrossSectionState(cs.id, cs.type, cs.lanes,
                                               cs.b_display_available, cs.hard_shoulder_available))
        return NetworkState(locations, cs_states)

    def __add_to_results(self, result_builder: ResultBuilder, measurement: Input,
                         display: Display | None, network_state: NetworkState,
                         start_time: GLib.DateTime, elapsed_time: int) -> None:
        result_builder.begin_snapshot(start_time.add_seconds(elapsed_time))
        for cs_state in network_state.cross_section_states:
            result_builder.begin_cross_section(self.network.cross_sections.find(cs_state.id))
            if display:
                result_builder.add_b_display(display.get_b_display(cs_state.id))

            for lane in cs_state.lanes:
                result_builder.begin_lane(lane)
                result_builder.add_average_speed(
                    measurement.get_average_speed(cs_state.id, lane))
                result_builder.add_traffic_volume(
                    measurement.get_traffic_volume(cs_state.id, lane))
                if display:
                    result_builder.add_a_display(
                        display.get_a_display(cs_state.id, lane))
                for vehicle_info in (measurement
                        .get_all_vehicle_infos(cs_state.id, lane)):
                    result_builder.begin_vehicle()
                    result_builder.add_vehicle_type(vehicle_info.type)
                    result_builder.add_vehicle_speed(vehicle_info.speed)
                    result_builder.end_vehicle()
                result_builder.end_lane()
            result_builder.end_cross_section()
        result_builder.end_snapshot()
