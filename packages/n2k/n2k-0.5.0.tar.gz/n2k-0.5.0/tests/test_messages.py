from n2k import messages, types
from n2k.n2k import PGN


def test_system_time_message() -> None:
    system_time = messages.SystemTime(
        system_date=20_205,
        system_time=28_136,
        time_source=types.N2kTimeSource.LocalCrystalClock,
        sid=123,
    )
    msg = messages.create_n2k_system_time_message(system_time)
    assert messages.parse_n2k_system_time(msg) == system_time


def test_empty_system_time_message() -> None:
    system_time = messages.SystemTime(
        system_date=None,
        system_time=None,
        time_source=types.N2kTimeSource.GPS,
        sid=None,
    )
    msg = messages.create_n2k_system_time_message(system_time)
    print(msg)
    assert messages.parse_n2k_system_time(msg) == system_time


def test_ais_safety_related_broadcast_message() -> None:
    ais_safety = messages.AISSafetyRelatedBroadcast(
        message_id=types.N2kAISMessageID.Safety_related_broadcast_message,
        repeat=types.N2kAISRepeat.Initial,
        source_id=123456789,
        ais_transceiver_information=types.N2kAISTransceiverInformation.Channel_A_VDL_reception,
        safety_related_text="Test message",
    )
    msg = messages.create_n2k_ais_related_broadcast_msg_message(ais_safety)
    assert messages.parse_n2k_ais_related_broadcast_msg(msg) == ais_safety


def test_empty_ais_safety_related_broadcast_message() -> None:
    ais_safety = messages.AISSafetyRelatedBroadcast(
        message_id=types.N2kAISMessageID.Safety_related_broadcast_message,
        repeat=types.N2kAISRepeat.Initial,
        source_id=None,
        ais_transceiver_information=types.N2kAISTransceiverInformation.Channel_A_VDL_reception,
        safety_related_text=None,
    )
    msg = messages.create_n2k_ais_related_broadcast_msg_message(ais_safety)
    assert messages.parse_n2k_ais_related_broadcast_msg(msg) == ais_safety


def test_mob_notification_message() -> None:
    mob_notification = messages.MOBNotification(
        mob_emitter_id=12345,
        mob_status=types.N2kMOBStatus.MOBEmitterActivated,
        activation_time=12.321,
        position_source=types.N2kMOBPositionSource.PositionEstimatedByVessel,
        position_date=20_205,
        position_time=28_136,
        latitude=13.162258,
        longitude=52.426179,
        cog_reference=types.N2kHeadingReference.magnetic,
        cog=1.5707,
        sog=3.5,
        mmsi=123456789,
        mob_emitter_battery_status=types.N2kMOBEmitterBatteryStatus.Good,
        sid=123,
    )
    msg = messages.create_n2k_mob_notification_message(mob_notification)
    assert messages.parse_n2k_mob_notification(msg) == mob_notification


def test_empty_mob_notification_message() -> None:
    mob_notification = messages.MOBNotification(
        mob_emitter_id=None,
        mob_status=types.N2kMOBStatus.MOBNotActive,
        activation_time=None,
        position_source=types.N2kMOBPositionSource.PositionReportedByMOBEmitter,
        position_date=None,
        position_time=None,
        latitude=None,
        longitude=None,
        cog_reference=types.N2kHeadingReference.Unavailable,
        cog=None,
        sog=None,
        mmsi=None,
        mob_emitter_battery_status=types.N2kMOBEmitterBatteryStatus.Low,
        sid=None,
    )
    msg = messages.create_n2k_mob_notification_message(mob_notification)
    assert messages.parse_n2k_mob_notification(msg) == mob_notification


def test_heading_track_control_message() -> None:
    heading_track_control = messages.HeadingTrackControl(
        rudder_limit_exceeded=types.N2kOnOff.On,
        off_heading_limit_exceeded=types.N2kOnOff.On,
        off_track_limit_exceeded=types.N2kOnOff.On,
        override=types.N2kOnOff.On,
        steering_mode=types.N2kSteeringMode.HeadingControlStandalone,
        turn_mode=types.N2kTurnMode.Unavailable,
        heading_reference=types.N2kHeadingReference.magnetic,
        commanded_rudder_direction=types.N2kRudderDirectionOrder.MoveToPort,
        commanded_rudder_angle=0.1,
        heading_to_steer_course=1.112,
        track=1.2,
        rudder_limit=3.0,
        off_heading_limit=0.1,
        radius_of_turn_order=123.0,
        rate_of_turn_order=0.8,
        off_track_limit=10,
        vessel_heading=0.4,
    )
    msg = messages.create_n2k_heading_track_control_message(heading_track_control)
    assert messages.parse_n2k_heading_track_control(msg) == heading_track_control


def test_empty_heading_track_control_message() -> None:
    heading_track_control = messages.HeadingTrackControl(
        rudder_limit_exceeded=types.N2kOnOff.Unavailable,
        off_heading_limit_exceeded=types.N2kOnOff.Unavailable,
        off_track_limit_exceeded=types.N2kOnOff.Unavailable,
        override=types.N2kOnOff.Unavailable,
        steering_mode=types.N2kSteeringMode.Unavailable,
        turn_mode=types.N2kTurnMode.Unavailable,
        heading_reference=types.N2kHeadingReference.Unavailable,
        commanded_rudder_direction=types.N2kRudderDirectionOrder.Unavailable,
        commanded_rudder_angle=None,
        heading_to_steer_course=None,
        track=None,
        rudder_limit=None,
        off_heading_limit=None,
        radius_of_turn_order=None,
        rate_of_turn_order=None,
        off_track_limit=None,
        vessel_heading=None,
    )
    msg = messages.create_n2k_heading_track_control_message(heading_track_control)
    assert messages.parse_n2k_heading_track_control(msg) == heading_track_control


def test_rudder_message() -> None:
    rudder = messages.Rudder(
        rudder_position=0.5,
        instance=1,
        rudder_direction_order=types.N2kRudderDirectionOrder.MoveToStarboard,
        angle_order=0.6,
    )
    msg = messages.create_n2k_rudder_message(rudder)
    assert messages.parse_n2k_rudder(msg) == rudder


def test_empty_rudder_message() -> None:
    rudder = messages.Rudder(
        rudder_position=None,
        instance=None,
        rudder_direction_order=types.N2kRudderDirectionOrder.Unavailable,
        angle_order=None,
    )
    msg = messages.create_n2k_rudder_message(rudder)
    assert messages.parse_n2k_rudder(msg) == rudder


def test_heading_message() -> None:
    heading = messages.Heading(
        heading=1.2,
        deviation=0.1,
        variation=0.2,
        ref=types.N2kHeadingReference.magnetic,
        sid=123,
    )
    msg = messages.create_n2k_heading_message(heading)
    assert messages.parse_n2k_heading(msg) == heading


def test_empty_heading_message() -> None:
    heading = messages.Heading(
        heading=None,
        deviation=None,
        variation=None,
        ref=types.N2kHeadingReference.Unavailable,
        sid=None,
    )
    msg = messages.create_n2k_heading_message(heading)
    assert messages.parse_n2k_heading(msg) == heading


def test_rate_of_turn_message() -> None:
    rate_of_turn = messages.RateOfTurn(
        rate_of_turn=0.5,
        sid=123,
    )
    msg = messages.create_n2k_rate_of_turn_message(rate_of_turn)
    assert messages.parse_n2k_rate_of_turn(msg) == rate_of_turn


def test_empty_rate_of_turn_message() -> None:
    rate_of_turn = messages.RateOfTurn(
        rate_of_turn=None,
        sid=None,
    )
    msg = messages.create_n2k_rate_of_turn_message(rate_of_turn)
    assert messages.parse_n2k_rate_of_turn(msg) == rate_of_turn


