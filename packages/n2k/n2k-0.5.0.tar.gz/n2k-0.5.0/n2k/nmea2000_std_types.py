from dataclasses import dataclass
from enum import IntEnum


class N2kDD002(IntEnum):
    No = 0
    Yes = 1
    Error = 2
    Unavailable = 3
    Off = No
    Disabled = No
    Reset = No
    Zero = No
    On = Yes
    Enabled = Yes
    Set = Yes
    One = Yes
    Unknown = Unavailable


class N2kDD025(IntEnum):
    Autonomous = 0
    Differential = 1
    Estimated = 2
    Simulator = 3
    Manual = 4
    Error = 0xE
    Unavailable = 0xF


class N2kDD072(IntEnum):
    RangeResidualsWereUsedToCalculateData = 0
    RangeResidualsWereCalculatedAfterPosition = 1
    Error = 2
    Unavailable = 3


class N2kDD124(IntEnum):
    NotTracked = 0
    TrackedButNotUsedInSolution = 1
    UsedInSolutionWithoutDifferentialCorrections = 2
    DifferentialCorrectionsAvailable = 3
    TrackedWithDifferentialCorrections = 4
    UsedWithDifferentialCorrections = 5
    Error = 14
    Unavailable = 15


@dataclass(frozen=True, kw_only=True)
class N2kDD206:
    check_engine: int = 0
    over_temperature: int = 0
    low_oil_pressure: int = 0
    low_oil_level: int = 0
    low_fuel_pressure: int = 0
    low_system_voltage: int = 0
    low_coolant_level: int = 0
    water_flow: int = 0
    water_in_fuel: int = 0
    charge_indicator: int = 0
    preheat_indicator: int = 0
    high_boost_pressure: int = 0
    rev_limit_exceeded: int = 0
    egr_system: int = 0
    throttle_position_sensor: int = 0
    engine_emergency_stop_mode: int = 0

    @property
    def status(self) -> int:
        return (
            self.check_engine << 0
            | self.over_temperature << 1
            | self.low_oil_pressure << 2
            | self.low_oil_level << 3
            | self.low_fuel_pressure << 4
            | self.low_system_voltage << 5
            | self.low_coolant_level << 6
            | self.water_flow << 7
            | self.water_in_fuel << 8
            | self.charge_indicator << 9
            | self.preheat_indicator << 10
            | self.high_boost_pressure << 11
            | self.rev_limit_exceeded << 12
            | self.egr_system << 13
            | self.throttle_position_sensor << 14
            | self.engine_emergency_stop_mode << 15
        )

    @staticmethod
    def from_status(value: int) -> "N2kDD206":
        return N2kDD206(
            check_engine=(value >> 0) & 0b1,
            over_temperature=(value >> 1) & 0b1,
            low_oil_pressure=(value >> 2) & 0b1,
            low_oil_level=(value >> 3) & 0b1,
            low_fuel_pressure=(value >> 4) & 0b1,
            low_system_voltage=(value >> 5) & 0b1,
            low_coolant_level=(value >> 6) & 0b1,
            water_flow=(value >> 7) & 0b1,
            water_in_fuel=(value >> 8) & 0b1,
            charge_indicator=(value >> 9) & 0b1,
            preheat_indicator=(value >> 10) & 0b1,
            high_boost_pressure=(value >> 11) & 0b1,
            rev_limit_exceeded=(value >> 12) & 0b1,
            egr_system=(value >> 13) & 0b1,
            throttle_position_sensor=(value >> 14) & 0b1,
            engine_emergency_stop_mode=(value >> 15) & 0b1,
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, N2kDD206):
            return self.status == other.status
        if isinstance(other, int):
            return self.status == other
        return False


