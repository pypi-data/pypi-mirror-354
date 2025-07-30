"""
This code is protected under GNU General Public License v3.0

A helper module dedicated to the design of time-varying state space model approximated by bilinear state space model.

Author: stephane.ploix@grenoble-inp.fr
"""
from __future__ import annotations
import numpy
import time
from abc import ABC, abstractmethod
from typing import Any
from enum import Enum
from datetime import datetime
from .components import Airflow
from .statemodel import StateModel
from .model import BuildingStateModelMaker
from .data import DataProvider
from .inhabitants import Preference


class VALUE_DOMAIN_TYPE(Enum):
    """An enum to define the type of the value domain of a control port"""
    CONTINUOUS = 0
    DISCRETE = 1


class AbstractModeFactory(ABC):

    def __init__(self, **provided_variables: dict[str, list[float]]) -> None:
        self.mode_variable_values: dict[str, list[float]] = provided_variables
        self.mode_variables: list[str] = list(self.mode_variable_values.keys())

    @abstractmethod
    def merge_to_mode(self, **variable_values) -> float:
        raise NotImplementedError("This method should be implemented in the child class")

    def __call__(self, k: int, **variable_values: dict[str, float]) -> dict[str, float]:
        mode_variable_values_k: dict[str, float] = {mode_variable: self.mode_variable_values[mode_variable][k] for mode_variable in self.mode_variables}  # get the values of the mode variables from the pre-existing series at time k
        for variable in variable_values:  # update the input data with the new provided values of the mode variables
            mode_variable_values_k[variable] = variable_values[variable]
        return self.merge_to_mode(**mode_variable_values_k)


class ModeFactory(AbstractModeFactory):

    def __init__(self, **provided_variables: dict[str, list[float]]) -> None:
        super().__init__(**provided_variables)
        if len(self.mode_variables) > 1:
            raise ValueError('ModeFactory should be used with a single mode variable')

    def merge_to_mode(self, **mode_variable_values_k: dict[str, float]) -> float:
        return int(mode_variable_values_k[self.mode_variables[0]] > 0)


class MultiplexModeFactory(AbstractModeFactory):

    def __init__(self, **provided_variables: dict[str, list[float]]) -> None:
        super().__init__(**provided_variables)

    def merge_to_mode(self, **mode_variable_values_k: dict[str, float]) -> float:
        return sum(2**i * int(mode_variable_values_k[self.mode_variables[i]] > 0) for i in range(len(self.mode_variables)))