def test_heave_message() -> None:
    heave = messages.Heave(
        heave=0.5,
        delay=0.1,
        delay_source=types.N2kDelaySource.factory_default,
        sid=123,
    )
    msg = messages.create_n2k_heave_message(heave)
    assert messages.parse_n2k_heave(msg) == heave


def test_empty_heave_message() -> None:
    heave = messages.Heave(
        heave=None,
        delay=None,
        delay_source=types.N2kDelaySource.data_not_available,
        sid=None,
    )
    msg = messages.create_n2k_heave_message(heave)
    assert messages.parse_n2k_heave(msg) == heave


def test_attitude_message() -> None:
    attitude = messages.Attitude(
        yaw=0.3,
        roll=0.1,
        pitch=0.2,
        sid=123,
    )
    msg = messages.create_n2k_attitude_message(attitude)
    assert messages.parse_n2k_attitude(msg) == attitude


def test_empty_attitude_message() -> None:
    attitude = messages.Attitude(
        yaw=None,
        roll=None,
        pitch=None,
        sid=None,
    )
    msg = messages.create_n2k_attitude_message(attitude)
    assert messages.parse_n2k_attitude(msg) == attitude


def test_magnetic_variation_message() -> None:
    magnetic_variation = messages.MagneticVariation(
        variation=0.5,
        days_since_1970=20_205,
        source=types.N2kMagneticVariation.Manual,
        sid=123,
    )
    msg = messages.create_n2k_magnetic_variation_message(magnetic_variation)
    assert messages.parse_n2k_magnetic_variation(msg) == magnetic_variation


def test_empty_magnetic_variation_message() -> None:
    magnetic_variation = messages.MagneticVariation(
        variation=None,
        days_since_1970=None,
        source=types.N2kMagneticVariation.Manual,
        sid=None,
    )
    msg = messages.create_n2k_magnetic_variation_message(magnetic_variation)
    assert messages.parse_n2k_magnetic_variation(msg) == magnetic_variation


def test_engine_parameters_rapid_message() -> None:
    engine_parameters = messages.EngineParametersRapid(
        engine_instance=0,
        engine_speed=555.5,
        engine_boost_pressure=1200,
        engine_tilt_trim=52,
    )
    msg = messages.create_n2k_engine_parameters_rapid_message(engine_parameters)
    assert messages.parse_n2k_engine_parameters_rapid(msg) == engine_parameters


def test_empty_engine_parameters_rapid_message() -> None:
    engine_parameters = messages.EngineParametersRapid(
        engine_instance=None,
        engine_speed=None,
        engine_boost_pressure=None,
        engine_tilt_trim=None,
    )
    msg = messages.create_n2k_engine_parameters_rapid_message(engine_parameters)
    assert messages.parse_n2k_engine_parameters_rapid(msg) == engine_parameters


def test_engine_parameters_dynamic_message() -> None:
    status1 = types.N2kEngineDiscreteStatus1()
    status2 = types.N2kEngineDiscreteStatus2()
    engine_parameters = messages.EngineParametersDynamic(
        engine_instance=0,
        engine_oil_press=400,
        engine_oil_temp=403.1,
        engine_coolant_temp=364.1,
        alternator_voltage=13.9,
        fuel_rate=50.5,
        engine_hours=17_283_600,
        engine_coolant_press=1200,
        engine_fuel_press=456000,
        engine_load=20,
        engine_torque=33,
        status1=status1,
        status2=status2,
    )
    msg = messages.create_n2k_engine_parameters_dynamic_message(engine_parameters)
    assert messages.parse_n2k_engine_parameters_dynamic(msg) == engine_parameters


def test_empty_engine_parameters_dynamic_message() -> None:
    status1 = types.N2kEngineDiscreteStatus1()
    status2 = types.N2kEngineDiscreteStatus2()
    engine_parameters = messages.EngineParametersDynamic(
        engine_instance=None,
        engine_oil_press=None,
        engine_oil_temp=None,
        engine_coolant_temp=None,
        alternator_voltage=None,
        fuel_rate=None,
        engine_hours=None,
        engine_coolant_press=None,
        engine_fuel_press=None,
        engine_load=None,
        engine_torque=None,
        status1=status1,
        status2=status2,
    )
    msg = messages.create_n2k_engine_parameters_dynamic_message(engine_parameters)
    assert messages.parse_n2k_engine_parameters_dynamic(msg) == engine_parameters


def test_transmission_parameters_dynamic_message() -> None:
    status1 = types.N2kTransmissionDiscreteStatus1()
    transmission_parameters = messages.TransmissionParametersDynamic(
        engine_instance=0,
        transmission_gear=types.N2kTransmissionGear.Forward,
        oil_pressure=1500,
        oil_temperature=410.5,
        discrete_status1=status1,
    )
    msg = messages.create_n2k_transmission_parameters_dynamic_message(
        transmission_parameters,
    )
    assert (
        messages.parse_n2k_transmission_parameters_dynamic(msg)
        == transmission_parameters
    )


def test_empty_transmission_parameters_dynamic_message() -> None:
    status1 = types.N2kTransmissionDiscreteStatus1()
    transmission_parameters = messages.TransmissionParametersDynamic(
        engine_instance=None,
        transmission_gear=types.N2kTransmissionGear.Unknown,
        oil_pressure=None,
        oil_temperature=None,
        discrete_status1=status1,
    )
    msg = messages.create_n2k_transmission_parameters_dynamic_message(
        transmission_parameters,
    )
    assert (
        messages.parse_n2k_transmission_parameters_dynamic(msg)
        == transmission_parameters
    )


def test_trip_parameters_engine_message() -> None:
    trip_parameters = messages.TripFuelConsumptionEngine(
        engine_instance=0,
        trip_fuel_used=10,
        fuel_rate_average=14.4,
        fuel_rate_economy=10.1,
        instantaneous_fuel_economy=31.1,
    )
    msg = messages.create_n2k_trip_parameters_engine_message(trip_parameters)
    assert messages.parse_n2k_trip_parameters_engine(msg) == trip_parameters


def test_empty_trip_parameters_engine_message() -> None:
    trip_parameters = messages.TripFuelConsumptionEngine(
        engine_instance=None,
        trip_fuel_used=None,
        fuel_rate_average=None,
        fuel_rate_economy=None,
        instantaneous_fuel_economy=None,
    )
    msg = messages.create_n2k_trip_parameters_engine_message(trip_parameters)
    assert messages.parse_n2k_trip_parameters_engine(msg) == trip_parameters


def test_binary_status_report_message() -> None:
    binary_status_report = messages.BinaryStatusReport(
        device_bank_instance=30,
        bank_status=131132,
    )
    msg = messages.create_n2k_binary_status_report_message(binary_status_report)
    assert messages.parse_n2k_binary_status_report(msg) == binary_status_report


def test_empty_binary_status_report_message() -> None:
    binary_status_report = messages.BinaryStatusReport(
        device_bank_instance=255,
        bank_status=0,
    )
    msg = messages.create_n2k_binary_status_report_message(binary_status_report)
    assert messages.parse_n2k_binary_status_report(msg) == binary_status_report


def test_switch_bank_control_message() -> None:
    switch_bank_control = messages.SwitchBankControl(
        target_bank_instance=30,
        bank_status=131132,
    )
    msg = messages.create_n2k_switch_bank_control_message(switch_bank_control)
    assert messages.parse_n2k_switch_bank_control(msg) == switch_bank_control


def test_empty_switch_bank_control_message() -> None:
    switch_bank_control = messages.SwitchBankControl(
        target_bank_instance=255,
        bank_status=0,
    )
    msg = messages.create_n2k_switch_bank_control_message(switch_bank_control)
    assert messages.parse_n2k_switch_bank_control(msg) == switch_bank_control