@dataclass(frozen=True, kw_only=True)
class N2kDD223:
    warning_level1: int = 0
    warning_level2: int = 0
    power_reduction: int = 0
    maintenance_needed: int = 0
    engine_comm_error: int = 0
    sub_or_secondary_throttle: int = 0
    neutral_start_protect: int = 0
    engine_shutting_down: int = 0
    manufacturer1: int = 0
    manufacturer2: int = 0
    manufacturer3: int = 0
    manufacturer4: int = 0
    manufacturer5: int = 0
    manufacturer6: int = 0
    manufacturer7: int = 0
    manufacturer8: int = 0

    @property
    def status(self) -> int:
        return (
            self.warning_level1 << 0
            | self.warning_level2 << 1
            | self.power_reduction << 2
            | self.maintenance_needed << 3
            | self.engine_comm_error << 4
            | self.sub_or_secondary_throttle << 5
            | self.neutral_start_protect << 6
            | self.engine_shutting_down << 7
            | self.manufacturer1 << 8
            | self.manufacturer2 << 9
            | self.manufacturer3 << 10
            | self.manufacturer4 << 11
            | self.manufacturer5 << 12
            | self.manufacturer6 << 13
            | self.manufacturer7 << 14
            | self.manufacturer8 << 15
        )

    @staticmethod
    def from_status(value: int) -> "N2kDD223":
        return N2kDD223(
            warning_level1=(value >> 0) & 0b1,
            warning_level2=(value >> 1) & 0b1,
            power_reduction=(value >> 2) & 0b1,
            maintenance_needed=(value >> 3) & 0b1,
            engine_comm_error=(value >> 4) & 0b1,
            sub_or_secondary_throttle=(value >> 5) & 0b1,
            neutral_start_protect=(value >> 6) & 0b1,
            engine_shutting_down=(value >> 7) & 0b1,
            manufacturer1=(value >> 8) & 0b1,
            manufacturer2=(value >> 9) & 0b1,
            manufacturer3=(value >> 10) & 0b1,
            manufacturer4=(value >> 11) & 0b1,
            manufacturer5=(value >> 12) & 0b1,
            manufacturer6=(value >> 13) & 0b1,
            manufacturer7=(value >> 14) & 0b1,
            manufacturer8=(value >> 15) & 0b1,
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, N2kDD223):
            return self.status == other.status
        if isinstance(other, int):
            return self.status == other
        return False


class N2kDD305(IntEnum):
    not_specified = 0
    reference_point = 1
    RACON = 2
    fixed_structure = 3
    emergency_wreck_marking_buoy = 4
    light_without_sectors = 5
    light_with_sectors = 6
    leading_light_front = 7
    leading_light_rear = 8
    beacon_cardinal_north = 9
    beacon_cardinal_east = 10
    beacon_cardinal_south = 11
    beacon_cardinal_west = 12
    beacon_port_hand = 13
    beacon_starboard_hand = 14
    beacon_preferred_ch_port_hand = 15
    beacon_preferred_ch_starboard_hand = 16
    beacon_isolated_danger = 17
    beacon_safe_water = 18
    beacon_special_mark = 19
    cardinal_mark_north = 20
    cardinal_mark_east = 21
    cardinal_mark_south = 22
    cardinal_mark_west = 23
    port_hand_mark = 24
    starboard_hand_mark = 25
    preferred_channel_port_hand = 26
    preferred_channel_starboard_hand = 27
    isolated_danger = 28
    safe_water = 29
    special_mark = 30
    light_vessel_lanby_rigs = 31


class N2kDD374(IntEnum):
    user_defined = 0
    minimum_defined = 1
    factory_default = 2
    maximum_supported = 3
    out_of_range = 14
    data_not_available = 15


# Thruster Motor Events
@dataclass(frozen=True, kw_only=True)
class N2kDD471:
    motor_over_temperature_cutout: int = 0
    motor_over_current_cutout: int = 0
    low_oil_level_warning: int = 0
    oil_over_temperature_warning: int = 0
    controller_under_voltage_cutout: int = 0
    manufacturer_defined: int = 0
    reserved: int = 0
    data_not_available: int = 0

    @property
    def events(self) -> int:
        return (
            self.motor_over_temperature_cutout << 0
            | self.motor_over_current_cutout << 1
            | self.low_oil_level_warning << 2
            | self.oil_over_temperature_warning << 3
            | self.controller_under_voltage_cutout << 4
            | self.manufacturer_defined << 5
            | self.reserved << 6
            | self.data_not_available << 7
        )

    @staticmethod
    def from_events(value: int) -> "N2kDD471":
        return N2kDD471(
            motor_over_temperature_cutout=(value >> 0) & 0b1,
            motor_over_current_cutout=(value >> 1) & 0b1,
            low_oil_level_warning=(value >> 2) & 0b1,
            oil_over_temperature_warning=(value >> 3) & 0b1,
            controller_under_voltage_cutout=(value >> 4) & 0b1,
            manufacturer_defined=(value >> 5) & 0b1,
            reserved=(value >> 6) & 0b1,
            data_not_available=(value >> 7) & 0b1,
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, N2kDD471):
            return self.events == other.events
        if isinstance(other, int):
            return self.events == other
        return False


# Thruster Direction Control
class N2kDD473(IntEnum):
    OFF = 0
    ThrusterReady = 1
    ThrusterToPORT = 2
    ThrusterToSTARBOARD = 3