class Port(ABC):

    def _intersection(self, *sets) -> tuple[float, float] | None:
        """Compute the intersection of two intervals.

        :param interval1: the first interval
        :type interval1: tuple[float, float]
        :param interval2: the second interval
        :type interval2: tuple[float, float]
        :return: the intersection of the two intervals
        :rtype: tuple[float, float] | None
        """
        if sets[0] is None:
            return None
        global_set: tuple[float, float] = sets[0]
        for _set in sets[1:]:
            if _set is None:
                return None
            else:
                if self.value_domain_type == VALUE_DOMAIN_TYPE.CONTINUOUS:
                    bound_inf: float = max(global_set[0], _set[0])
                    bound_sup: float = min(global_set[1], _set[1])
                    if bound_inf <= bound_sup:
                        global_set: tuple[float, float] = (bound_inf, bound_sup)
                    else:
                        return None
                else:
                    global_set: list[int] = list(set(global_set) & set(_set))
        return global_set
    
    def __union(self, *sets) -> tuple[float, float] | None:
        i = 0
        while i < len(sets) and sets[i] is None:
            i += 1
        if i == len(sets):
            return None
        global_set: tuple[float, float] = sets[i]
        i += 1
        while i < len(sets):
            if sets[i] is not None:
                if self.value_domain_type == VALUE_DOMAIN_TYPE.CONTINUOUS:
                    global_set: tuple[float, float] =(min(global_set[0], sets[i][0]), max(global_set[1], sets[i][-1]))
                else:
                    global_set: list[int] = list(set(global_set) | set(sets[i]))
            i += 1
        return tuple(global_set)

    def __init__(self, data_provider: DataProvider, variable_name: str, value_domain_type: VALUE_DOMAIN_TYPE, value_domain: list[float]) -> None:
        super().__init__()
        self.dp: DataProvider = data_provider
        self.variable_name: str = variable_name
        self.in_provider: bool = self._in_provider(variable_name)
        if self.in_provider:
            print(f'{variable_name} is saved automatically by the port')
        else:
            print(f'{variable_name} must be saved manually via the port at the end of a simulation')
        self.recorded_data: dict[int, float] = dict()
        self.value_domain_type: VALUE_DOMAIN_TYPE = value_domain_type
        self.modes_value_domains: dict[int, list[float]] = dict()
        if value_domain is not None:
            self.modes_value_domains[0] = value_domain

    def _in_provider(self, variable_name: str) -> bool:
        return self.dp is not None and variable_name in self.dp

    def __call__(self, k: int, port_value: float | None = None) -> list[float] | float | None:
        if port_value is None:
            if k in self.recorded_data:
                return self.recorded_data[k]
            else:
                return self.modes_value_domains[0]
        else:
            value_domain: list[float] = self._standardize(self.modes_value_domains[0])
            port_value = self._restrict(value_domain, port_value)
            self.recorded_data[k] = port_value
            if self.in_provider:
                self.dp(self.variable_name, k, port_value)
            return port_value
    
    def _restrict(self, value_domain: list[float], port_value: float) -> float:
        if self.value_domain_type == VALUE_DOMAIN_TYPE.DISCRETE:
            if port_value not in value_domain:
                distance_to_value = tuple([abs(port_value - v) for v in value_domain])
                port_value = value_domain[distance_to_value.index(min(distance_to_value))]
        else:
            port_value = port_value if port_value <= value_domain[1] else value_domain[1]
            port_value = port_value if port_value >= value_domain[0] else value_domain[0]
        return port_value

    def _standardize(self, value_domain: int | float | tuple | float | list[float]) -> None | tuple[float]:
        if value_domain is None:
            return None
        else:
            if self.value_domain_type == VALUE_DOMAIN_TYPE.DISCRETE:
                if type(value_domain) is int or type(value_domain) is float:
                    standardized_value_domain: tuple[int | float] = (value_domain,)
                elif len(value_domain) >= 1:
                    standardized_value_domain = tuple(sorted(list(set(value_domain))))
            else:  # VALUE_DOMAIN_TYPE.CONTINUOUS
                if type(value_domain) is not list and type(value_domain) is not tuple:
                    standardized_value_domain: tuple[float, float] = (value_domain, value_domain)
                else:
                    standardized_value_domain: tuple[float, float] = (min(value_domain), max(value_domain))
            return standardized_value_domain

    def save(self) -> None:
        if not self.in_provider:
            data = list()
            for k in range(len(self.dp)):
                if k in self.recorded_data:
                    data.append(self.recorded_data[k])
                else:
                    data.append(0)
            self.dp.add_external_variable(self.variable_name, data)
        else:
            if self.dp is None:
                raise ValueError('No data provider: cannot save the port data')
            else:
                print(f'{self.variable_name} is saved automatically')
                self.dp(self.variable_name, self.recorded_data)

    def __repr__(self) -> str:
        return f"Control port {self.variable_name}"

    def __str__(self) -> str:
        if self.value_domain_type == VALUE_DOMAIN_TYPE.DISCRETE:
            string = 'Discrete'
        else:
            string = 'Continuous'
        string += f" control port on {self.variable_name} with general value domain {self.modes_value_domains}"
        string += f", automatically recorded data: {self.in_provider}"
        return string