def test_fluid_level_message() -> None:
    fluid_level = messages.FluidLevel(
        instance=0,
        fluid_type=types.N2kFluidType.Fuel,
        level=0.5,
        capacity=300.5,
    )
    msg = messages.create_n2k_fluid_level_message(fluid_level)
    assert messages.parse_n2k_fluid_level(msg) == fluid_level


def test_empty_fluid_level_message() -> None:
    fluid_level = messages.FluidLevel(
        instance=15,
        fluid_type=types.N2kFluidType.Unavailable,
        level=None,
        capacity=None,
    )
    msg = messages.create_n2k_fluid_level_message(fluid_level)
    assert messages.parse_n2k_fluid_level(msg) == fluid_level


def test_dc_detailed_status_message() -> None:
    dc_detailed_status = messages.DCDetailedStatus(
        dc_instance=50,
        dc_type=types.N2kDCType.Battery,
        state_of_charge=45,
        state_of_health=83,
        time_remaining=4560,
        ripple_voltage=0.421,
        capacity=144_000,
    )
    msg = messages.create_n2k_dc_detailed_status_message(dc_detailed_status)
    assert messages.parse_n2k_dc_detailed_status(msg) == dc_detailed_status


def test_empty_dc_detailed_status_message() -> None:
    dc_detailed_status = messages.DCDetailedStatus(
        dc_instance=None,
        dc_type=types.N2kDCType.Battery,
        state_of_charge=None,
        state_of_health=None,
        time_remaining=None,
        ripple_voltage=None,
        capacity=None,
    )
    msg = messages.create_n2k_dc_detailed_status_message(dc_detailed_status)
    assert messages.parse_n2k_dc_detailed_status(msg) == dc_detailed_status


def test_charger_status_message() -> None:
    charger_status = messages.ChargerStatus(
        instance=0,
        battery_instance=34,
        charge_state=types.N2kChargeState.Bulk,
        charger_mode=types.N2kChargerMode.Primary,
        enabled=types.N2kOnOff.On,
        equalization_pending=types.N2kOnOff.On,
        equalization_time_remaining=12_360,
    )
    msg = messages.create_n2k_charger_status_message(charger_status)
    assert messages.parse_n2k_charger_status(msg) == charger_status


def test_empty_charger_status_message() -> None:
    charger_status = messages.ChargerStatus(
        instance=None,
        battery_instance=None,
        charge_state=types.N2kChargeState.Unavailable,
        charger_mode=types.N2kChargerMode.Unavailable,
        enabled=types.N2kOnOff.Unavailable,
        equalization_pending=types.N2kOnOff.Unavailable,
        equalization_time_remaining=None,
    )
    msg = messages.create_n2k_charger_status_message(charger_status)
    assert messages.parse_n2k_charger_status(msg) == charger_status


def test_battery_status_message() -> None:
    battery_status = messages.BatteryStatus(
        battery_instance=0,
        battery_voltage=12.25,
        battery_current=0.4,
        battery_temperature=313.16,
        sid=123,
    )
    msg = messages.create_n2k_battery_status_message(battery_status)
    assert messages.parse_n2k_battery_status(msg) == battery_status


def test_empty_battery_status_message() -> None:
    battery_status = messages.BatteryStatus(
        battery_instance=None,
        battery_voltage=None,
        battery_current=None,
        battery_temperature=None,
        sid=None,
    )
    msg = messages.create_n2k_battery_status_message(battery_status)
    assert messages.parse_n2k_battery_status(msg) == battery_status


def test_charger_configuration_status_message() -> None:
    charger_configuration_status = messages.ChargerConfigurationStatus(
        charger_instance=123,
        battery_instance=34,
        enable=types.N2kOnOff.On,
        charge_current_limit=240,
        charging_algorithm=types.N2kChargingAlgorithm.ThreeStage,
        charger_mode=types.N2kChargerMode.Primary,
        battery_temperature=types.N2kBattTempNoSensor.Warm,
        equalization_enabled=types.N2kOnOff.On,
        over_charge_enable=types.N2kOnOff.On,
        equalization_time_remaining=12_360,
    )
    msg = messages.create_n2k_charger_configuration_status_message(
        charger_configuration_status,
    )
    assert (
        messages.parse_n2k_charger_configuration_status(msg)
        == charger_configuration_status
    )


def test_empty_charger_configuration_status_message() -> None:
    charger_configuration_status = messages.ChargerConfigurationStatus(
        charger_instance=None,
        battery_instance=None,
        enable=types.N2kOnOff.Unavailable,
        charge_current_limit=None,
        charging_algorithm=types.N2kChargingAlgorithm.NotAvailable,
        charger_mode=types.N2kChargerMode.Unavailable,
        battery_temperature=types.N2kBattTempNoSensor.NotAvailable,
        equalization_enabled=types.N2kOnOff.Unavailable,
        over_charge_enable=types.N2kOnOff.Unavailable,
        equalization_time_remaining=None,
    )
    msg = messages.create_n2k_charger_configuration_status_message(
        charger_configuration_status,
    )
    assert (
        messages.parse_n2k_charger_configuration_status(msg)
        == charger_configuration_status
    )


def test_battery_configuration_status_message() -> None:
    battery_configuration_status = messages.BatteryConfigurationStatus(
        battery_instance=0,
        battery_type=types.N2kBatType.Gel,
        supports_equal=types.N2kBatEqSupport.Yes,
        battery_nominal_voltage=types.N2kBatNomVolt.Volt_12,
        battery_chemistry=types.N2kBatChem.LeadAcid,
        battery_capacity=144_000,
        battery_temperature_coefficient=20,
        peukert_exponent=1.2,
        charge_efficiency_factor=3,
    )
    msg = messages.create_n2k_battery_configuration_status_message(
        battery_configuration_status,
    )
    assert (
        messages.parse_n2k_battery_configuration_status(msg)
        == battery_configuration_status
    )


def test_empty_battery_configuration_status_message() -> None:
    battery_configuration_status = messages.BatteryConfigurationStatus(
        battery_instance=None,
        battery_type=types.N2kBatType.Flooded,
        supports_equal=types.N2kBatEqSupport.Unavailable,
        battery_nominal_voltage=types.N2kBatNomVolt.Volt_6,
        battery_chemistry=types.N2kBatChem.LeadAcid,
        battery_capacity=None,
        battery_temperature_coefficient=None,
        peukert_exponent=None,
        charge_efficiency_factor=None,
    )
    msg = messages.create_n2k_battery_configuration_status_message(
        battery_configuration_status,
    )
    assert (
        messages.parse_n2k_battery_configuration_status(msg)
        == battery_configuration_status
    )


def test_converter_status_message() -> None:
    converter_status = messages.ConverterStatus(
        connection_number=135,
        operating_state=types.N2kConvMode.Float,
        temperature_state=types.N2kTemperatureState.Warning,
        overload_state=types.N2kOverloadState.Overload,
        low_dc_voltage_state=types.N2kDCVoltageState.Low,
        ripple_state=types.N2kRippleState.Warning,
        sid=135,
    )
    msg = messages.create_n2k_converter_status_message(converter_status)
    assert messages.parse_n2k_converter_status(msg) == converter_status


def test_empty_converter_status_message() -> None:
    converter_status = messages.ConverterStatus(
        connection_number=None,
        operating_state=types.N2kConvMode.NotAvailable,
        temperature_state=types.N2kTemperatureState.NotAvailable,
        overload_state=types.N2kOverloadState.NotAvailable,
        low_dc_voltage_state=types.N2kDCVoltageState.NotAvailable,
        ripple_state=types.N2kRippleState.NotAvailable,
        sid=None,
    )
    msg = messages.create_n2k_converter_status_message(converter_status)
    assert messages.parse_n2k_converter_status(msg) == converter_status