# Thruster Retraction
class N2kDD474(IntEnum):
    OFF = 0
    Extend = 1
    Retract = 2


# Thruster Control Events
@dataclass(frozen=True, kw_only=True)
class N2kDD475:
    another_device_controlling_thruster: int = 0
    boat_speed_to_fast: int = 0

    @property
    def events(self) -> int:
        return (
            self.another_device_controlling_thruster << 0 | self.boat_speed_to_fast << 1
        )

    @staticmethod
    def from_events(value: int) -> "N2kDD475":
        return N2kDD475(
            another_device_controlling_thruster=(value >> 0) & 0b1,
            boat_speed_to_fast=(value >> 1) & 0b1,
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, N2kDD475):
            return self.events == other.events
        if isinstance(other, int):
            return self.events == other
        return False


# DD477 - Windlass Monitoring Events
@dataclass(frozen=True, kw_only=True)
class N2kDD477:
    controller_under_voltage_cutout: int = 0
    controller_over_current_cutout: int = 0
    controller_over_temperature_cutout: int = 0

    @property
    def events(self) -> int:
        return (
            self.controller_under_voltage_cutout << 0
            | self.controller_over_current_cutout << 1
            | self.controller_over_temperature_cutout << 2
        )

    @staticmethod
    def from_events(value: int) -> "N2kDD477":
        return N2kDD477(
            controller_under_voltage_cutout=(value >> 0) & 0b1,
            controller_over_current_cutout=(value >> 1) & 0b1,
            controller_over_temperature_cutout=(value >> 2) & 0b1,
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, N2kDD477):
            return self.events == other.events
        if isinstance(other, int):
            return self.events == other
        return False


# DD478 - Windlass Control Events
@dataclass(frozen=True, kw_only=True)
class N2kDD478:
    another_device_controlling_windlass: int = 0

    @property
    def events(self) -> int:
        return self.another_device_controlling_windlass

    @staticmethod
    def from_events(value: int) -> "N2kDD478":
        return N2kDD478(
            another_device_controlling_windlass=(value >> 0) & 0b1,
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, N2kDD478):
            return self.events == other.events
        if isinstance(other, int):
            return self.events == other
        return False


# DD480 - Windlass Motion States
class N2kDD480(IntEnum):
    WindlassStopped = 0
    DeploymentOccurring = 1
    RetrievalOccurring = 2
    Unavailable = 3


#  DD481 - Rode Type States
class N2kDD481(IntEnum):
    ChainPresentlyDetected = 0
    RopePresentlyDetected = 1
    Error = 2
    Unavailable = 3


# DD482 - Anchor Docking States
class N2kDD482(IntEnum):
    NotDocked = 0
    FullyDocked = 1
    Error = 2
    DataNotAvailable = 3


# DD483 - Windlass Operating Events
@dataclass(frozen=True, kw_only=True)
class N2kDD483:
    system_error: int = 0
    sensor_error: int = 0
    no_windlass_motion_detected: int = 0
    retrieval_docking_distance_reached: int = 0
    end_of_rode_reached: int = 0

    @property
    def event(self) -> int:
        return (
            self.system_error << 0
            | self.sensor_error << 1
            | self.no_windlass_motion_detected << 2
            | self.retrieval_docking_distance_reached << 3
            | self.end_of_rode_reached << 4
        )

    @staticmethod
    def from_event(value: int) -> "N2kDD483":
        return N2kDD483(
            system_error=(value >> 0) & 0b1,
            sensor_error=(value >> 1) & 0b1,
            no_windlass_motion_detected=(value >> 2) & 0b1,
            retrieval_docking_distance_reached=(value >> 3) & 0b1,
            end_of_rode_reached=(value >> 4) & 0b1,
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, N2kDD483):
            return self.event == other.event
        if isinstance(other, int):
            return self.event == other
        return False


# DD484 - Windlass Direction Control
class N2kDD484(IntEnum):
    Off = 0  # Status only / cannot command
    Down = 1
    Up = 2
    Reserved = 3


# DD487 - Motor Power Type
class N2kDD487(IntEnum):
    N2kDD487_12VDC = 0
    N2kDD487_24VDC = 1
    N2kDD487_48VDC = 2
    N2kDD487_24VAC = 3
    N2kDD487_Hydraulic = 4


# DD488 - Speed Type
class N2kDD488(IntEnum):
    SingleSpeed = 0
    DualSpeed = 1
    ProportionalSpeed = 2
    DataNotAvailable = 3