class ModePort(Port):
    """A control port that depends on a mode variable: the value domain is different depending on the mode.
    """

    def __init__(self, data_provider: DataProvider, variable_name: str, value_domain_type: VALUE_DOMAIN_TYPE, modes_value_domains: list[float], mode_factory: ModeFactory) -> None:
        super().__init__(data_provider, variable_name, value_domain_type, None)
        self.modes_value_domains = {mode: self._standardize(modes_value_domains[mode]) for mode in modes_value_domains}
        self.mode_factory: ModeFactory = mode_factory

    def value_domain(self, k: int, **mode_values: Any) -> list[float]:
        mode: dict[str, float] = self.mode_factory(k, **mode_values)
        return self.modes_value_domains[mode]

    def __call__(self, k: int, port_value: float | None = None, **mode_variable_values: dict[str, float]) -> list[float] | float | None:
        mode: dict[str, float] = self.mode_factory(k, **mode_variable_values)
        if port_value is None:
            return self.modes_value_domains[mode]
        else:
            port_value = self._restrict(self.modes_value_domains[mode], port_value)
            self.recorded_data[k] = port_value
            if self.in_provider:
                self.dp(self.variable_name, k, port_value)
            return port_value


class ContinuousPort(Port):
    def __init__(self, data_provider: DataProvider, variable_name: str, value_domain: list[float]) -> None:
        super().__init__(data_provider, variable_name, VALUE_DOMAIN_TYPE.CONTINUOUS, value_domain)


class DiscretePort(Port):
    def __init__(self, data_provider: DataProvider, variable_name: str, value_domain: list[float]) -> None:
        super().__init__(data_provider, variable_name, VALUE_DOMAIN_TYPE.DISCRETE, value_domain)


class ContinuousModePort(ModePort):
    def __init__(self, data_provider: DataProvider, variable_name: str, modes_value_domains: dict[int, list[float]], mode_factory: ModeFactory) -> None:
        super().__init__(data_provider, variable_name, VALUE_DOMAIN_TYPE.CONTINUOUS, modes_value_domains, mode_factory)


class DiscreteModePort(ModePort):
    def __init__(self, data_provider: DataProvider, variable_name: str, modes_value_domains: dict[int, list[float]], mode_factory: ModeFactory) -> None:
        super().__init__(data_provider, variable_name, VALUE_DOMAIN_TYPE.DISCRETE, modes_value_domains, mode_factory)