def test_leeway_message() -> None:
    leeway = messages.Leeway(
        leeway=1.002,
        sid=135,
    )
    msg = messages.create_n2k_leeway_message(leeway)
    assert messages.parse_n2k_leeway(msg) == leeway


def test_empty_leeway_message() -> None:
    leeway = messages.Leeway(
        leeway=None,
        sid=None,
    )
    msg = messages.create_n2k_leeway_message(leeway)
    assert messages.parse_n2k_leeway(msg) == leeway


def test_boat_speed_message() -> None:
    boat_speed = messages.BoatSpeed(
        water_referenced=3.14,
        ground_referenced=2.71,
        swrt=types.N2kSpeedWaterReferenceType.PaddleWheel,
        sid=135,
    )
    msg = messages.create_n2k_boat_speed_message(boat_speed)
    assert messages.parse_n2k_boat_speed(msg) == boat_speed


def test_empty_boat_speed_message() -> None:
    boat_speed = messages.BoatSpeed(
        water_referenced=None,
        ground_referenced=None,
        swrt=types.N2kSpeedWaterReferenceType.Unavailable,
        sid=None,
    )
    msg = messages.create_n2k_boat_speed_message(boat_speed)
    assert messages.parse_n2k_boat_speed(msg) == boat_speed


def test_water_depth_message() -> None:
    water_depth = messages.WaterDepth(
        depth_below_transducer=120.25,
        offset=-0.305,
        max_range=300,
        sid=135,
    )
    msg = messages.create_n2k_water_depth_message(water_depth)
    assert messages.parse_n2k_water_depth(msg) == water_depth


def test_empty_water_depth_message() -> None:
    water_depth = messages.WaterDepth(
        depth_below_transducer=None,
        offset=None,
        max_range=None,
        sid=None,
    )
    msg = messages.create_n2k_water_depth_message(water_depth)
    assert messages.parse_n2k_water_depth(msg) == water_depth


def test_distance_log_message() -> None:
    distance_log = messages.DistanceLog(
        days_since_1970=20_205,
        seconds_since_midnight=28_136.1234,
        log=12345,
        trip_log=123,
    )
    msg = messages.create_n2k_distance_log_message(distance_log)
    assert messages.parse_n2k_distance_log(msg) == distance_log


def test_empty_distance_log_message() -> None:
    distance_log = messages.DistanceLog(
        days_since_1970=None,
        seconds_since_midnight=None,
        log=None,
        trip_log=None,
    )
    msg = messages.create_n2k_distance_log_message(distance_log)
    assert messages.parse_n2k_distance_log(msg) == distance_log


def test_anchor_windlass_control_status_message() -> None:
    anchor_windlass_control_status = messages.AnchorWindlassControlStatus(
        windlass_identifier=152,
        windlass_direction_control=types.N2kWindlassDirectionControl.Up,
        speed_control=90,
        speed_control_type=types.N2kSpeedType.DualSpeed,
        anchor_docking_control=types.N2kGenericStatusPair.Yes,
        power_enable=types.N2kGenericStatusPair.No,
        mechanical_lock=types.N2kGenericStatusPair.Yes,
        deck_and_anchor_wash=types.N2kGenericStatusPair.No,
        anchor_light=types.N2kGenericStatusPair.Yes,
        command_timeout=1.115,
        windlass_control_events=types.N2kWindlassControlEvents.from_events(1),
    )
    msg = messages.create_n2k_anchor_windlass_control_status_message(
        anchor_windlass_control_status,
    )
    assert (
        messages.parse_n2k_anchor_windlass_control_status(msg)
        == anchor_windlass_control_status
    )


def test_empty_anchor_windlass_control_status_message() -> None:
    anchor_windlass_control_status = messages.AnchorWindlassControlStatus(
        windlass_identifier=None,
        windlass_direction_control=types.N2kWindlassDirectionControl.Reserved,
        speed_control=None,
        speed_control_type=types.N2kSpeedType.DataNotAvailable,
        anchor_docking_control=types.N2kGenericStatusPair.Unavailable,
        power_enable=types.N2kGenericStatusPair.Unavailable,
        mechanical_lock=types.N2kGenericStatusPair.Unavailable,
        deck_and_anchor_wash=types.N2kGenericStatusPair.Unavailable,
        anchor_light=types.N2kGenericStatusPair.Unavailable,
        command_timeout=None,
        windlass_control_events=types.N2kWindlassControlEvents.from_events(0),
    )
    msg = messages.create_n2k_anchor_windlass_control_status_message(
        anchor_windlass_control_status,
    )
    assert (
        messages.parse_n2k_anchor_windlass_control_status(msg)
        == anchor_windlass_control_status
    )


def test_anchor_windlass_operating_status_message() -> None:
    anchor_windlass_operating_status = messages.AnchorWindlassOperatingStatus(
        windlass_identifier=152,
        rode_counter_value=123.4,
        windlass_line_speed=34.6,
        windlass_motion_status=types.N2kWindlassMotionStates.RetrievalOccurring,
        rode_type_status=types.N2kRodeTypeStates.ChainPresentlyDetected,
        anchor_docking_status=types.N2kAnchorDockingStates.DataNotAvailable,
        windlass_operating_events=types.N2kWindlassOperatingEvents.from_event(1),
        sid=135,
    )
    msg = messages.create_n2k_anchor_windlass_operating_status_message(
        anchor_windlass_operating_status,
    )
    assert (
        messages.parse_n2k_anchor_windlass_operating_status(msg)
        == anchor_windlass_operating_status
    )


def test_empty_anchor_windlass_operating_status_message() -> None:
    anchor_windlass_operating_status = messages.AnchorWindlassOperatingStatus(
        windlass_identifier=None,
        rode_counter_value=None,
        windlass_line_speed=None,
        windlass_motion_status=types.N2kWindlassMotionStates.Unavailable,
        rode_type_status=types.N2kRodeTypeStates.Unavailable,
        anchor_docking_status=types.N2kAnchorDockingStates.DataNotAvailable,
        windlass_operating_events=types.N2kWindlassOperatingEvents.from_event(0),
        sid=None,
    )
    msg = messages.create_n2k_anchor_windlass_operating_status_message(
        anchor_windlass_operating_status,
    )
    assert (
        messages.parse_n2k_anchor_windlass_operating_status(msg)
        == anchor_windlass_operating_status
    )


def test_anchor_windlass_monitoring_status_message() -> None:
    anchor_windlass_monitoring_status = messages.AnchorWindlassMonitoringStatus(
        windlass_identifier=152,
        total_motor_time=2520,
        controller_voltage=12.4,
        motor_current=4,
        windlass_monitoring_events=types.N2kWindlassMonitoringEvents.from_events(1),
        sid=135,
    )
    msg = messages.create_n2k_anchor_windlass_monitoring_status_message(
        anchor_windlass_monitoring_status,
    )
    assert (
        messages.parse_n2k_anchor_windlass_monitoring_status(msg)
        == anchor_windlass_monitoring_status
    )


def test_empty_anchor_windlass_monitoring_status_message() -> None:
    anchor_windlass_monitoring_status = messages.AnchorWindlassMonitoringStatus(
        windlass_identifier=None,
        total_motor_time=None,
        controller_voltage=None,
        motor_current=None,
        windlass_monitoring_events=types.N2kWindlassMonitoringEvents.from_events(0),
        sid=None,
    )
    msg = messages.create_n2k_anchor_windlass_monitoring_status_message(
        anchor_windlass_monitoring_status,
    )
    assert (
        messages.parse_n2k_anchor_windlass_monitoring_status(msg)
        == anchor_windlass_monitoring_status
    )


