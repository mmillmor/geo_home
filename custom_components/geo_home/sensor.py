from __future__ import annotations
from .geohome import GeoHomeHub
import logging
import async_timeout
from datetime import datetime, time, date, timedelta

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass
)
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass
)
from homeassistant.const import STATE_OFF, STATE_ON, UnitOfEnergy, UnitOfPower, UnitOfVolume
from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):

    username = config_entry.data.get("username")
    password = config_entry.data.get("password")
    hub = GeoHomeHub(username, password, hass)

    coordinator = MyCoordinator(hass, hub)

    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [   GeoHomeElectricityCreditRemaining(coordinator, hub),
            GeoHomeGasCreditRemaining(coordinator, hub),
            GeoHomeElectricityEmergencyCreditBalance(coordinator, hub),
            GeoHomeGasEmergencyCreditBalance(coordinator, hub),
            GeoHomeElectricitySupplyStatus(coordinator, hub),
            GeoHomeGasSupplyStatus(coordinator, hub),
            GeoHomeGasSensor(coordinator, hub),
            GeoHomeGasM3Sensor(coordinator, hub),
            GeoHomeElectricitySensor(coordinator, hub),
            GeoHomeGasPriceSensor(coordinator, hub),
            GeoHomeGasStandingChargeSensor(coordinator, hub),
            GeoHomeElectricityPriceSensor(coordinator, hub),
            GeoHomeElectricityStandingChargeSensor(coordinator, hub),
            GeoHomeGasPowerSensor(coordinator, hub),
            GeoHomeElectricityPowerSensor(coordinator, hub),
            GeoHomeGasCostPerHourSensor(coordinator, hub),
            GeoHomeElectricityCostPerHourSensor(coordinator, hub),
            GeoHomeGasCostTodaySensor(coordinator, hub),
            GeoHomeGasCostThisWeekSensor(coordinator, hub),
            GeoHomeGasCostThisMonthSensor(coordinator, hub),
            GeoHomeGasCostThisBillSensor(coordinator, hub),
            GeoHomeElectricityCostTodaySensor(coordinator, hub),
            GeoHomeElectricityCostThisWeekSensor(coordinator, hub),
            GeoHomeElectricityCostThisMonthSensor(coordinator, hub),
            GeoHomeElectricityCostThisBillSensor(coordinator, hub),
            GeoHomeGaskWhTodaySensor(coordinator, hub),
            GeoHomeGaskWhThisWeekSensor(coordinator, hub),
            GeoHomeGaskWhThisMonthSensor(coordinator, hub),
            GeoHomeElectricitykWhTodaySensor(coordinator, hub),
            GeoHomeElectricitykWhThisWeekSensor(coordinator, hub),
            GeoHomeElectricitykWhThisMonthSensor(coordinator, hub),
            GeoHomeGasZigbeeConnected(coordinator, hub),
            GeoHomeElectricityZigbeeConnected(coordinator, hub),
            GeoHomeHanConnected(coordinator, hub),
        ]
    )

class MyCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, hub):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="geo home sensor",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=120),
        )
        self.hub = hub

    async def _async_update_data(self):
        async with async_timeout.timeout(30):
            return await self.hub.get_device_data()