class TemperatureController:
    """A controller is controlling a power port to reach as much as possible a temperature setpoint modeled by a temperature port. The controller is supposed to be fast enough comparing to the 1-hour time slots, that its effect is immediate (level 0), or almost immediate (level 1, for modifying the next temperature).
    It would behave as a perfect controller if the power was not limited but it is.
    """

    def __init__(self, power_name: str, hvac_heat_power_port: Port, temperature_name: str, temperature_setpoint_port: Port, state_model_nominal: StateModel) -> None:

        self.dp: DataProvider = hvac_heat_power_port.dp
        self.hvac_heat_power_port: Port = hvac_heat_power_port
        self.temperature_setpoint_port: Port = temperature_setpoint_port
        self.power_name: str = power_name
        self.heat_gain_name: str = power_name
        self.power_index: int = state_model_nominal.input_names.index(power_name)
        self.temperature_name: str = temperature_name
        self.temperature_setpoint_name: str = self.temperature_setpoint_port.variable_name
        self.temperature_index: int = state_model_nominal.output_names.index(temperature_name)

        if self.heat_gain_name not in self.dp:
            raise ValueError(f'{self.heat_gain_name} is not in the data provider')
        if self.temperature_setpoint_name not in self.dp:
            raise ValueError(f'{self.temperature_setpoint_name} is not in the data provider')
        self.controller_delay: int = -1

        if power_name not in state_model_nominal.input_names:
            raise ValueError(f'{power_name} is not an input of the state model: {state_model_nominal.input_names}')
        if temperature_name not in state_model_nominal.output_names:
            raise ValueError(f'{temperature_name} is not an output of the state model: {str(state_model_nominal.output_names)}')
        
        D_condition: numpy.matrix = state_model_nominal.D[self.temperature_index, self.power_index]
        CB: numpy.matrix = state_model_nominal.C * state_model_nominal.B
        CB_condition: numpy.matrix = CB[self.temperature_index, self.power_index]
        if D_condition != 0:
            self.controller_delay = 0
        elif CB_condition != 0:
            self.controller_delay = 1
        else:
            raise ValueError(f'{self.temperature_name} cannot be controlled by {self.power_name} thanks to the setpoint {self.temperature_setpoint_name} adding power to {self.heat_gain_name}')

    def hvac_power_k(self, k: int, temperature_setpoint_k: float, state_model_k: StateModel, state_k: numpy.matrix, inputs_k: numpy.matrix, inputs_kp1: numpy.matrix = None) -> float:

        if temperature_setpoint_k is None or numpy.isnan(temperature_setpoint_k) or type(temperature_setpoint_k) is float('nan'):
            return 0
        temperature_setpoint_k = self.temperature_setpoint_port(temperature_setpoint_k)
        
        # if self.heat_gain_name not in self.hvac_heat_power_port.dp:
        #     raise ValueError(f'{self.heat_gain_name} is not in the data provider')
        inputs_k[self.power_index, 0]: numpy.matrix = 0  # self.dp(self.heat_gain_name, k)
        inputs_kp1[self.power_index, 0]: numpy.matrix = 0  # self.dp(self.heat_gain_name, k+1)
        power_removal = numpy.diag(numpy.ones(len(inputs_k)))
        power_removal[self.power_index, self.power_index] = 0

        if self.controller_delay == 0:
            hvac_power_k: numpy.matrix = (temperature_setpoint_k - state_model_k.C[self.temperature_index, :] * state_k - state_model_k.D[self.temperature_index, :] * power_removal * inputs_k) / state_model_k.D[self.temperature_index, self.power_index]
        elif self.controller_delay == 1:
            if inputs_kp1 is None:
                raise ValueError("Inputs at time k and k+1 must be provided for delay-1 controller")

            hvac_power_k: numpy.matrix = (temperature_setpoint_k - state_model_k.C[self.temperature_index, :] * state_model_k.A * state_k - state_model_k.C[self.temperature_index, :] * state_model_k.B * power_removal * inputs_k - state_model_k.D[self.temperature_index, :] * power_removal * inputs_kp1) / (state_model_k.C[self.temperature_index] * state_model_k.B[:, self.power_index])
        else:  # unknown level
            raise ValueError('No controller available')
        return self.hvac_heat_power_port(k, self.hvac_heat_power_port(hvac_power_k[0, 0]-self.dp(self.heat_gain_name, k)))

    def delay(self) -> int:
        """Get the delay of the controller. 0 means that the controller reach the setpoint immediately, 1 means that the controller reach the setpoint with a delay of one time slot.

        :return: the delay of the controller
        :rtype: int 0 or 1
        """
        return self.controller_delay

    def __repr__(self) -> str:
        """String representation of the controller.
        :return: a string representation of the controller
        :rtype: str
        """
        return self.temperature_setpoint_port.variable_name + '>' + self.hvac_heat_power_port.variable_name

    def __str__(self) -> str:
        """String representation of the controller.
        :return: a string representation of the controller
        :rtype: str
        """
        string: str = f'> Temperature is controlled by {self.hvac_heat_power_port.variable_name} is controlled by\n  the setpoint {self.temperature_setpoint_port.variable_name}\n  with a delay of {self.controller_delay}'
        return string