def test_lat_long_rapid_message() -> None:
    lat_long_rapid = messages.LatLonRapid(
        latitude=13.162258,
        longitude=52.426179,
    )
    msg = messages.create_n2k_lat_long_rapid_message(lat_long_rapid)
    assert messages.parse_n2k_lat_long_rapid(msg) == lat_long_rapid


def test_empty_lat_long_rapid_message() -> None:
    lat_long_rapid = messages.LatLonRapid(
        latitude=None,
        longitude=None,
    )
    msg = messages.create_n2k_lat_long_rapid_message(lat_long_rapid)
    assert messages.parse_n2k_lat_long_rapid(msg) == lat_long_rapid


def test_cog_sog_rapid_message() -> None:
    cog_sog_rapid = messages.CogSogRapid(
        heading_reference=types.N2kHeadingReference.magnetic,
        cog=1.203,
        sog=3.54,
        sid=135,
    )
    msg = messages.create_n2k_cog_sog_rapid_message(cog_sog_rapid)
    assert messages.parse_n2k_cog_sog_rapid(msg) == cog_sog_rapid


def test_empty_cog_sog_rapid_message() -> None:
    cog_sog_rapid = messages.CogSogRapid(
        heading_reference=types.N2kHeadingReference.Unavailable,
        cog=None,
        sog=None,
        sid=None,
    )
    msg = messages.create_n2k_cog_sog_rapid_message(cog_sog_rapid)
    assert messages.parse_n2k_cog_sog_rapid(msg) == cog_sog_rapid


def test_gnss_data_message() -> None:
    gnss_data = messages.GNSSPositionData(
        days_since_1970=20_205,
        seconds_since_midnight=28_136.1234,
        latitude=13.162258134567812,
        longitude=52.42617912345679,
        altitude=23.123458,
        gnss_type=types.N2kGNSSType.GPS_GLONASS,
        gnss_method=types.N2kGNSSMethod.DGNSS,
        n_satellites=8,
        hdop=1.2,
        pdop=1.3,
        geoidal_separation=123.02,
        n_reference_stations=1,
        reference_station_type=types.N2kGNSSType.GPS_GLONASS,
        reference_station_id=1234,
        age_of_correction=23.24,
        sid=135,
    )
    msg = messages.create_n2k_gnss_data_message(gnss_data)
    assert messages.parse_n2k_gnss_data(msg) == gnss_data


def test_empty_gnss_data_message() -> None:
    gnss_data = messages.GNSSPositionData(
        days_since_1970=None,
        seconds_since_midnight=None,
        latitude=None,
        longitude=None,
        altitude=None,
        gnss_type=types.N2kGNSSType.GPS,
        gnss_method=types.N2kGNSSMethod.Unavailable,
        n_satellites=None,
        hdop=None,
        pdop=None,
        geoidal_separation=None,
        n_reference_stations=None,
        reference_station_type=types.N2kGNSSType.GPS,
        reference_station_id=None,
        age_of_correction=None,
        sid=None,
    )
    msg = messages.create_n2k_gnss_data_message(gnss_data)
    assert messages.parse_n2k_gnss_data(msg) == gnss_data


def test_date_time_local_offset_message() -> None:
    date_time_local_offset = messages.DateTimeLocalOffset(
        days_since_1970=20_205,
        seconds_since_midnight=28_136.1234,
        local_offset=15,
        sid=135,
    )
    msg = messages.create_n2k_date_time_local_offset_message(date_time_local_offset)
    assert messages.parse_n2k_date_time_local_offset(msg) == date_time_local_offset


def test_empty_date_time_local_offset_message() -> None:
    date_time_local_offset = messages.DateTimeLocalOffset(
        days_since_1970=None,
        seconds_since_midnight=None,
        local_offset=None,
        sid=None,
    )
    msg = messages.create_n2k_date_time_local_offset_message(date_time_local_offset)
    assert messages.parse_n2k_date_time_local_offset(msg) == date_time_local_offset


def test_ais_class_a_position_message() -> None:
    ais_class_a_position_report = messages.AISClassAPositionReport(
        message_id=types.N2kAISMessageID.Scheduled_Class_A_position_report,
        repeat=types.N2kAISRepeat.Final,
        user_id=123456789,
        latitude=13.162258,
        longitude=52.426179,
        accuracy=True,
        raim=True,
        seconds=62,
        cog=1.203,
        sog=3.21,
        ais_transceiver_information=types.N2kAISTransceiverInformation.Channel_A_VDL_transmission,
        heading=1.213,
        rot=0.3858125,
        nav_status=types.N2kAISNavStatus.Constrained_By_Draught,
        sid=135,
    )
    msg = messages.create_n2k_ais_class_a_position_message(
        ais_class_a_position_report,
    )
    assert messages.parse_n2k_ais_class_a_position(msg) == ais_class_a_position_report


def test_empty_ais_class_a_position_message() -> None:
    ais_class_a_position_report = messages.AISClassAPositionReport(
        message_id=types.N2kAISMessageID.Scheduled_Class_A_position_report,
        repeat=types.N2kAISRepeat.Final,
        user_id=123456789,
        latitude=None,
        longitude=None,
        accuracy=False,
        raim=False,
        seconds=63,
        cog=None,
        sog=None,
        ais_transceiver_information=types.N2kAISTransceiverInformation.Channel_A_VDL_transmission,
        heading=None,
        rot=None,
        nav_status=types.N2kAISNavStatus.Under_Way_Motoring,
        sid=None,
    )
    msg = messages.create_n2k_ais_class_a_position_message(
        ais_class_a_position_report,
    )
    assert messages.parse_n2k_ais_class_a_position(msg) == ais_class_a_position_report


def test_ais_class_b_position_message() -> None:
    ais_class_b_position_report = messages.AISClassBPositionReport(
        message_id=types.N2kAISMessageID.Standard_Class_B_position_report,
        repeat=types.N2kAISRepeat.First,
        user_id=123456789,
        latitude=13.162258,
        longitude=52.426179,
        accuracy=True,
        raim=True,
        seconds=62,
        cog=1.203,
        sog=3.21,
        ais_transceiver_information=types.N2kAISTransceiverInformation.Channel_A_VDL_transmission,
        heading=1.213,
        unit=types.N2kAISUnit.ClassB_SOTDMA,
        display=True,
        dsc=False,
        band=True,
        msg22=False,
        mode=types.N2kAISMode.Autonomous,
        state=True,
        sid=135,
    )
    msg = messages.create_n2k_ais_class_b_position_message(
        ais_class_b_position_report,
    )
    assert messages.parse_n2k_ais_class_b_position(msg) == ais_class_b_position_report


def test_empty_ais_class_b_position_message() -> None:
    ais_class_b_position_report = messages.AISClassBPositionReport(
        message_id=types.N2kAISMessageID.Standard_Class_B_position_report,
        repeat=types.N2kAISRepeat.Final,
        user_id=None,
        latitude=None,
        longitude=None,
        accuracy=False,
        raim=False,
        seconds=63,
        cog=None,
        sog=None,
        ais_transceiver_information=types.N2kAISTransceiverInformation.Reserved,
        heading=None,
        unit=types.N2kAISUnit.ClassB_CS,
        display=False,
        dsc=False,
        band=False,
        msg22=False,
        mode=types.N2kAISMode.Assigned,
        state=False,
        sid=None,
    )
    msg = messages.create_n2k_ais_class_b_position_message(
        ais_class_b_position_report,
    )
    assert messages.parse_n2k_ais_class_b_position(msg) == ais_class_b_position_report