class GeoHomeElectricityCreditRemaining(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Credit Remaining"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_Credit_Remaining"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityCreditRemaining

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

    @property
    def last_reset(self):
        return None

class GeoHomeGasCreditRemaining(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Credit Remaining"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_Credit_Remaining"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasCreditRemaining

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

    @property
    def last_reset(self):
        return None

class GeoHomeElectricityEmergencyCreditBalance(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Emergency Credit Balance"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_Emergency_Credt_Balance"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityEmergencyCreditBalance

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

    @property
    def last_reset(self):
        return None

class GeoHomeGasEmergencyCreditBalance(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Emergency Credit Balance"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_Emergency_Credt_Balance"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasEmergencyCreditBalance

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

    @property
    def last_reset(self):
        return None

class GeoHomeElectricitySupplyStatus(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Supply Status"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_supply_status"

    @property
    def is_on(self):
        """Return the state of the sensor."""
        if self.hub.electricitySupplyStatus is not None:
            if self.hub.electricitySupplyStatus=="SUPPLYON":
                return STATE_ON
            else:
                return STATE_OFF
        return None

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if self.hub.electricitySupplyStatus is not None:
            if self.hub.electricitySupplyStatus=="SUPPLYON":
                return "mdi:flash"
            else :
                return "mdi:flash-outline"
        return "mdi:flash-off-outline"

class GeoHomeGasSupplyStatus(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Supply Status"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_supply_status"

    @property
    def is_on(self):
        """Return the state of the sensor."""
        if self.hub.gasSupplyStatus is not None:
            if self.hub.gasSupplyStatus=="SUPPLYON":
                return STATE_ON
            else:
                return STATE_OFF
        return None

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if self.hub.gasSupplyStatus is not None:
            if self.hub.gasSupplyStatus=="SUPPLYON":
                return "mdi:fire"
            else :
                return "mdi:fire-off"
        return "mdi:fire-alert"

class GeoHomeGasSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_total"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gaskWhReading

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:fire"

    @property
    def last_reset(self):
        return None

class GeoHomeGasM3Sensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.GAS
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfVolume.CUBIC_METERS
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas m³"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_m3_total"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasReading

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:fire"

    @property
    def last_reset(self):
        return None

class GeoHomeGasPriceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP/kWh"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Price per kWh"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_price"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasPrice

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

class GeoHomeGasStandingChargeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP/day"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Standing Charge per Day"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_standing_charge"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasStandingCharge

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

class GeoHomeElectricitySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_total"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityReading

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:flash"

    @property
    def last_reset(self):
        return None


class GeoHomeElectricityPriceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP/kWh"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Price per kWh"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_price"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityPrice

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

class GeoHomeElectricityStandingChargeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP/day"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Standing Charge per Day"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_standing_charge"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityStandingCharge

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"


class GeoHomeGasPowerSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Power"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_power"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasPower

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:fire"

    @property
    def last_reset(self):
        return None


class GeoHomeElectricityPowerSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Power"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_power"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityPower

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:flash"

    @property
    def last_reset(self):
        return None

class GeoHomeGasCostPerHourSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP/hour"
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Cost Per Hour"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_cost_per_hour"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if(self.hub.gasPower is not None and self.hub.gasPrice is not None):
            return round(self.hub.gasPower*self.hub.gasPrice/1000,2)
        else:
            return None

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

    @property
    def last_reset(self):
        return None

class GeoHomeElectricityCostPerHourSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP/hour"
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Cost Per Hour"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_cost_per_hour"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if(self.hub.electricityPower is not None and self.hub.electricityPrice is not None):
            return round(self.hub.electricityPower*self.hub.electricityPrice/1000,2)
        else:
            return None

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

    @property
    def last_reset(self):
        return None


class GeoHomeGasCostTodaySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP"
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Cost Today"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_cost_today"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasCostToday

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

    @property
    def last_reset(self):
        return datetime.combine(date.today(), datetime.min.time())


class GeoHomeGasCostThisWeekSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP"
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Cost This Week"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_cost_this_week"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasCostThisWeek

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

    @property
    def last_reset(self):
        today = date.today()
        start = today - timedelta(days=today.weekday())

        return datetime.combine(start, datetime.min.time())

class GeoHomeGasCostThisMonthSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP"
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Cost This Month"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_cost_this_month"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasCostThisMonth

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

    @property
    def last_reset(self):
        return datetime.combine(datetime.today().replace(day=1), datetime.min.time())

class GeoHomeGasCostThisBillSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP"
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Cost This Bill"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_cost_this_bill"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasCostThisBill

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

    @property
    def last_reset(self):
        if self.hub.gasCostThisBillTimestamp is None:
          return None
        else:
          return datetime.fromtimestamp(self.hub.gasCostThisBillTimestamp)


class GeoHomeElectricityCostTodaySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP"
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Cost Today"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_cost_today"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityCostToday

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

    @property
    def last_reset(self):
        return datetime.combine(date.today(), datetime.min.time())


class GeoHomeElectricityCostThisWeekSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP"
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Cost This Week"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_cost_this_week"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityCostThisWeek

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

    @property
    def last_reset(self):
        today = date.today()
        start = today - timedelta(days=today.weekday())

        return datetime.combine(start, datetime.min.time())

class GeoHomeElectricityCostThisMonthSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP"
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Cost This Month"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_cost_this_month"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityCostThisMonth

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

    @property
    def last_reset(self):
        return datetime.combine(datetime.today().replace(day=1), datetime.min.time())

class GeoHomeElectricityCostThisBillSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "GBP"
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Cost This Bill"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_cost_this_bill"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityCostThisBill

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"

    @property
    def last_reset(self):
        if self.hub.electricityCostThisBillTimestamp is None:
          return None
        else:
          return datetime.fromtimestamp(self.hub.electricityCostThisBillTimestamp)


class GeoHomeGaskWhTodaySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas kWh Today"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_kwh_today"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gaskWhToday

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:fire"

    @property
    def last_reset(self):
        return datetime.combine(date.today(), datetime.min.time())


class GeoHomeGaskWhThisWeekSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas kWh This Week"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_kwh_this_week"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gaskWhThisWeek

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:fire"

    @property
    def last_reset(self):
        today = date.today()
        start = today - timedelta(days=today.weekday())

        return datetime.combine(start, datetime.min.time())

class GeoHomeGaskWhThisMonthSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas kWh This Month"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_kwh_this_month"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gaskWhThisMonth

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:fire"

    @property
    def last_reset(self):
        return datetime.combine(datetime.today().replace(day=1), datetime.min.time())

class GeoHomeElectricitykWhTodaySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity kWh Today"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_kwh_today"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricitykWhToday

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:flash"

    @property
    def last_reset(self):
        return datetime.combine(date.today(), datetime.min.time())


class GeoHomeElectricitykWhThisWeekSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity kWh This Week"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_kwh_this_week"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricitykWhThisWeek

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:flash"

    @property
    def last_reset(self):
        today = date.today()
        start = today - timedelta(days=today.weekday())

        return datetime.combine(start, datetime.min.time())

class GeoHomeElectricitykWhThisMonthSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity kWh This Month"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_kwh_this_month"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricitykWhThisMonth

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:flash"

    @property
    def last_reset(self):
        return datetime.combine(datetime.today().replace(day=1), datetime.min.time())

class GeoHomeGasZigbeeConnected(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Meter Zigbee Connection"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "gas_zigbee_connection"

    @property
    def is_on(self):
        """Return the state of the sensor."""
        if self.hub.gasZigbeeStatus is not None:
            if self.hub.gasZigbeeStatus=="CONNECTED":
                return STATE_ON
            else:
                return STATE_OFF
        return None

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if self.hub.gasZigbeeStatus is not None:
            if self.hub.gasZigbeeStatus=="CONNECTED":
                return "mdi:lan-connect"
            else :
                return "mdi:lan-disconnect"
        return "mdi:lan-pending"

class GeoHomeElectricityZigbeeConnected(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Meter Zigbee Connection"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "electricity_zigbee_connection"

    @property
    def is_on(self):
        """Return the state of the sensor."""
        if self.hub.electricityZigbeeStatus is not None:
            if self.hub.electricityZigbeeStatus=="CONNECTED":
                return STATE_ON
            else:
                return STATE_OFF
        return None

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if self.hub.electricityZigbeeStatus is not None:
            if self.hub.electricityZigbeeStatus=="CONNECTED":
                return "mdi:lan-connect"
            else :
                return "mdi:lan-disconnect"
        return "mdi:lan-pending"

class GeoHomeHanConnected(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Geo Home HAN Connection"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_han_connection"

    @property
    def is_on(self):
        """Return the state of the sensor."""
        if self.hub.hanStatus is not None:
            if self.hub.hanStatus=="CONNECTED":
                return STATE_ON
            else:
                return STATE_OFF
        return None

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if self.hub.hanStatus is not None:
            if self.hub.hanStatus=="CONNECTED":
                return "mdi:lan-connect"
            else :
                return "mdi:lan-disconnect"
        return "mdi:lan-pending"