class Simulator(ABC):
    """A manager is a class that gathers all the data about a zone, including control rules.
    """
    
    class Zone:
        
        def __init__(self, zone_name: str,  preference: Preference, initial_temperature: float = 20, CO2production_name: str, heat_gain_name: str = None, temperature_controller: TemperatureController = None, **control_ports: Port) -> None:
            self.zone_name: str = zone_name
            self.heat_gain_name: str = heat_gain_name
            if heat_gain_name not in self.dp:
                raise ValueError(f'heat gain {heat_gain_name} must be defined in the data provider')
            self.CO2production_name: str = CO2production_name
            if CO2production_name not in self.dp:
                raise ValueError(f'CO2 production {CO2production_name} must be defined in the data provider')
            self.preference: Preference = preference
            self.initial_temperature: float = initial_temperature
            self.temperature_controller: TemperatureController = temperature_controller
            self.control_ports: dict[str, Port] = control_ports
            
            self.model_temperature_name: str = 'TZ' + zone_name
            self.model_temperature_index: int = self.nominal_state_model.output_names.index(self.model_temperature_name)
            self.model_CO2concentration_name: str = 'CCO2' + zone_name
            self.model_CO2concentration_index: int = self.nominal_state_model.output_names.index(self.model_CO2concentration_name)
            self.model_power_name: str = 'P' + zone_name
            self.model_power_index: int = self.nominal_state_model.input_names.index(self.model_power_name)
            self.model_CO2production_name: str = 'PCO2' + zone_name
            self.model_CO2production_index: int = self.nominal_state_model.input_names.index(self.model_CO2production_name)
            
            if self.has_controller():
                if self.temperature_controller.temperature_name != self.model_temperature_name:
                    raise ValueError(f'{self.temperature_controller.temperature_name} is not an output of the state model')
                if self.temperature_controller.heat_gain_name not in self.dp:
                    raise ValueError(f'heat gain {self.temperature_controller.heat_gain_name} must be defined in the data provider')
                if 
                    
                self.model_temperature_setpoint_name: str = self.temperature_controller.temperature_setpoint_port.variable_name
                self.model_temperature_setpoint_index: int = self.nominal_state_model.input_names.index(self.model_temperature_setpoint_name)
                self.model_heat_gain_name: str = self.temperature_controller.heat_gain_name
                self.model_heat_gain_index: int = self.nominal_state_model.input_names.index(self.model_heat_gain_name)
            else:
                if heat_gain_name is None:
                    raise ValueError('heat gain must be defined if no controller')
                self.model_heat_gain_name: str = heat_gain_name
                self.model_heat_gain_index: int = self.nominal_state_model.input_names.index(self.model_heat_gain_name)
                self.model_CO2production_name: str = CO2production_name
            
            self.model_temperature_setpoint_name: str = 'TZ' + zone_name + '_setpoint'
            self.model_temperature_setpoint_index: int = self.nominal_state_model.input_names.index(self.model_temperature_setpoint_name)
            self.model_heat_gain_name: str = 'PZ' + zone_name
            self.model_heat_gain_index: int = self.nominal_state_model.input_names.index(self.model_heat_gain_name)
            
            
            self.input_names: list[str] = self.nominal_state_model.input_names
            self.output_names: list[str] = self.nominal_state_model.output_names
            self.initial_temperature: float = initial_temperature
            self.datetimes: list[datetime] = self.dp.series('datetime')
            self.day_of_week: list[int] = self.dp('day_of_week')
            self.other_ports: dict[str, Port] = control_ports
            
        def has_controller(self) -> bool:
            return self.temperature_controller is not None
            
            
            

    def __init__(self, dp: DataProvider, state_model_maker: BuildingStateModelMaker) -> None:
        self.dp = dp
        self.state_model_maker: BuildingStateModelMaker = state_model_maker
        self.zone_data: dict[str, Simulator.Zone] = dict()
        self.nominal_state_model: StateModel = self.state_model_maker.make_nominal(reset_reduction=True)
        self.model_input_names: list[str] = self.nominal_state_model.input_names
        self.model_output_names: list[str] = self.nominal_state_model.output_names
        self.datetimes: list[datetime] = self.dp.series('datetime')
        self.day_of_week: list[int] = self.dp('day_of_week')
         
    def make_zone(self, zone_name: str, preference: Preference, initial_temperature: float = 20, heat_gain_name: str = None, temperature_controller: TemperatureController = None, **other_ports: Port) -> None:
        self.recorded_data: dict[str, dict[int, list[float]]] = dict()
        self.temperature_controller: TemperatureController = temperature_controller
        self.preference: Preference = preference
        self.other_ports: dict[str, Port] = other_ports
    
        

        if self.temperature_controller.temperature_name not in self.output_names:
            raise ValueError(f'{self.temperature_controller.temperature_name} is not an output of the state model')
        self.zone_temperature_index: int = self.output_names.index(self.temperature_controller.temperature_name)
        self.preference: Preference = preference
        self.control_model: ControlModel = None
        
    def __call__(self, element):
        return super().__call__(*args, **kwds)

    def register_control_model(self, control_model: ControlModel) -> None:
        self.control_model = control_model

    def controls(self, k: int, X_k: numpy.matrix, current_output_dict: dict[str, float]) -> None:
        # if self.dp('presence', k) == 1:    ######### DESIGN YOUR OWN CONTROLS HERE #########
        #     self.window_opening_port(k, 1) # USE THE CONTROL PORTS FOR ACTION AND USE self.dp('variable', k) TO GET A VALUE
        pass

    def __str__(self) -> str:
        string: str = "__________ZONE MANAGER__________\n"
        string += '* NOMINAL STATE MODEL:\n'
        string += str(self.nominal_state_model) + '\n'
        string += "* CONTROLLER:\n"
        string += str(self.temperature_controller) + '\n'
        string += "* PREFERENCES:\n"
        string += str(self.preference) + '\n'
        string += f'* INITIAL TEMPERATURE: {self.initial_temperature}\n'
        if len(self.other_ports) > 0:
            string += "* AVAILABLE PORTS:\n"
            for port_name in self.other_ports:
                string += str(self.other_ports[port_name]) + '\n'
        return string