def test_ais_aids_to_navigation_report_message() -> None:
    aids_to_navigation_report = messages.AISAtoNReportData(
        message_id=types.N2kAISMessageID.ATON_report,
        repeat=types.N2kAISRepeat.Final,
        user_id=123456789,
        latitude=13.162258,
        longitude=52.426179,
        accuracy=True,
        raim=False,
        seconds=62,
        length=512.6,
        beam=82.1,
        position_reference_starboard=12.5,
        position_reference_true_north=40.1,
        a_to_n_type=types.N2kAISAtoNType.beacon_safe_water,
        off_position_reference_indicator=True,
        virtual_a_to_n_flag=False,
        assigned_mode_flag=True,
        gnss_type=types.N2kGNSSType.GPS_GLONASS,
        a_to_n_status=2,
        n2k_ais_transceiver_information=types.N2kAISTransceiverInformation.Channel_A_VDL_transmission,
        a_to_n_name="Test AtoN",
    )
    msg = messages.create_n2k_ais_aids_to_navigation_report_message(
        aids_to_navigation_report,
    )
    assert (
        messages.parse_n2k_ais_aids_to_navigation_report(msg)
        == aids_to_navigation_report
    )


def test_empty_ais_aids_to_navigation_report_message() -> None:
    aids_to_navigation_report = messages.AISAtoNReportData(
        message_id=types.N2kAISMessageID.ATON_report,
        repeat=types.N2kAISRepeat.Final,
        user_id=None,
        latitude=None,
        longitude=None,
        accuracy=False,
        raim=False,
        seconds=63,
        length=None,
        beam=None,
        position_reference_starboard=None,
        position_reference_true_north=None,
        a_to_n_type=types.N2kAISAtoNType.not_specified,
        off_position_reference_indicator=False,
        virtual_a_to_n_flag=False,
        assigned_mode_flag=False,
        gnss_type=types.N2kGNSSType.GPS,
        a_to_n_status=None,
        n2k_ais_transceiver_information=types.N2kAISTransceiverInformation.Reserved,
        a_to_n_name=None,
    )
    msg = messages.create_n2k_ais_aids_to_navigation_report_message(
        aids_to_navigation_report,
    )
    assert (
        messages.parse_n2k_ais_aids_to_navigation_report(msg)
        == aids_to_navigation_report
    )


def test_cross_track_error_message() -> None:
    cross_track_error = messages.CrossTrackError(
        xte_mode=types.N2kXTEMode.Differential,
        navigation_terminated=False,
        xte=52041.09,
        sid=135,
    )
    msg = messages.create_n2k_cross_track_error_message(cross_track_error)
    assert messages.parse_n2k_cross_track_error(msg) == cross_track_error


def test_empty_cross_track_error_message() -> None:
    cross_track_error = messages.CrossTrackError(
        xte_mode=types.N2kXTEMode.Manual,
        navigation_terminated=False,
        xte=None,
        sid=None,
    )
    msg = messages.create_n2k_cross_track_error_message(cross_track_error)
    assert messages.parse_n2k_cross_track_error(msg) == cross_track_error


def test_navigation_info_message() -> None:
    navigation_info = messages.NavigationInfo(
        distance_to_waypoint=42949672.94,
        bearing_reference=types.N2kHeadingReference.magnetic,
        perpendicular_crossed=True,
        arrival_circle_entered=False,
        calculation_type=types.N2kDistanceCalculationType.GreatCircle,
        eta_time=28_136.1234,
        eta_date=20_205,
        bearing_origin_to_destination_waypoint=1.2345,
        bearing_position_to_destination_waypoint=2.3456,
        origin_waypoint_number=1234567890,
        destination_waypoint_number=1234567891,
        destination_latitude=13.162258,
        destination_longitude=52.426179,
        waypoint_closing_velocity=123.45,
        sid=135,
    )
    msg = messages.create_n2k_navigation_info_message(navigation_info)
    assert messages.parse_n2k_navigation_info(msg) == navigation_info


def test_empty_navigation_info_message() -> None:
    navigation_info = messages.NavigationInfo(
        distance_to_waypoint=None,
        bearing_reference=types.N2kHeadingReference.Unavailable,
        perpendicular_crossed=False,
        arrival_circle_entered=False,
        calculation_type=types.N2kDistanceCalculationType.RhumbLine,
        eta_time=None,
        eta_date=None,
        bearing_origin_to_destination_waypoint=None,
        bearing_position_to_destination_waypoint=None,
        origin_waypoint_number=None,
        destination_waypoint_number=None,
        destination_latitude=None,
        destination_longitude=None,
        waypoint_closing_velocity=None,
        sid=None,
    )
    msg = messages.create_n2k_navigation_info_message(navigation_info)
    assert messages.parse_n2k_navigation_info(msg) == navigation_info


def test_route_waypoint_information_message() -> None:
    route_waypoint_information = messages.RouteWaypointInformation(
        start=32676,
        database=12345,
        route=32123,
        nav_direction=types.N2kNavigationDirection.reverse,
        route_name="Test Route",
        supplementary_data=types.N2kGenericStatusPair.No,
        waypoints=[
            types.Waypoint(
                id=0,
                name="Waypoint 1",
                latitude=13.162258,
                longitude=52.426179,
            ),
            types.Waypoint(
                id=2,
                name="Waypoint 2",
                latitude=13.362258,
                longitude=52.456179,
            ),
            types.Waypoint(
                id=10,
                name="Waypoint the Third",
                latitude=13.122258,
                longitude=52.026179,
            ),
            types.Waypoint(
                id=32450,
                name="Sir Waypointsalot the Fourth",
                latitude=13.162358,
                longitude=52.426079,
            ),
        ],
    )
    msg = messages.create_n2k_route_waypoint_information_message(
        route_waypoint_information,
    )
    assert (
        messages.parse_n2k_route_waypoint_information(msg) == route_waypoint_information
    )


def test_empty_route_waypoint_information_message() -> None:
    route_waypoint_information = messages.RouteWaypointInformation(
        start=None,
        database=None,
        route=None,
        nav_direction=types.N2kNavigationDirection.unknown,
        route_name=None,
        supplementary_data=types.N2kGenericStatusPair.Unavailable,
        waypoints=[
            types.Waypoint(
                id=None,
                name=None,
                latitude=None,
                longitude=None,
            ),
        ],
    )
    msg = messages.create_n2k_route_waypoint_information_message(
        route_waypoint_information,
    )
    assert (
        messages.parse_n2k_route_waypoint_information(msg) == route_waypoint_information
    )


def test_gnss_dop_message() -> None:
    gnss_dop = messages.GNSSDOPData(
        desired_mode=types.N2kGNSSDOPmode.Unavailable,
        actual_mode=types.N2kGNSSDOPmode.Unavailable,
        hdop=None,
        vdop=None,
        tdop=None,
        sid=None,
    )
    msg = messages.create_n2k_gnss_dop_message(gnss_dop)
    assert messages.parse_n2k_gnss_dop(msg) == gnss_dop


def test_gnss_satellites_in_view_message() -> None:
    gnss_satellites_in_view = messages.GNSSSatellitesInView(
        mode=types.N2kRangeResidualMode.RangeResidualsWereUsedToCalculateData,
        satellites=[
            types.SatelliteInfo(
                prn=0,
                elevation=2.0234,
                azimuth=4.0435,
                snr=30.02,
                range_residuals=4.56789,
                usage_status=types.N2kPRNUsageStatus.NotTracked,
            ),
            types.SatelliteInfo(
                prn=45,
                elevation=0.0234,
                azimuth=1.0435,
                snr=3.02,
                range_residuals=0.6789,
                usage_status=types.N2kPRNUsageStatus.DifferentialCorrectionsAvailable,
            ),
            types.SatelliteInfo(
                prn=125,
                elevation=2.2,
                azimuth=4.0435,
                snr=30.02,
                range_residuals=8.06789,
                usage_status=types.N2kPRNUsageStatus.NotTracked,
            ),
            types.SatelliteInfo(
                prn=250,
                elevation=1.345,
                azimuth=6.0435,
                snr=30.02,
                range_residuals=1.56789,
                usage_status=types.N2kPRNUsageStatus.NotTracked,
            ),
        ],
        sid=135,
    )
    msg = messages.create_n2k_gnss_satellites_in_view_message(
        gnss_satellites_in_view,
    )
    assert messages.parse_n2k_gnss_satellites_in_view(msg) == gnss_satellites_in_view