class ControlledZoneManager(Simulator):
    """A manager is a class that gathers all the data about a zone, including control rules.
    """

    def __init__(self, dp: DataProvider, zone_temperature_controller: TemperatureController, state_model_maker: BuildingStateModelMaker, preference: Preference, initial_temperature: float = 20, **other_ports: Port) -> None:
        super().__init__(dp, zone_temperature_controller, state_model_maker, preference, initial_temperature, **other_ports)

        self.available_set_points: bool = False
        self.temperature_controller: TemperatureController = zone_temperature_controller
        self.has_controller: bool = zone_temperature_controller is not None
        self.available_set_points = False

        if self.has_controller:
            self.temperature_controller: TemperatureController = zone_temperature_controller

    def state_model_k(self, k: int) -> StateModel:
        """Get the state model for time slot k.
        """
        return self.state_model_maker.make_k(k)


class ControlModel:
    """The main class for simulating a living area with a control.
    """

    def __init__(self, building_state_model_maker: BuildingStateModelMaker, manager: ControlledZoneManager = None) -> None:
        self.building_state_model_maker: BuildingStateModelMaker = building_state_model_maker
        self.dp: DataProvider = building_state_model_maker.data_provider
        self.airflows: list[Airflow] = building_state_model_maker.airflows
        self.fingerprint_0: list[int] = self.dp.fingerprint(0)  # None
        self.state_model_0: StateModel = building_state_model_maker.make_k(k=0, reset_reduction=True, fingerprint=self.fingerprint_0)
        self.input_names: list[str] = self.state_model_0.input_names
        self.output_names: list[str] = self.state_model_0.output_names
        self.state_models_cache: dict[int, StateModel] = {self.fingerprint_0: self.state_model_0}
        self.manager: ControlledZoneManager = manager
        if manager is not None:
            self.manager.register_control_model(self)

    def simulate(self, suffix: str = '_sim'):
        print("simulation running...")
        start: float = time.time()
        # controller_controls: dict[str, list[float]] = {repr(self.manager.zone_temperature_controller): [self.manager.zone_temperature_controller]}  # list() for controller in self.manager.zone_temperature_controller}
        # controller_setpoints: dict[str, list[float]] = {repr(self.manager.zone_temperature_controller): [self.manager.zone_temperature_controller]}  # {repr(controller): list() for controller in self.manager.zone_temperature_controller}

        X_k: numpy.matrix = None
        simulated_outputs: dict[str, list[float]] = {output_name: list() for output_name in self.output_names}
        counter = 0
        for k in range(len(self.dp)):
            current_outputs = None
            # compute the current state model
            current_fingerprint: list[int] = self.dp.fingerprint(k)
            if current_fingerprint in self.state_models_cache:
                state_model_k = self.state_models_cache[current_fingerprint]
                counter += 1
                if counter % 100 == 0:
                    print('.', end='')
            else:
                state_model_k: StateModel = self.building_state_model_maker.make_k(k, reset_reduction=(k == 0))
                self.state_models_cache[self.dp.fingerprint(k)] = state_model_k
                print('*', end='')
                counter = 0
            # compute inputs and state vector
            inputs_k: dict[str, float] = {input_name: self.dp(input_name, k) for input_name in self.input_names}
            if X_k is None:
                X_k: numpy.matrix = self.state_model_0.initialize(**inputs_k)
            # compute the output before change
            output_values: list[float] = state_model_k.output(**inputs_k)
            current_outputs: dict[str, float] = {self.output_names[i]: output_values[i] for i in range(len(self.output_names))}
            self.manager.controls(k, X_k, current_outputs)

            # compute the current state model after potential change by the "controls" function
            current_fingerprint: list[int] = self.dp.fingerprint(k)
            if current_fingerprint in self.state_models_cache:
                state_model_k = self.state_models_cache[current_fingerprint]
                counter += 1
                if counter % 100 == 0:
                    print('.', end='')
            else:
                state_model_k: StateModel = self.building_state_model_maker.make_k(k, reset_reduction=(k == 0))
                self.state_models_cache[self.dp.fingerprint(k)] = state_model_k
                print('*', end='')
                counter = 0
            # collect input data for time slot k (and k+1 if possible) from the data provided
            inputs_k: dict[str, float] = {input_name: self.dp(input_name, k) for input_name in self.input_names}
            if k < len(self.dp) - 1:
                inputs_kp1: dict[str, float] = {input_name: self.dp(input_name, k+1) for input_name in self.input_names}
            # else:
            #     inputs_kp1 = inputs_k
            # update the input power value to reach the control temperature setpoints
            # for controller in self.manager.zone_temperature_controllers_initial_temperature:
            controller = self.manager.temperature_controller
            # controller_name: str = repr(controller)
            if controller.controller_delay == 0:
                setpoint_k: float = self.dp(controller.zone_temperature_setpoint_variable, k)
                control_k: float = controller.hvac_power_k(k, setpoint_k, state_model_k, X_k, inputs_k)
            elif controller.controller_delay == 1:
                if k < len(self.dp) - 1:
                    setpoint_k: float = self.dp(controller.temperature_setpoint_port.variable_name, k+1)
                else:
                    setpoint_k: float = self.dp(controller.temperature_setpoint_port.variable_name, k)
            # control_k: float = controller.compute_hvac_power_k(k, setpoint_k, state_model_k, X_k, inputs_k, inputs_kp1)
            # controller_controls[controller_name].append(control_k)
            # controller_setpoints[controller_name].append(setpoint_k)

            # inputs_k[controller.zone_power_name] = inputs_k[controller.zone_power_name] + control_k
            # self.dp(controller.zone_power_name, k, control_k)

            state_model_k.set_state(X_k)
            output_values = state_model_k.output(**inputs_k)
            # for output_index, output_name in enumerate(self.output_names):
            #     self.dp(output_name, k, output_values[output_index])
            for i, output_name in enumerate(self.output_names):
                simulated_outputs[output_name].append(output_values[i])
            X_k = state_model_k.step(**inputs_k)
        print(f"\nDuration in seconds {time.time() - start} with a state model cache size={len(self.state_models_cache)}")
        string = "Simulation results have been stored in "
        for output_name in self.output_names:
            string += output_name + suffix + ','
            self.dp.add_external_variable(output_name + suffix, simulated_outputs[output_name])

    def __str__(self) -> str:
        string = 'ControlModel:'
        string += f'\n-{self.manager.temperature_controller}'
        return string