def test_empty_gnss_satellites_in_view_message() -> None:
    gnss_satellites_in_view = messages.GNSSSatellitesInView(
        mode=types.N2kRangeResidualMode.Unavailable,
        satellites=[
            types.SatelliteInfo(
                prn=None,
                elevation=None,
                azimuth=None,
                snr=None,
                range_residuals=None,
                usage_status=types.N2kPRNUsageStatus.Unavailable,
            ),
        ],
        sid=None,
    )
    msg = messages.create_n2k_gnss_satellites_in_view_message(
        gnss_satellites_in_view,
    )
    assert messages.parse_n2k_gnss_satellites_in_view(msg) == gnss_satellites_in_view


def test_ais_class_a_static_data_message() -> None:
    ais_class_a_static_data = messages.AISClassAStaticData(
        message_id=types.N2kAISMessageID.Scheduled_Class_A_position_report,
        repeat=types.N2kAISRepeat.Initial,
        user_id=123456789,
        imo_number=1234567,
        callsign="LZ1234",
        name="TEST VESSEL",
        vessel_type=120,
        length=123,
        beam=45.2,
        pos_ref_stbd=4.0,
        pos_ref_bow=12.5,
        eta_date=20_205,
        eta_time=28_136.1234,
        draught=3.5,
        destination="TEST DESTINATION",
        ais_version=types.N2kAISVersion.ITU_R_M_1371_1,
        gnss_type=types.N2kGNSSType.GPS_GLONASS,
        dte=types.N2kAISDTE.Ready,
        ais_info=types.N2kAISTransceiverInformation.Channel_A_VDL_transmission,
        sid=135,
    )
    msg = messages.create_n2k_ais_class_a_static_data_message(
        ais_class_a_static_data,
    )
    assert messages.parse_n2k_ais_class_a_static_data(msg) == ais_class_a_static_data


def test_empty_ais_class_a_static_data_message() -> None:
    ais_class_a_static_data = messages.AISClassAStaticData(
        message_id=types.N2kAISMessageID.Scheduled_Class_A_position_report,
        repeat=types.N2kAISRepeat.Initial,
        user_id=None,
        imo_number=None,
        callsign=None,
        name=None,
        vessel_type=None,
        length=None,
        beam=None,
        pos_ref_stbd=None,
        pos_ref_bow=None,
        eta_date=None,
        eta_time=None,
        draught=None,
        destination=None,
        ais_version=types.N2kAISVersion.ITU_R_M_1371_3,
        gnss_type=types.N2kGNSSType.Galileo,
        dte=types.N2kAISDTE.NotReady,
        ais_info=types.N2kAISTransceiverInformation.Channel_A_VDL_transmission,
        sid=None,
    )
    msg = messages.create_n2k_ais_class_a_static_data_message(
        ais_class_a_static_data,
    )
    assert messages.parse_n2k_ais_class_a_static_data(msg) == ais_class_a_static_data


def test_ais_class_b_static_data_part_a_message() -> None:
    ais_class_b_static_data_part_a = messages.AISClassBStaticDataPartA(
        message_id=types.N2kAISMessageID.Standard_Class_B_position_report,
        repeat=types.N2kAISRepeat.Final,
        user_id=123456789,
        name="TEST VESSEL",
        ais_info=types.N2kAISTransceiverInformation.Channel_A_VDL_transmission,
        sid=135,
    )
    msg = messages.create_n2k_ais_class_b_static_data_part_a_message(
        ais_class_b_static_data_part_a,
    )
    assert (
        messages.parse_n2k_ais_class_b_static_data_part_a(msg)
        == ais_class_b_static_data_part_a
    )


def test_empty_ais_class_b_static_data_part_a_message() -> None:
    ais_class_b_static_data_part_a = messages.AISClassBStaticDataPartA(
        message_id=types.N2kAISMessageID.Standard_Class_B_position_report,
        repeat=types.N2kAISRepeat.Final,
        user_id=None,
        name=None,
        ais_info=types.N2kAISTransceiverInformation.Channel_A_VDL_transmission,
        sid=None,
    )
    msg = messages.create_n2k_ais_class_b_static_data_part_a_message(
        ais_class_b_static_data_part_a,
    )
    assert (
        messages.parse_n2k_ais_class_b_static_data_part_a(msg)
        == ais_class_b_static_data_part_a
    )


def test_ais_class_b_static_data_part_b_message() -> None:
    ais_class_b_static_data_part_b = messages.AISClassBStaticDataPartB(
        message_id=types.N2kAISMessageID.Extended_Class_B_position_report,
        repeat=types.N2kAISRepeat.Initial,
        user_id=123456789,
        callsign="LZ1234",
        vessel_type=120,
        vendor="ACME-12",
        length=123,
        beam=45.2,
        pos_ref_stbd=4.0,
        pos_ref_bow=12.5,
        mothership_id=123456780,
        ais_info=types.N2kAISTransceiverInformation.Channel_A_VDL_transmission,
        sid=135,
    )

    msg = messages.create_n2k_ais_class_b_static_data_part_b_message(
        ais_class_b_static_data_part_b,
    )
    assert (
        messages.parse_n2k_ais_class_b_static_data_part_b(msg)
        == ais_class_b_static_data_part_b
    )


def test_empty_ais_class_b_static_data_part_b_message() -> None:
    ais_class_b_static_data_part_b = messages.AISClassBStaticDataPartB(
        message_id=types.N2kAISMessageID.Extended_Class_B_position_report,
        repeat=types.N2kAISRepeat.Initial,
        user_id=None,
        callsign=None,
        vessel_type=None,
        vendor=None,
        length=None,
        beam=None,
        pos_ref_stbd=None,
        pos_ref_bow=None,
        mothership_id=None,
        ais_info=types.N2kAISTransceiverInformation.Channel_A_VDL_transmission,
        sid=None,
    )

    msg = messages.create_n2k_ais_class_b_static_data_part_b_message(
        ais_class_b_static_data_part_b,
    )
    assert (
        messages.parse_n2k_ais_class_b_static_data_part_b(msg)
        == ais_class_b_static_data_part_b
    )


def test_waypoint_list_message() -> None:
    waypoint_list = messages.WaypointList(
        start=0,
        num_waypoints=4,
        database=3,
        waypoints=[
            types.Waypoint(
                id=0,
                name="Waypoint 1",
                latitude=13.162258,
                longitude=52.426179,
            ),
            types.Waypoint(
                id=2,
                name="Waypoint 2",
                latitude=13.362258,
                longitude=52.456179,
            ),
            types.Waypoint(
                id=10,
                name="Waypoint the Third",
                latitude=13.122258,
                longitude=52.026179,
            ),
            types.Waypoint(
                id=32450,
                name="Sir Waypointsalot the Fourth",
                latitude=13.162358,
                longitude=52.426079,
            ),
        ],
    )
    msg = messages.create_n2k_waypoint_list_message(waypoint_list)
    assert messages.parse_n2k_waypoint_list(msg) == waypoint_list


def test_empty_waypoint_list_message() -> None:
    waypoint_list = messages.WaypointList(
        start=None,
        num_waypoints=None,
        database=None,
        waypoints=[
            types.Waypoint(
                id=None,
                name=None,
                latitude=None,
                longitude=None,
            ),
        ],
    )
    msg = messages.create_n2k_waypoint_list_message(waypoint_list)
    assert messages.parse_n2k_waypoint_list(msg) == waypoint_list


def test_wind_speed_message() -> None:
    wind_speed = messages.WindSpeed(
        wind_speed=10.04,
        wind_angle=1.234,
        wind_reference=types.N2kWindReference.TrueNorth,
        sid=135,
    )
    msg = messages.create_n2k_wind_speed_message(wind_speed)
    assert messages.parse_n2k_wind_speed(msg) == wind_speed


def test_empty_wind_speed_message() -> None:
    wind_speed = messages.WindSpeed(
        wind_speed=None,
        wind_angle=None,
        wind_reference=types.N2kWindReference.Unavailable,
        sid=None,
    )
    msg = messages.create_n2k_wind_speed_message(wind_speed)
    assert messages.parse_n2k_wind_speed(msg) == wind_speed


def test_outside_environmental_parameters_message() -> None:
    outside_environmental_parameters = messages.OutsideEnvironmentalParameters(
        water_temperature=303.23,
        outside_ambient_air_temperature=310.15,
        atmospheric_pressure=1100,
        sid=135,
    )
    msg = messages.create_n2k_outside_environmental_parameters_message(
        outside_environmental_parameters,
    )
    assert (
        messages.parse_n2k_outside_environmental_parameters(msg)
        == outside_environmental_parameters
    )


def test_empty_outside_environmental_parameters_message() -> None:
    outside_environmental_parameters = messages.OutsideEnvironmentalParameters(
        water_temperature=None,
        outside_ambient_air_temperature=None,
        atmospheric_pressure=None,
        sid=None,
    )
    msg = messages.create_n2k_outside_environmental_parameters_message(
        outside_environmental_parameters,
    )
    assert (
        messages.parse_n2k_outside_environmental_parameters(msg)
        == outside_environmental_parameters
    )


def test_environmental_parameters_message() -> None:
    environmental_parameters = messages.EnvironmentalParameters(
        temp_source=types.N2kTempSource.ApparentWindChillTemperature,
        temperature=303.23,
        humidity_source=types.N2kHumiditySource.OutsideHumidity,
        humidity=50.024,
        atmospheric_pressure=1100,
        sid=135,
    )
    msg = messages.create_n2k_environmental_parameters_message(
        environmental_parameters,
    )
    assert messages.parse_n2k_environmental_parameters(msg) == environmental_parameters


def test_empty_environmental_parameters_message() -> None:
    environmental_parameters = messages.EnvironmentalParameters(
        temp_source=types.N2kTempSource.ShaftSealTemperature,
        temperature=None,
        humidity_source=types.N2kHumiditySource.InsideHumidity,
        humidity=None,
        atmospheric_pressure=None,
        sid=None,
    )
    msg = messages.create_n2k_environmental_parameters_message(
        environmental_parameters,
    )
    assert messages.parse_n2k_environmental_parameters(msg) == environmental_parameters


def test_temperature_message() -> None:
    temperature = messages.Temperature(
        temp_instance=135,
        temp_source=types.N2kTempSource.ApparentWindChillTemperature,
        actual_temperature=293.57,
        set_temperature=295.15,
        sid=135,
    )
    msg = messages.create_n2k_temperature_message(temperature)
    assert messages.parse_n2k_temperature(msg) == temperature


def test_empty_temperature_message() -> None:
    temperature = messages.Temperature(
        temp_instance=None,
        temp_source=types.N2kTempSource.ApparentWindChillTemperature,
        actual_temperature=None,
        set_temperature=None,
        sid=135,
    )
    msg = messages.create_n2k_temperature_message(temperature)
    assert messages.parse_n2k_temperature(msg) == temperature


def test_humidity_message() -> None:
    humidity = messages.Humidity(
        humidity_instance=135,
        humidity_source=types.N2kHumiditySource.InsideHumidity,
        actual_humidity=50.024,
        set_humidity=39.128,
        sid=135,
    )
    msg = messages.create_n2k_humidity_message(humidity)
    assert messages.parse_n2k_humidity(msg) == humidity


def test_empty_humidity_message() -> None:
    humidity = messages.Humidity(
        humidity_instance=None,
        humidity_source=types.N2kHumiditySource.OutsideHumidity,
        actual_humidity=None,
        set_humidity=None,
        sid=None,
    )
    msg = messages.create_n2k_humidity_message(humidity)
    assert messages.parse_n2k_humidity(msg) == humidity


def test_actual_pressure_message() -> None:
    actual_pressure = messages.ActualPressure(
        pressure_instance=135,
        pressure_source=types.N2kPressureSource.Atmospheric,
        actual_pressure=102200.2,
        sid=135,
    )
    msg = messages.create_n2k_actual_pressure_message(actual_pressure)
    assert messages.parse_n2k_actual_pressure(msg) == actual_pressure


def test_empty_actual_pressure_message() -> None:
    actual_pressure = messages.ActualPressure(
        pressure_instance=None,
        pressure_source=types.N2kPressureSource.Unavailable,
        actual_pressure=None,
        sid=None,
    )
    msg = messages.create_n2k_actual_pressure_message(actual_pressure)
    assert messages.parse_n2k_actual_pressure(msg) == actual_pressure


def test_set_pressure_message() -> None:
    set_pressure = messages.SetPressure(
        pressure_instance=135,
        pressure_source=types.N2kPressureSource.CompressedAir,
        set_pressure=1002200.2,
        sid=135,
    )
    msg = messages.create_n2k_set_pressure_message(set_pressure)
    assert messages.parse_n2k_set_pressure(msg) == set_pressure


def test_empty_set_pressure_message() -> None:
    set_pressure = messages.SetPressure(
        pressure_instance=None,
        pressure_source=types.N2kPressureSource.Unavailable,
        set_pressure=None,
        sid=None,
    )
    msg = messages.create_n2k_set_pressure_message(set_pressure)
    assert messages.parse_n2k_set_pressure(msg) == set_pressure


def test_product_information_message() -> None:
    product_information = types.ProductInformation(
        n2k_version=2101,
        product_code=345,
        n2k_model_id="TestModel",
        n2k_sw_code="BleedingEdge",
        n2k_model_version="1.0.0",
        n2k_model_serial_code="1234567890",
        certification_level=4,
        load_equivalency=5,
    )
    msg = messages.create_n2k_product_information_message(product_information, 45)
    assert messages.parse_n2k_pgn_product_information(msg) == product_information


def test_empty_product_information_message() -> None:
    product_information = types.ProductInformation(
        n2k_version=None,
        product_code=None,
        n2k_model_id=None,
        n2k_sw_code=None,
        n2k_model_version=None,
        n2k_model_serial_code=None,
        certification_level=None,
        load_equivalency=None,
    )
    msg = messages.create_n2k_product_information_message(product_information, 45)
    assert messages.parse_n2k_pgn_product_information(msg) == product_information


def test_configuration_information_message() -> None:
    configuration_information = types.ConfigurationInformation(
        manufacturer_information="Test Manufacturer",
        installation_description1="Test Installation 1",
        installation_description2="Test Installation 2",
    )
    msg = messages.create_n2k_configuration_information_message(
        configuration_information,
    )
    assert (
        messages.parse_n2k_pgn_configuration_information(msg)
        == configuration_information
    )


def test_pgn_iso_request_message() -> None:
    msg = messages.create_n2k_pgn_iso_request_message(45, PGN.IsoAddressClaim)
    assert messages.parse_n2k_pgn_iso_request(msg) == PGN.IsoAddressClaim
